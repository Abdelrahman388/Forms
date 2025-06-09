from flask import Flask, flash, json, jsonify, redirect, render_template, request, session
from datetime import datetime
from flask_login import LoginManager, login_required, current_user
from flask import Blueprint
from flask_wtf.csrf import generate_csrf, validate_csrf

from models import db,Form, Question, Option,generate_random_id

builder_bp = Blueprint('builder', __name__)

ANSWER_options=["text","radio","checkbox","dropdown"]

@builder_bp.route("/create" ,methods = ["GET","POST"])
@login_required
def create():
    if "form_id" not in session or not Form.query.filter_by(id=session.get("form_id"), userId=current_user.id).first():
        session["form_id"] = 0

    if request.method == "GET":
        form_data = {}

        if request.args.get("form_id"):
            session["form_id"] = str(request.args.get("form_id"))  # Convert to string
        else:
            session["form_id"] = 0

        if session["form_id"] == 0:
            # Generate unique ID for new form
            form_id = generate_random_id()
            while Form.query.get(form_id):
                form_id = generate_random_id()
                
            new_form = Form(id=form_id, name="", title="", userId=current_user.id)
            db.session.add(new_form)
            db.session.commit()
            form = new_form
            session["form_id"] = form.id
        else:
            form = Form.query.filter_by(id=session["form_id"]).first()

        questions = Question.query.filter_by(formId=form.id, saved=True).all()
        question_list = []
        for q in questions:
            options = Option.query.filter_by(questionId=q.id).all()
            question_list.append({
                "id": q.id,
                "text": q.text,
                "answerType": q.answerType,
                "options": [{"id": opt.id, "text": opt.text} for opt in options]
            })

        form_data = {
            "form_id": form.id,
            "name": form.name,
            "title": form.title,
            "description": form.description or "",
            "questions": question_list
        }

        # print(f"\n===== FORM DATA BEING SENT TO TEMPLATE =====")
        # print(f"Form Data: {form_data}")
        # print(f"JSON Form Data: {json.dumps(form_data)}")
        # print(f"==========================================\n")

        return render_template("create.html", form_data=json.dumps(form_data))

    elif request.method == "POST":
        try:
            csrf_token = request.headers.get("X-CSRFToken")
            try:
                validate_csrf(csrf_token)
            except Exception as e:
                return jsonify(success=False, error="Invalid CSRF token"), 400

            data = request.get_json()
            if not data:
                return jsonify(success=False, error="No JSON data received"), 400

            form_name = data.get("name", "").strip()
            form_title = data.get("title", "").strip()
            form_description = data.get("description", "").strip()
            questions = data.get("questions", [])

            if not form_name or not form_title:
                return jsonify(success=False, error="Form name and title are required"), 400

            form_id = session.get("form_id")
            form = Form.query.get(form_id)

            if not form or form.userId != current_user.id:
                return jsonify(success=False, error="Invalid or unauthorized form ID"), 403

            # Update form details
            form.name = form_name
            form.title = form_title
            form.description = form_description
            form.questionCount = 0
            form.responsesCount = 0
            db.session.commit()

            # Clear previous questions and options
            previous_questions = Question.query.filter_by(formId=form.id).all()
            for pq in previous_questions:
                Option.query.filter_by(questionId=pq.id).delete()
            Question.query.filter_by(formId=form.id).delete()
            db.session.commit()

            # print(f"\n===== UPDATING EXISTING FORM =====")
            # print(f"Form ID: {form.id}")
            # print(f"Name: '{form.name}'")
            # print(f"Title: '{form.title}'")
            # print(f"Questions: {questions}")
            # print(f"===========================\n")

            # Add new questions and options
            for question_data in questions:
                question_text = question_data.get("text", "").strip()
                answer_type = question_data.get("answerType", "").strip()
                options = question_data.get("options") or []

                if not question_text or answer_type not in ["text", "radio", "checkbox", "dropdown"]:
                    continue

                # Generate unique ID for new question
                question_id = generate_random_id()
                while Question.query.get(question_id):
                    question_id = generate_random_id()

                new_question = Question(
                    id=question_id,
                    text=question_text,
                    answerType=answer_type,
                    formId=form.id,
                    optionCount=len(options) if answer_type != "text" else 0,
                    saved=True
                )
                form.questionCount+= 1
                db.session.add(new_question)
                db.session.commit()

                for option_data in options:
                    option_text = option_data.get("text", "").strip()
                    if option_text:
                        # Generate unique ID for new option
                        option_id = generate_random_id()
                        while Option.query.get(option_id):
                            option_id = generate_random_id()
                            
                        new_option = Option(
                            id=option_id,
                            text=option_text,
                            questionId=new_question.id,
                            formId=form.id
                        )
                        db.session.add(new_option)

            db.session.commit()
            return jsonify(success=True, formId=form.id)

        except Exception as e:
            db.session.rollback()
            return jsonify(success=False, error=str(e)), 500
    
    
@builder_bp.route("/delete" ,methods = ["POST"])
@login_required
def delete():
    try:
        data = request.get_json()
        form_id = data.get('form_id')
        
        if not form_id:
            return jsonify({'success': False, 'error': 'Form ID is required'}), 400
        
        form = Form.query.filter_by(id=form_id, userId=current_user.id).first()
        if not form:
            return jsonify({'success': False, 'error': 'Form not found or unauthorized'}), 404
        
        db.session.delete(form)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Form deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500