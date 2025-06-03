"""
Respond blueprint for form responses and statistics.
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_login import login_required
from models import Form, Question, Option, Responder, Response

respond_bp = Blueprint('respond', __name__)


@respond_bp.route('/respond/<int:form_id>', methods=['GET', 'POST'])
def respond(form_id):
    """Handle form responses"""
    try:
        form = Form.get_by_id(form_id)
        if not form:
            return "Form not found", 404
        
        questions = Question.get_written(form_id)
        if not questions:
            return "This form has no questions", 400
        
        if request.method == 'GET':
            # Get all options for display
            all_options = Option.get_saved(form_id)
            return render_template('respond.html', form=form, questions=questions, options=all_options)
        
        else:  # POST
            # Get responder name
            responder_name = request.form.get('name') or request.json.get('name')
            if not responder_name:
                if request.is_json:
                    return jsonify({'success': False, 'error': 'Name is required'})
                return render_template('respond.html', form=form, questions=questions, 
                                     options=Option.get_saved(form_id), error='Name is required')
            
            # Create responder
            responder = Responder.create(responder_name)
            session['responder_id'] = responder.responder_id
            
            # Collect and validate responses
            responses_data = []
            errors = []
            
            for question in questions:
                if question.answer_type == "text":
                    answer = request.form.get(str(question.question_id)) or request.json.get(str(question.question_id))
                    if not answer:
                        errors.append(f"Answer required for: {question.question}")
                        continue
                    responses_data.append({
                        'answer': answer,
                        'q_id': question.question_id
                    })
                
                elif question.answer_type == "radio":
                    answer = request.form.get(str(question.question_id)) or request.json.get(str(question.question_id))
                    if not answer:
                        errors.append(f"Please select an option for: {question.question}")
                        continue
                    
                    # Validate option exists
                    valid_options = [opt.option for opt in Option.get_by_question(question.question_id)]
                    if answer not in valid_options:
                        errors.append(f"Invalid option selected for: {question.question}")
                        continue
                    
                    responses_data.append({
                        'answer': answer,
                        'q_id': question.question_id
                    })
                
                elif question.answer_type == "checkbox":
                    answers = request.form.getlist(str(question.question_id)) or request.json.get(str(question.question_id), [])
                    if not answers:
                        errors.append(f"Please select at least one option for: {question.question}")
                        continue
                    
                    # Validate all options exist
                    valid_options = [opt.option for opt in Option.get_by_question(question.question_id)]
                    invalid_options = [ans for ans in answers if ans not in valid_options]
                    if invalid_options:
                        errors.append(f"Invalid options selected for: {question.question}")
                        continue
                    
                    # Join multiple answers
                    answer = ", ".join(answers)
                    responses_data.append({
                        'answer': answer,
                        'q_id': question.question_id
                    })
            
            if errors:
                if request.is_json:
                    return jsonify({'success': False, 'errors': errors})
                return render_template('respond.html', form=form, questions=questions, 
                                     options=Option.get_saved(form_id), errors=errors)
            
            # Save all responses
            Response.create_bulk(responses_data, form_id, responder.responder_id)
            form.increment_responses()
            
            if request.is_json:
                return jsonify({'success': True, 'message': 'Form submitted successfully!'})
            
            return render_template('success.html', message='You have successfully submitted the form!')
    
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return f"An error occurred: {str(e)}", 500


@respond_bp.route('/responses_statistics/<int:form_id>')
@login_required
def responses_statistics(form_id):
    """View response statistics for a form"""
    try:
        form = Form.get_by_id(form_id)
        if not form:
            return "Form not found", 404
        
        # Check if current user owns this form
        from flask_login import current_user
        if form.user_id != current_user.id:
            return "Access denied", 403
        
        questions = Question.get_written(form_id)
        responses = Response.get_by_form(form_id)
        option_answer_count = Response.get_option_counts(form_id)
        
        if request.is_json:
            # Return JSON for AJAX requests
            return jsonify({
                'success': True,
                'form': {
                    'form_id': form.form_id,
                    'name': form.name,
                    'title': form.title,
                    'responses_no': form.responses_no
                },
                'questions': [
                    {
                        'question_id': q.question_id,
                        'question': q.question,
                        'answer_type': q.answer_type
                    } for q in questions
                ],
                'responses': responses,
                'option_answer_count': option_answer_count
            })
        
        # Get all options for display
        all_options = Option.get_saved(form_id)
        
        return render_template('responses.html', 
                             form=form, 
                             questions=questions, 
                             options=all_options,
                             responses=responses, 
                             option_answer_count=option_answer_count)
    
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return f"An error occurred: {str(e)}", 500
