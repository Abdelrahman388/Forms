"""
Builder blueprint for form creation and editing functionality.
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import Form, Question, Option
from forms import FormDetailsForm, QuestionForm, OptionForm

builder_bp = Blueprint('builder', __name__)

ANSWER_OPTIONS = ["text", "radio", "checkbox"]


@builder_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create or edit a form"""
    # Clean up any empty forms first
    Form.cleanup_empty_forms(current_user.id)
    
    if request.method == 'GET':
        # Check if we have an existing form to edit
        form_id = request.args.get('form_id')
        if form_id:
            # Editing existing form - use old server-side approach
            form = Form.get_by_id(form_id)
            if not form or form.user_id != current_user.id:
                return redirect(url_for('main.index'))
            session['form_id'] = form.form_id
            
            # Get questions and options
            written_questions = Question.get_written(form.form_id)
            empty_questions = Question.get_empty(form.form_id)
            saved_options = Option.get_saved(form.form_id)
            empty_options = Option.get_empty(form.form_id)
            
            return render_template('create.html', 
                                 form=[form], 
                                 writtenquestions=written_questions,
                                 emptyquestions=empty_questions,
                                 savedoptions=saved_options,
                                 emptyoptions=empty_options)
        else:
            # New form - use client-side approach
            return render_template('create.html')
    
    else:  # POST
        form_id = request.form.get('form_id')
        name = request.form.get('name')
        title = request.form.get('title')
        
        if request.is_json:
            # AJAX request
            try:
                form = Form.get_by_id(form_id)
                if form and form.user_id == current_user.id:
                    if name and title:
                        form.update(name, title)
                        form.cleanup_empty()
                        session['form_id'] = 0
                        return jsonify({'success': True, 'redirect': url_for('main.index')})
                    else:
                        return jsonify({'success': False, 'error': 'Form name and title are required'})
                return jsonify({'success': False, 'error': 'Form not found'})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        # Regular form submission (backward compatibility)
        form = Form.get_by_id(form_id)
        if form and form.user_id == current_user.id:
            if name and title:
                form.update(name, title)
                form.cleanup_empty()
            else:
                form.delete()
        
        session['form_id'] = 0
        return redirect(url_for('main.index'))


@builder_bp.route('/addquestion', methods=['POST'])
@login_required
def add_question():
    """Add a new question to the form"""
    form_id = request.form.get('form_id') or request.json.get('form_id')
    
    try:
        form = Form.get_by_id(form_id)
        if not form or form.user_id != current_user.id:
            raise ValueError("Form not found or access denied")
        
        # Create new question
        question = Question.create(form_id)
        form.increment_question_count()
        
        if request.is_json:
            # Return updated questions HTML for AJAX
            written_questions = Question.get_written(form_id)
            empty_questions = Question.get_empty(form_id)
            saved_options = Option.get_saved(form_id)
            empty_options = Option.get_empty(form_id)
            
            html = render_template('partials/questions.html',
                                 form=[form],
                                 writtenquestions=written_questions,
                                 emptyquestions=empty_questions,
                                 savedoptions=saved_options,
                                 emptyoptions=empty_options)
            
            return jsonify({'success': True, 'html': html})
        
        return redirect(url_for('builder.create'))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return redirect(url_for('builder.create'))


@builder_bp.route('/writequestion', methods=['POST'])
@login_required
def write_question():
    """Save a written question"""
    question_text = request.form.get('question') or request.json.get('question')
    answer_type = request.form.get('answer-type') or request.json.get('answer_type')
    question_id = request.form.get('qid') or request.json.get('qid')
    
    try:
        if answer_type not in ANSWER_OPTIONS:
            raise ValueError("Invalid answer type")
        
        question = Question.get_by_id(question_id)
        if not question:
            raise ValueError("Question not found")
        
        # Verify form ownership
        form = Form.get_by_id(question.form_id)
        if not form or form.user_id != current_user.id:
            raise ValueError("Access denied")
        
        question.update(question_text, answer_type, saved=True)
        
        if request.is_json:
            return jsonify({'success': True})
        
        return redirect(url_for('builder.create'))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return redirect(url_for('builder.create'))


@builder_bp.route('/updatequestion', methods=['POST'])
@login_required
def update_question():
    """Update a question"""
    question_text = request.form.get('question_text') or request.json.get('question_text')
    answer_type = request.form.get('type_') or request.json.get('answer_type')
    question_id = request.form.get('qid') or request.json.get('qid')
    
    try:
        if answer_type not in ANSWER_OPTIONS:
            raise ValueError("Invalid answer type")
        
        question = Question.get_by_id(question_id)
        if not question:
            raise ValueError("Question not found")
        
        # Verify form ownership
        form = Form.get_by_id(question.form_id)
        if not form or form.user_id != current_user.id:
            raise ValueError("Access denied")
        
        question.update(question_text, answer_type)
        
        if request.is_json:
            return jsonify({'success': True})
        
        return redirect(url_for('builder.create'))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return redirect(url_for('builder.create'))


