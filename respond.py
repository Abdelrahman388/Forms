from flask import Flask, flash, json, jsonify, redirect, render_template, request, session, url_for
from datetime import datetime
from flask_login import LoginManager, login_required, current_user
from flask import Blueprint
from flask_wtf.csrf import generate_csrf, validate_csrf
from collections import defaultdict

from models import db,User,Form, Question, Option,Responder,Response, generate_random_id

respond_bp = Blueprint('respond', __name__)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

@respond_bp.route("/respond/<form_id>" ,methods = ["GET","POST"])
def respond(form_id):
    # form = db.execute("SELECT * FROM forms WHERE form_id = ?",form_id)[0]
    form = Form.query.filter_by(id=form_id).first()
    
    # questions = db.execute("SELECT * FROM questions WHERE form_id = ?",form_id)
    questions = Question.query.filter_by(formId=form_id).all()
    
    # options=db.execute("SELECT * FROM options")
    options = Option.query.all()


    options = Option.query.all()
    options_map = defaultdict(list)
    for opt in options:
        options_map[opt.questionId].append(opt)
    
    if request.method=="GET":
        # Check if user has already responded (if they have a session)
        if session.get("responded_forms") and str(form_id) in session.get("responded_forms", []):
            return redirect(url_for('respond.response_submitted', form_id=form_id))
        
        return render_template("respond.html" ,form=form, questions=questions, options_map=options_map)
    else:
        # responder_name=request.form.get("name") 
        
        # if responder_name =="":
        #     return render_template("respond.html" ,form=form, questions=questions, options_map=options_map) 
        
        
        # Check if user has already responded
        if session.get("responded_forms") and str(form_id) in session.get("responded_forms", []):
            return redirect(url_for('respond.response_submitted', form_id=form_id))
        
        # Create new responder with unique ID
        responder_id = generate_random_id()
        while Responder.query.get(responder_id):
            responder_id = generate_random_id()
            
        responder_name = "resp_" + generate_random_id()
        while Responder.query.filter_by(name=responder_name).first():
            responder_name = "resp_" + generate_random_id()

        new_responder = Responder(id=responder_id, name=responder_name)
        db.session.add(new_responder)
        db.session.flush()  # Flush to get the ID without committing
        
        # Set session responder_id immediately after creating responder
        session["responder_id"] = new_responder.id
        
        # Validate all questions before processing
        for question in questions:
            answers = None  # Initialize answers for each question
            
            if question.answerType != "text":
                question_options = Option.query.filter_by(questionId=question.id).all()
                option_list = [opt.text for opt in question_options]
                
                if question.answerType == "radio":
                    answers = request.form.get(f"{question.id}")
                    if answers and answers not in option_list:
                        db.session.rollback()  # Rollback if validation fails
                        return "One of the selected options is not in the options list"
                elif question.answerType == "checkbox":
                    answers = request.form.getlist(f"{question.id}")
                    for answer in answers:
                        if answer not in option_list:
                            db.session.rollback()  # Rollback if validation fails
                            return "One of the selected options is not in the options list"
                elif question.answerType == "dropdown":
                    answers = request.form.get(f"{question.id}")
                    if answers and answers not in option_list:
                        db.session.rollback()  # Rollback if validation fails
                        return "Selected option is not in the options list"
            else:
                # For text questions
                answers = request.form.get(f"{question.id}")
            
            # Check if required question is empty
            if question.answerType != "checkbox" and (not answers or answers == ""):
                db.session.rollback()  # Rollback if validation fails
                return render_template("respond.html", form=form, questions=questions, options_map=options_map)
            elif question.answerType == "checkbox" and (not answers or len(answers) == 0):
                # For checkbox, it's optional, so we can continue
                pass
        
        date_time = datetime.now()
        date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
        
        for question in questions:
            if question.answerType != "checkbox":
                answer = request.form.get(f"{question.id}")
                
                # Generate unique ID for new response
                response_id = generate_random_id()
                while Response.query.get(response_id):
                    response_id = generate_random_id()
                    
                new_response = Response(
                    id=response_id,
                    answer=answer,
                    createdAt=date_time,
                    questionId=question.id,
                    formId=form_id,
                    responderId=session["responder_id"]
                )
                db.session.add(new_response)
            else:
                answers = request.form.getlist(f"{question.id}")
                Answer = ""
                for index, answer in enumerate(answers):
                    Answer += f"{answer}"
                    if index != (len(answers)-1):
                        Answer += ", "
                
                response_id = generate_random_id()
                while Response.query.get(response_id):
                    response_id = generate_random_id()
                    
                new_response = Response(
                    id=response_id,
                    answer=Answer,
                    createdAt=date_time,
                    questionId=question.id,
                    formId=form_id,
                    responderId=session["responder_id"]
                )
                db.session.add(new_response)

        form.responsesCount = (form.responsesCount or 0) + 1
        
        # Commit all changes at once
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Database error: {str(e)}"
        
        # Mark this form as responded to in the session
        if "responded_forms" not in session:
            session["responded_forms"] = []
        session["responded_forms"].append(str(form_id))
        session.permanent = True  # Make session persistent
        
        # Store submission time
        session[f"submission_time_{form_id}"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return redirect(url_for('respond.response_submitted', form_id=form_id))

@respond_bp.route("/response-submitted/<form_id>")
def response_submitted(form_id):
    """Display response submitted confirmation page"""
    # Check if user actually submitted a response
    if not session.get("responded_forms") or str(form_id) not in session.get("responded_forms", []):
        # Redirect to form if no submission found
        return redirect(url_for('respond.respond', form_id=form_id))
    
    form = Form.query.filter_by(id=form_id).first()
    if not form:
        return "Form not found", 404
    
    submission_time = session.get(f"submission_time_{form_id}", "Unknown")
    
    return render_template("response_submitted.html", 
                         form=form, 
                         submission_time=submission_time)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

@respond_bp.route("/responses_statistics/<form_id>" ,methods = ["GET"])
@login_required
def responses_statistics(form_id):
    if request.method == "GET":
        form = Form.query.filter_by(id=form_id).first()
        
        questions = Question.query.filter_by(formId=form_id).all()
        questionsJson = [q.toJson() for q in questions]
        options = Option.query.all()
        
        # Fix the responses query to get proper objects
        responses_query = db.session.query(Response, Responder).join(Responder, Response.responderId == Responder.id).filter(Response.formId == form_id).all()
        
        # Convert to serializable format
        responses = []
        for response, responder in responses_query:
            responses.append({
                'id': response.id,
                'answer': response.answer,
                'createdAt': response.createdAt,
                'questionId': response.questionId,
                'formId': response.formId,
                'responderId': response.responderId,
                'responder_name': responder.name
            })
        
        # Enhanced option_answer_count query to handle checkbox responses
        option_answer_count = []
        
        for question in questions:
            if question.answerType != "text":
                question_options = Option.query.filter_by(questionId=question.id).all()
                
                for option in question_options:
                    if question.answerType == "checkbox":
                        # For checkbox, count occurrences of each option in comma-separated answers
                        count = db.session.query(Response).filter(
                            Response.questionId == question.id,
                            Response.answer.like(f'%{option.text}%')
                        ).count()
                    else:
                        # For radio and dropdown, exact match
                        count = db.session.query(Response).filter(
                            Response.questionId == question.id,
                            Response.answer == option.text
                        ).count()
                    
                    if count > 0:  # Only include options that have responses
                        option_answer_count.append({
                            'option': option.text,
                            'count': count,
                            'question_id': question.id
                        })
        
        return render_template("responses.html", 
                             form=form,
                             questions=questionsJson,
                             options=options,
                             responses=responses,
                             option_answer_count=option_answer_count)

