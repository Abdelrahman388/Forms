"""
Main blueprint for the application's main routes.
"""
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from models import Form

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    """Main dashboard showing user's forms"""
    try:
        # Clean up any empty forms first
        Form.cleanup_empty_forms(current_user.id)
        
        # Get user's forms
        forms = Form.get_by_user(current_user.id)
        
        if request.is_json:
            # Return JSON for AJAX requests
            return jsonify({
                'success': True,
                'forms': [
                    {
                        'form_id': form.form_id,
                        'name': form.name,
                        'title': form.title,
                        'datetime_created': form.datetime_created,
                        'responses_no': form.responses_no,
                        'question_count': form.question_count
                    } for form in forms
                ]
            })
        
        return render_template('index.html', forms=forms)
    
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)})
        return f"An error occurred: {str(e)}", 500