@builder_bp.route('/editquestion', methods=['POST'])
@login_required
def edit_question():
    """Make a question editable"""
    question_id = request.form.get('qid') or request.json.get('qid')
    
    try:
        question = Question.get_by_id(question_id)
        if not question:
            raise ValueError("Question not found")
        
        # Verify form ownership
        form = Form.get_by_id(question.form_id)
        if not form or form.user_id != current_user.id:
            raise ValueError("Access denied")
        
        question.make_editable()
        
        if request.is_json:
            return jsonify({'success': True})
        
        return redirect(url_for('builder.create'))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return redirect(url_for('builder.create'))


@builder_bp.route('/deletequestion', methods=['POST'])
@login_required
def delete_question():
    """Delete a question"""
    question_id = request.form.get('qid') or request.json.get('qid')
    form_id = request.form.get('form_id') or request.json.get('form_id')
    
    try:
        form = Form.get_by_id(form_id)
        if not form or form.user_id != current_user.id:
            raise ValueError("Form not found or access denied")
        
        question = Question.get_by_id(question_id)
        if not question:
            raise ValueError("Question not found")
        
        question.delete()
        form.decrement_question_count()
        
        if request.is_json:
            return jsonify({'success': True})
        
        return redirect(url_for('builder.create'))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return redirect(url_for('builder.create'))


@builder_bp.route('/addoption', methods=['POST'])
@login_required
def add_option():
    """Add an option to a question"""
    question_id = request.form.get('qid') or request.json.get('qid')
    form_id = request.form.get('form_id') or request.json.get('form_id')
    option_type = request.form.get('type') or request.json.get('type')
    
    try:
        form = Form.get_by_id(form_id)
        if not form or form.user_id != current_user.id:
            raise ValueError("Form not found or access denied")
        
        question = Question.get_by_id(question_id)
        if not question:
            raise ValueError("Question not found")
        
        # Create new option
        option = Option.create(question_id, form_id)
        question.increment_option_count()
        question.update(answer_type=option_type)
        
        if request.is_json:
            return jsonify({'success': True})
        
        return redirect(url_for('builder.create'))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return redirect(url_for('builder.create'))


@builder_bp.route('/saveoption', methods=['POST'])
@login_required
def save_option():
    """Save an option"""
    option_text = request.form.get('option') or request.json.get('option')
    option_id = request.form.get('oid') or request.json.get('oid')
    
    try:
        option = Option.get_by_id(option_id)
        if not option:
            raise ValueError("Option not found")
        
        # Verify form ownership
        form = Form.get_by_id(option.form_id)
        if not form or form.user_id != current_user.id:
            raise ValueError("Access denied")
        
        option.update(option_text)
        
        if request.is_json:
            return jsonify({'success': True})
        
        return redirect(url_for('builder.create'))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return redirect(url_for('builder.create'))


@builder_bp.route('/deleteoption', methods=['POST'])
@login_required
def delete_option():
    """Delete an option"""
    option_id = request.form.get('oid') or request.json.get('oid')
    question_id = request.form.get('qid') or request.json.get('qid')
    
    try:
        option = Option.get_by_id(option_id)
        if not option:
            raise ValueError("Option not found")
        
        # Verify form ownership
        form = Form.get_by_id(option.form_id)
        if not form or form.user_id != current_user.id:
            raise ValueError("Access denied")
        
        question = Question.get_by_id(question_id)
        if question:
            question.decrement_option_count()
        
        option.delete()
        
        if request.is_json:
            return jsonify({'success': True})
        
        return redirect(url_for('builder.create'))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return redirect(url_for('builder.create'))


@builder_bp.route('/delete', methods=['POST'])
@login_required
def delete_form():
    """Delete a form"""
    form_id = request.form.get('form_id') or request.json.get('form_id')
    
    try:
        form = Form.get_by_id(form_id)
        if not form or form.user_id != current_user.id:
            raise ValueError("Form not found or access denied")
        
        form.delete()
        
        if request.is_json:
            return jsonify({'success': True})
        
        return redirect(url_for('main.index'))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return redirect(url_for('main.index'))


