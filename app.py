


"""
Main application factory and entry point for the Forms application.
This file replaces the old app.py with a modern Flask structure using blueprints.
"""
from flask import Flask, render_template
from flask_login import LoginManager
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
import os

from models import User
from auth import auth_bp
from main import main_bp
from builder import builder_bp
from respond import respond_bp


def create_app(test_config=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure application
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-change-in-production'),
        SESSION_PERMANENT=False,
        SESSION_TYPE='filesystem',
        WTF_CSRF_ENABLED=True,
        WTF_CSRF_TIME_LIMIT=None
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # Initialize extensions
    Session(app)
    csrf = CSRFProtect(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)  # No URL prefix for auth routes
    app.register_blueprint(main_bp)
    app.register_blueprint(builder_bp)
    app.register_blueprint(respond_bp)
    
    # Add CSRF token to all templates
    @app.context_processor
    def inject_csrf_token():
        from flask_wtf.csrf import generate_csrf
        return dict(csrf_token=generate_csrf)
    
    # Cache control
    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    return app


# Create the application instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# from cs50 import SQL
# from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
# from werkzeug.security import check_password_hash, generate_password_hash
# from helper import  login_required, apology

# from datetime import datetime

# app= Flask(__name__)

# ANSWER_options=["text","radio","checkbox"]

# # Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# # Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///project.db")
# #db.execute("PRAGMA foreign_keys = ON;")

# @app.after_request
# def after_request(response):
#     """Ensure responses aren't cached"""
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# @app.route("/" ,methods = ["GET"])
# @login_required
# def index():
#     db.execute("DELETE FROM forms WHERE name = ? AND title = ? ","","")
#     forms = db.execute("SELECT * FROM forms WHERE user_id = ? ",session["user_id"])
#     return render_template("index.html",forms=forms)

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# @app.route("/register" ,methods = ["GET","POST"])
# def register():
#     if request.method == "GET" :
#         return render_template("register.html")
#     else:
#         user = request.form.get("username")
#         pword = request.form.get("password")
#         conf = request.form.get("confirmation")

#         if not user or not pword or not conf:
#             apology("Must Provid All Data")
#         if pword != conf:
#             return apology("Password And Confirmation Donot Match")

#         usersin = db.execute("SELECT username FROM users")

#         try:
#             db.execute("INSERT INTO users (username,hash) VALUES (?,?)",user, generate_password_hash(pword))
#         except ValueError:
#             return apology("Username Already Exists")

#         return redirect("/")
    

# @app.route("/login" ,methods = ["GET","POST"])
# def login():
        
#     session.clear()
#     if request.method == "POST":
#         if not request.form.get("username"):
#             return apology("must provide username", 403)
#         elif not request.form.get("password"):
#             return apology("must provide password", 403)
#         rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
#         if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
#             return apology("invalid username and/or password", 403)
#         session["user_id"] = rows[0]["id"]
#         return redirect("/")
#     else:
#         return render_template("login.html")


# @app.route("/logout" ,methods = ["GET"])################################
# def logout():
#     session.clear()
#     return redirect("/")

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


# @app.route("/create" ,methods = ["GET","POST"])
# @login_required
# def create():
#     if "form_id" not in session or not db.execute("SELECT * FROM forms WHERE name=? AND title=? AND user_id=? ","","",session["user_id"]):
#         session["form_id"] = 0
#     if request.method == "GET" :
#         if request.args.get("form_id"):
#             session["form_id"]=request.args.get("from_id")
#             print(f"A-{session['form_id']}")
#         if session["form_id"] == 0 :    
#             print(f"B-{session['form_id']}")
#             db.execute("INSERT INTO forms (name,title,user_id) VALUES (?,?,?)","","",session["user_id"])
#             form=db.execute("SELECT * FROM forms WHERE name = ? AND title = ? and question_count = ? AND user_id=? ORDER BY form_id DESC LIMIT 1", "","",0,session["user_id"])
#             session["form_id"]=form[0]["form_id"]
#             print(f"C-{session['form_id']}")
#         else:
#             print(f"D-{session['form_id']}")
#             form= db.execute("SELECT * FROM forms WHERE form_id = ?",session["form_id"])
#             print(f"F-{session['form_id']}")
#         print(f"G-{session['form_id']}")
#         saved_options=db.execute("SELECT * FROM options WHERE option != ?","")
#         empty_options=db.execute("SELECT * FROM options WHERE option = ?","")
#         written_questions=db.execute("SELECT * FROM questions WHERE saved = ? AND form_id =?",1,session["form_id"])
#         empty_questions=db.execute("SELECT * FROM questions WHERE saved = ? AND form_id = ? ",0,session["form_id"])
#         return render_template("create.html",form=form ,writtenquestions=written_questions, emptyquestions=empty_questions, savedoptions=saved_options, emptyoptions=empty_options)
#     else:
#         date_time = datetime.now()
#         date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
#         name=request.form.get("name")
#         title=request.form.get("title")
#         form_id=request.form.get("form_id")
#         created_datetime = db.execute("SELECT * FROM forms WHERE form_id = ?",form_id)[0]["datetime_created"]
#         empty_questions=db.execute("SELECT question_id FROM questions WHERE question = ? AND form_id = ?","",form_id)
#         db.execute("DELETE FROM options WHERE q_id IN (?)", empty_questions)
#         db.execute("DELETE FROM questions WHERE saved = ? AND form_id = ? ",0,form_id)
#         if (not name == "") and (not title  == ""):
#             if created_datetime == None:
#                     db.execute("UPDATE forms SET datetime_created = ?  WHERE form_id = ?",date_time ,form_id)  
#             db.execute("UPDATE forms SET name = ? ,title = ? WHERE form_id = ?",name ,title,form_id)
#         else:
#             db.execute("DELETE FROM forms WHERE form_id = ?","",form_id)
#         print(f"H-{session['form_id']}")
#         session["form_id"]= 0
#         print(f"I-{session['form_id']}")
#         return redirect("/")
    
    
    
# @app.route("/delete" ,methods = ["POST"])
# @login_required
# def delete():
#     form_id=request.form.get("form_id")
#     db.execute("DELETE FROM questions WHERE form_id = ?",form_id)
#     db.execute("DELETE FROM forms WHERE form_id = ?",form_id)
#     return redirect("/")


# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# @app.route("/addquestion" ,methods = ["POST"])
# @login_required
# def addquestion():
#     if request.method == "POST":
#         form_id=request.form.get("form_id")
#         question_no=db.execute("SELECT question_count FROM forms WHERE form_id = ?",form_id)
#         q_number=int(question_no[0]["question_count"]) + 1
#         db.execute("UPDATE forms SET question_count = ? WHERE form_id = ?",q_number,form_id )
#         db.execute("INSERT INTO questions (question,answer_type,form_id) VALUES (?,?,?)","" ,"",form_id)
#     return redirect("/create")
    
 
# @app.route("/writequestion" ,methods = ["POST"])
# @login_required
# def writequestion():
#     if request.method == "POST":
#         question=request.form.get("question")
#         answer_type= request.form.get("answer-type")
#         question_id=request.form.get("qid")
#         if answer_type not in ANSWER_options:
#             return redirect("/create")
#         db.execute("UPDATE questions SET question = ? ,answer_type = ?,saved = ? WHERE question_id = ? ",question ,answer_type,1 , question_id)
#     return redirect("/create")
 

# @app.route("/updatequestion" ,methods = ["POST"])
# @login_required
# def updatequestion():
#     if request.method == "POST":
#         question_text=request.form.get("question_text")
#         answer_type= request.form.get("type_")
#         question_id=request.form.get("qid")
#         answer_t=db.execute("SELECT * FROM questions WHERE question_id = ?",question_id)[0]["answer_type"]  
#         if answer_type not in ANSWER_options:
#             return redirect("/create")
#         if answer_type == "text" and answer_t != "text":
#             db.execute("DELETE FROM options WHERE q_id = ?" ,question_id)
#             db.execute("UPDATE questions SET option_count = ? WHERE question_id = ? ", 0, question_id)
#         db.execute("UPDATE questions SET question = ? ,answer_type = ? WHERE question_id = ? ",question_text,answer_type , question_id)     
#     return redirect("/create") 


# @app.route("/editquestion" ,methods = ["POST"])
# @login_required
# def editquestion(): 
#     form_id = request.form.get("form_id")
#     question_id=request.form.get("qid")    
#     db.execute("UPDATE questions set saved = ? WHERE question_id = ?",0 ,question_id)
#     return redirect("/create") 


# @app.route("/deletequestion" ,methods = ["POST"])
# @login_required
# def deletequestion(): 
#     form_id = request.form.get("form_id")
#     question_id=request.form.get("qid")   
#     question_no=db.execute("SELECT question_count FROM forms WHERE form_id = ?",form_id)
#     q_number=question_no[0]["question_count"] - 1
#     db.execute("UPDATE forms SET question_count = ?  WHERE form_id = ?",q_number,form_id ) 
#     db.execute("DELETE FROM options WHERE q_id = ?" ,question_id)
#     db.execute("DELETE FROM questions WHERE question_id = ?" ,question_id)
#     return redirect("/create") 


# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# @app.route("/addoption" ,methods = ["POST"])
# @login_required
# def addoption(): 
#     type=request.form.get("type")
#     question_id=request.form.get("qid")
#     form_id=request.form.get("form_id")
#     option_no=db.execute("SELECT option_count FROM questions WHERE question_id = ?",question_id)
#     opt_number=option_no[0]["option_count"] +1
#     db.execute("UPDATE questions SET option_count = ?,answer_type = ?  WHERE question_id = ?",opt_number,type,question_id )
#     db.execute("INSERT INTO options (option,q_id,form_id) VALUES (?,?,?)" ,"",question_id,form_id)
#     print(f"{type} , {question_id} , {opt_number}")
#     return redirect("/create")


# @app.route("/saveoption" ,methods = ["POST"])
# @login_required
# def saveoption(): 
#     type=request.form.get("type")
#     question_id=request.form.get("qid")
#     text= request.form.get("option")
#     option_id=request.form.get("oid")
#     db.execute("UPDATE options SET option = ? WHERE option_id = ?" ,text,option_id)
#     return redirect("/create")
  

# @app.route("/deleteoption" ,methods = ["POST"])
# @login_required
# def deleteoption(): 
#     question_id=request.form.get("qid")
#     option_id=request.form.get("oid")
#     option_no=db.execute("SELECT option_count FROM questions WHERE question_id = ?",question_id)
#     opt_number=option_no[0]["option_count"] - 1
#     db.execute("UPDATE questions SET option_count = ?  WHERE question_id = ?",opt_number,question_id )
#     db.execute("DELETE FROM options WHERE option_id = ?" ,option_id)
#     return redirect("/create")  


# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


# # @app.route("/addpage" ,methods = ["GET","POST"])
# # @login_required
# # def addpage():
# #     return


# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# @app.route("/respond/<form_id>" ,methods = ["GET","POST"])
# def respond(form_id):
#     form = db.execute("SELECT * FROM forms WHERE form_id = ?",form_id)[0]
#     questions = db.execute("SELECT * FROM questions WHERE form_id = ?",form_id)
#     options=db.execute("SELECT * FROM options")
    
#     if request.method=="GET":
#         return render_template("respond.html" ,form=form, questions=questions, options=options)
#     else:
#         responder_name=request.form.get("name") 
        
#         if responder_name =="":
#             return render_template("respond.html" ,form=form, questions=questions, options=options) 
#         db.execute("INSERT INTO responders (responder_name) VALUES (?)",responder_name) 
#         responder_id=db.execute("SELECT * FROM responders WHERE responder_name = ? ORDER BY responder_id DESC LIMIT 1", responder_name) 
#         session["responder_id"]=responder_id[0]["responder_id"]  
#         for question in questions:
 
#             if question["answer_type"] != "text":
#                 options =  db.execute("SELECT option FROM options WHERE q_id = ? ",question["question_id"])
#                 option_list =[]
#                 answers=[]
#                 for option in options:
#                     option_list.append(option["option"])
#                 if question["answer_type"] == "radio":
#                     answers= request.form.get(f"{question['question_id']}")
#                     if answers not in option_list:
#                         return "One 1111 of the selected options is not in the options list"
#                 elif question["answer_type"] == "checkbox":
#                     answers =request.form.getlist(f"{question['question_id']}")
#                     for answer in answers:
#                         if answer not in option_list:
#                             return "One 2222 of the selected options is not in the options list"
#             if answers=="" or not answers:
#                 return render_template("respond.html" ,form=form, questions=questions, options=options)
#         date_time = datetime.now()
#         date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
#         for question in questions:
#             if question["answer_type"] != "checkbox":
#                 answer= request.form.get(f"{question['question_id']}")
#                 db.execute("INSERT INTO responses (answer,datetime_resp,q_id,form_id,responder_id) VAlUES (?,?,?,?,?)",answer,date_time,question["question_id"],form_id,session["responder_id"])

#             else:
#                 answers =request.form.getlist(f"{question['question_id']}")
#                 Answer =""
#                 for index,answer in enumerate(answers):
#                     Answer+= f"{answer} "
#                     if index != (len(answers)-1):
#                         Answer+= ", "
#                 db.execute("INSERT INTO responses (answer,datetime_resp,q_id,form_id,responder_id) VAlUES (?,?,?,?,?)",Answer,date_time,question["question_id"],form_id,session["responder_id"])

#         responses_no=db.execute("SELECT * FROM forms WHERE form_id = ?",form_id)[0]["responses_no"]
#         responses_no+= 1
#         db.execute("UPDATE forms SET responses_no = ? WHERE form_id = ?",responses_no,form_id)
        
#         return"You have succesfully submitted the form"

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


# @app.route("/responses_statistics/<form_id>" ,methods = ["GET"])
# @login_required
# def responses_statistics(form_id):
#     if request.method == "GET":
#         form=db.execute("SELECT * FROM forms WHERE form_id = ?",form_id)[0]
#         questions=db.execute("SELECT * FROM questions WHERE form_id = ?",form_id)
#         options = db.execute("SELECT * FROM options")
#         responses=db.execute("SELECT * FROM responses JOIN responders ON responses.responder_id = responders.responder_id WHERE form_id = ?",form_id ) 
#         option_answer_count= db.execute("SELECT option,COUNT(response_id) AS count,responses.q_id AS question_id FROM responses JOIN options ON responses.q_id = options.q_id AND answer = option GROUP BY option_id,options.q_id")
#         return render_template("responses.html", form=form,questions=questions,options=options,responses=responses,option_answer_count=option_answer_count)



# # if __name__ == "__main__":
# #     app.run(debug=True)
