from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from models import Form
from models import db
from sqlalchemy import or_
# Blueprint name should be 'home' to match the import in app.py
home_bp = Blueprint('home', __name__)


@home_bp.route('/',methods=['GET','POST'])
@login_required
def index():
    try:
        empty_forms = Form.query.filter(Form.userId == current_user.id,
            or_(Form.name == "", Form.title == "", Form.questionCount <= 0)
        ).all()

        for form in empty_forms:
            db.session.delete(form)
        db.session.commit()
        
        # Get user's forms
        forms = Form.query.filter_by(userId=current_user.id).all()
        
        # if request.is_json:
        #     # Return JSON for AJAX requests
        #     return jsonify({
        #         'success': True,
        #         'forms': [
        #             {
        #                 'formId': form.id,
        #                 'name': form.name,
        #                 'title': form.title,
        #                 'createdAt': form.createdAt,
        #                 'responsesCount': form.responsesCount,
        #                 'questionCount': form.questionCount
        #             } for form in forms
        #         ]
        #     })
        
        return render_template('index.html', forms=forms)
    
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return f"An error occurred: {str(e)}", 500