@builder_bp.route('/create-client-form', methods=['POST'])
@login_required
def create_client_form():
    """Create a complete form from client-side data"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('title'):
            return jsonify({'success': False, 'error': 'Form name and title are required'})
        
        if not data.get('questions') or len(data['questions']) == 0:
            return jsonify({'success': False, 'error': 'At least one question is required'})
        
        # Get the form from session (created when page loaded)
        form_id = session.get('form_id')
        if not form_id:
            return jsonify({'success': False, 'error': 'No form session found'})
        
        form = Form.get_by_id(form_id)
        if not form or form.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Form not found or access denied'})
        
        # Update form basic info
        form.update(data['name'], data['title'])
        if data.get('restrictToOne'):
            # Add restrict_to_one field to form if needed
            pass  # This can be implemented if you have this field in your form model
        
        # Create all questions and options
        for question_data in data['questions']:
            if not question_data.get('question') or not question_data.get('answerType'):
                continue
                
            # Create question
            question = Question.create(form_id)
            question.update(
                question_text=question_data['question'],
                answer_type=question_data['answerType'],
                saved=True
            )
            
            # Create options for radio/checkbox questions
            if question_data['answerType'] in ['radio', 'checkbox'] and question_data.get('options'):
                for option_data in question_data['options']:
                    if option_data.get('option'):
                        option = Option.create(question.question_id, form_id)
                        option.save_text(option_data['option'])
        
        # Update form question count
        form.update_question_count()
        
        # Clear session
        session['form_id'] = 0
        
        return jsonify({
            'success': True, 
            'message': 'Form created successfully!',
            'redirect': url_for('main.index')
        })
        
    except Exception as e:
        print(f"Error creating client form: {e}")  # For debugging
        return jsonify({'success': False, 'error': str(e)})
    

@builder_bp.route('/create-temp-form', methods=['POST'])
@login_required
def create_temp_form():
    """Create a temporary form for hybrid form builder"""
    try:
        # Check if user is properly authenticated
        if not current_user or not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'User not authenticated'})
            
        # Get user ID safely
        user_id = getattr(current_user, 'id', None)
        if not user_id:
            return jsonify({'success': False, 'error': 'Invalid user session'})
        
        # Clean up any existing empty forms for this user
        Form.cleanup_empty_forms(user_id)
        
        name = request.form.get('name', 'Untitled Form')
        title = request.form.get('title', 'Untitled Form')
        
        # Create a new form with proper error handling
        form = Form.create(name, title, user_id)
        if not form:
            return jsonify({'success': False, 'error': 'Failed to create form'})
            
        session['form_id'] = form.form_id
        
        return jsonify({
            'success': True,
            'form_id': form.form_id,
            'message': 'Temporary form created'
        })
        
    except Exception as e:
        print(f"Error creating temp form: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Database error: {str(e)}'})


@builder_bp.route('/get-form-data/<form_id>')
@login_required
def get_form_data(form_id):
    """Get form data with questions and options for hybrid form builder"""
    try:
        form = Form.get_by_id(form_id)
        if not form or form.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Form not found or access denied'})
        
        # Get all questions for this form
        questions = []
        
        # Get written (saved) questions
        written_questions = Question.get_written(form_id)
        for q in written_questions:
            question_data = {
                'question_id': q.question_id,
                'question_text': q.question_text,
                'answer_type': q.answer_type,
                'saved': True,
                'options': []
            }
              # Get options for this question if it's radio/checkbox
            if q.answer_type in ['radio', 'checkbox']:
                all_options = Option.get_by_question(q.question_id)
                saved_options = [opt for opt in all_options if opt.option != ""]
                empty_options = [opt for opt in all_options if opt.option == ""]
                
                # Add saved options
                for opt in saved_options:
                    question_data['options'].append({
                        'option_id': opt.option_id,
                        'option_text': opt.option_text,
                        'saved': True
                    })
                
                # Add empty options
                for opt in empty_options:
                    question_data['options'].append({
                        'option_id': opt.option_id,
                        'option_text': '',
                        'saved': False
                    })
            
            questions.append(question_data)
        
        # Get empty (unsaved) questions
        empty_questions = Question.get_empty(form_id)
        for q in empty_questions:
            question_data = {
                'question_id': q.question_id,
                'question_text': '',
                'answer_type': 'text',
                'saved': False,
                'options': []
            }
            questions.append(question_data)
        
        form_data = {
            'form_id': form.form_id,
            'name': form.name,
            'title': form.title,
            'questions': questions
        }
        
        return jsonify({
            'success': True,
            'form_data': form_data
        })
        
    except Exception as e:
        print(f"Error getting form data: {e}")
        return jsonify({'success': False, 'error': str(e)})
