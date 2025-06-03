"""
Models for the Forms application using OOP principles.
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# Initialize database connection
db = SQL("sqlite:///project.db")


@dataclass
class User(UserMixin):
    """User model for authentication"""
    id: int
    username: str
    hash: str = None

    @classmethod
    def create(cls, username: str, password: str) -> 'User':
        """Create a new user"""
        try:
            user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username, generate_password_hash(password)
            )
            return cls.get_by_id(user_id)
        except Exception:
            raise ValueError("Username already exists")

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """Get user by ID"""
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        if rows:
            return cls(**rows[0])
        return None

    @classmethod
    def get_by_username(cls, username: str) -> Optional['User']:
        """Get user by username"""
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if rows:
            return cls(**rows[0])
        return None

    @classmethod
    def get_all(cls) -> List['User']:
        """Get all users"""
        rows = db.execute("SELECT * FROM users")
        return [cls(**row) for row in rows]

    def check_password(self, password: str) -> bool:
        """Check if password is correct"""
        return check_password_hash(self.hash, password)

    def get_id(self) -> str:
        """Required by Flask-Login"""
        return str(self.id)

    @property
    def is_authenticated(self) -> bool:
        """Required by Flask-Login"""
        return True

    @property
    def is_active(self) -> bool:
        """Required by Flask-Login"""
        return True

    @property
    def is_anonymous(self) -> bool:
        """Required by Flask-Login"""
        return False


@dataclass
class Form:
    """Form model"""
    form_id: int
    name: str
    title: str
    question_count: int = 0
    datetime_created: str = None
    responses_no: int = 0
    user_id: int = None
    is_public: bool = False
    slug: str = None

    @classmethod
    def create(cls, name: str, title: str, user_id: int) -> 'Form':
        """Create a new form"""
        try:
            # Verify user exists
            user_check = db.execute("SELECT id FROM users WHERE id = ?", user_id)
            if not user_check:
                raise ValueError(f"User with ID {user_id} does not exist")
            
            form_id = db.execute(
                "INSERT INTO forms (name, title, user_id, datetime_created, question_count, responses_no) VALUES (?, ?, ?, ?, ?, ?)",
                name, title, user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, 0
            )
            return cls.get_by_id(form_id)
        except Exception as e:
            print(f"Error creating form: {e}")
            raise e

    @classmethod
    def create_empty(cls, user_id: int) -> 'Form':
        """Create an empty form for building"""
        try:
            # Verify user exists
            user_check = db.execute("SELECT id FROM users WHERE id = ?", user_id)
            if not user_check:
                raise ValueError(f"User with ID {user_id} does not exist")
                
            form_id = db.execute(
                "INSERT INTO forms (name, title, user_id, question_count, responses_no) VALUES (?, ?, ?, ?, ?)",
                "", "", user_id, 0, 0
            )
            return cls.get_by_id(form_id)
        except Exception as e:
            print(f"Error creating empty form: {e}")
            raise e

    @classmethod
    def get_by_id(cls, form_id: int) -> Optional['Form']:
        """Get form by ID"""
        rows = db.execute("SELECT * FROM forms WHERE form_id = ?", form_id)
        if rows:
            return cls(**rows[0])
        return None

    @classmethod
    def get_by_user(cls, user_id: int) -> List['Form']:
        """Get all forms by user"""
        rows = db.execute("SELECT * FROM forms WHERE user_id = ? AND name != '' AND title != ''", user_id)
        return [cls(**row) for row in rows]

    def update(self, name: str = None, title: str = None) -> None:
        """Update form details"""
        if name is not None:
            self.name = name
        if title is not None:
            self.title = title
        
        db.execute(
            "UPDATE forms SET name = ?, title = ?, datetime_created = ? WHERE form_id = ?",
            self.name, self.title, 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S") if not self.datetime_created else self.datetime_created,
            self.form_id
        )

    def delete(self) -> None:
        """Delete form and all associated data"""
        db.execute("DELETE FROM responses WHERE form_id = ?", self.form_id)
        db.execute("DELETE FROM options WHERE form_id = ?", self.form_id)
        db.execute("DELETE FROM questions WHERE form_id = ?", self.form_id)
        db.execute("DELETE FROM forms WHERE form_id = ?", self.form_id)

    def increment_question_count(self) -> None:
        """Increment question count"""
        self.question_count += 1
        db.execute("UPDATE forms SET question_count = ? WHERE form_id = ?", self.question_count, self.form_id)

    def decrement_question_count(self) -> None:
        """Decrement question count"""
        self.question_count = max(0, self.question_count - 1)
        db.execute("UPDATE forms SET question_count = ? WHERE form_id = ?", self.question_count, self.form_id)

    def increment_responses(self) -> None:
        """Increment response count"""
        self.responses_no += 1
        db.execute("UPDATE forms SET responses_no = ? WHERE form_id = ?", self.responses_no, self.form_id)

    def cleanup_empty(self) -> None:
        """Clean up empty questions and options"""
        empty_questions = db.execute("SELECT question_id FROM questions WHERE question = ? AND form_id = ?", "", self.form_id)
        if empty_questions:
            question_ids = [q['question_id'] for q in empty_questions]
            for qid in question_ids:
                db.execute("DELETE FROM options WHERE q_id = ?", qid)
            db.execute("DELETE FROM questions WHERE question = ? AND form_id = ?", "", self.form_id)

    @classmethod
    def cleanup_empty_forms(cls, user_id: int) -> None:
        """Clean up empty forms"""
        db.execute("DELETE FROM forms WHERE name = ? AND title = ? AND user_id = ?", "", "", user_id)


@dataclass
class Question:
    """Question model"""
    question_id: int
    question: str
    answer_type: str
    option_count: int = 0
    form_id: int = None
    saved: bool = False
    sort_order: int = 0

    @classmethod
    def create(cls, form_id: int, question: str = "", answer_type: str = "") -> 'Question':
        """Create a new question"""
        question_id = db.execute(
            "INSERT INTO questions (question, answer_type, form_id, sort_order) VALUES (?, ?, ?, ?)",
            question, answer_type, form_id, 0
        )
        return cls.get_by_id(question_id)

    @classmethod
    def get_by_id(cls, question_id: int) -> Optional['Question']:
        """Get question by ID"""
        rows = db.execute("SELECT * FROM questions WHERE question_id = ?", question_id)
        if rows:
            return cls(**rows[0])
        return None

    @classmethod
    def get_all(cls, form_id: int) -> List['Question']:
        """Get all questions for a form"""
        rows = db.execute("SELECT * FROM questions WHERE form_id = ? ORDER BY sort_order", form_id)
        return [cls(**row) for row in rows]

    @classmethod
    def get_written(cls, form_id: int) -> List['Question']:
        """Get saved/written questions for a form"""
        rows = db.execute("SELECT * FROM questions WHERE form_id = ? AND saved = 1 ORDER BY sort_order", form_id)
        return [cls(**row) for row in rows]

    @classmethod
    def get_empty(cls, form_id: int) -> List['Question']:
        """Get unsaved/empty questions for a form"""
        rows = db.execute("SELECT * FROM questions WHERE form_id = ? AND saved = 0 ORDER BY sort_order", form_id)
        return [cls(**row) for row in rows]

    def update(self, question: str = None, answer_type: str = None, saved: bool = None) -> None:
        """Update question"""
        if question is not None:
            self.question = question
        if answer_type is not None:
            self.answer_type = answer_type
        if saved is not None:
            self.saved = saved

        # If changing to text type, remove all options
        if answer_type == "text" and self.answer_type != "text":
            Option.delete_by_question(self.question_id)
            self.option_count = 0

        db.execute(
            "UPDATE questions SET question = ?, answer_type = ?, saved = ?, option_count = ? WHERE question_id = ?",
            self.question, self.answer_type, self.saved, self.option_count, self.question_id
        )

    def delete(self) -> None:
        """Delete question and all associated options"""
        Option.delete_by_question(self.question_id)
        db.execute("DELETE FROM questions WHERE question_id = ?", self.question_id)

    def increment_option_count(self) -> None:
        """Increment option count"""
        self.option_count += 1
        db.execute("UPDATE questions SET option_count = ? WHERE question_id = ?", self.option_count, self.question_id)

    def decrement_option_count(self) -> None:
        """Decrement option count"""
        self.option_count = max(0, self.option_count - 1)
        db.execute("UPDATE questions SET option_count = ? WHERE question_id = ?", self.option_count, self.question_id)

    def make_editable(self) -> None:
        """Make question editable"""
        self.saved = False
        db.execute("UPDATE questions SET saved = ? WHERE question_id = ?", self.saved, self.question_id)


@dataclass
class Option:
    """Option model"""
    option_id: int
    option: str
    q_id: int
    form_id: int
    sort_order: int = 0

    @classmethod
    def create(cls, q_id: int, form_id: int, option: str = "") -> 'Option':
        """Create a new option"""
        option_id = db.execute(
            "INSERT INTO options (option, q_id, form_id, sort_order) VALUES (?, ?, ?, ?)",
            option, q_id, form_id, 0
        )
        return cls.get_by_id(option_id)

    @classmethod
    def get_by_id(cls, option_id: int) -> Optional['Option']:
        """Get option by ID"""
        rows = db.execute("SELECT * FROM options WHERE option_id = ?", option_id)
        if rows:
            return cls(**rows[0])
        return None

    @classmethod
    def get_by_question(cls, q_id: int) -> List['Option']:
        """Get all options for a question"""
        rows = db.execute("SELECT * FROM options WHERE q_id = ? ORDER BY sort_order", q_id)
        return [cls(**row) for row in rows]

    @classmethod
    def get_saved(cls, form_id: int = None) -> List['Option']:
        """Get saved options (non-empty)"""
        if form_id:
            rows = db.execute("SELECT * FROM options WHERE form_id = ? AND option != ? ORDER BY sort_order", form_id, "")
        else:
            rows = db.execute("SELECT * FROM options WHERE option != ? ORDER BY sort_order", "")
        return [cls(**row) for row in rows]

    @classmethod
    def get_empty(cls, form_id: int = None) -> List['Option']:
        """Get empty options"""
        if form_id:
            rows = db.execute("SELECT * FROM options WHERE form_id = ? AND option = ? ORDER BY sort_order", form_id, "")
        else:
            rows = db.execute("SELECT * FROM options WHERE option = ? ORDER BY sort_order", "")
        return [cls(**row) for row in rows]

    def update(self, option: str) -> None:
        """Update option text"""
        self.option = option
        db.execute("UPDATE options SET option = ? WHERE option_id = ?", self.option, self.option_id)

    def delete(self) -> None:
        """Delete option"""
        db.execute("DELETE FROM options WHERE option_id = ?", self.option_id)

    @classmethod
    def delete_by_question(cls, q_id: int) -> None:
        """Delete all options for a question"""
        db.execute("DELETE FROM options WHERE q_id = ?", q_id)


@dataclass
class Responder:
    """Responder model"""
    responder_id: int
    responder_name: str

    @classmethod
    def create(cls, responder_name: str) -> 'Responder':
        """Create a new responder"""
        responder_id = db.execute(
            "INSERT INTO responders (responder_name) VALUES (?)",
            responder_name
        )
        return cls.get_by_id(responder_id)

    @classmethod
    def get_by_id(cls, responder_id: int) -> Optional['Responder']:
        """Get responder by ID"""
        rows = db.execute("SELECT * FROM responders WHERE responder_id = ?", responder_id)
        if rows:
            return cls(**rows[0])
        return None

    @classmethod
    def get_latest_by_name(cls, responder_name: str) -> Optional['Responder']:
        """Get latest responder by name"""
        rows = db.execute(
            "SELECT * FROM responders WHERE responder_name = ? ORDER BY responder_id DESC LIMIT 1",
            responder_name
        )
        if rows:
            return cls(**rows[0])
        return None


@dataclass
class Response:
    """Response model"""
    response_id: int
    answer: str
    datetime_resp: str
    q_id: int
    form_id: int
    responder_id: int

    @classmethod
    def create(cls, answer: str, q_id: int, form_id: int, responder_id: int) -> 'Response':
        """Create a new response"""
        response_id = db.execute(
            "INSERT INTO responses (answer, datetime_resp, q_id, form_id, responder_id) VALUES (?, ?, ?, ?, ?)",
            answer, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), q_id, form_id, responder_id
        )
        return cls.get_by_id(response_id)

    @classmethod
    def get_by_id(cls, response_id: int) -> Optional['Response']:
        """Get response by ID"""
        rows = db.execute("SELECT * FROM responses WHERE response_id = ?", response_id)
        if rows:
            return cls(**rows[0])
        return None

    @classmethod
    def get_by_form(cls, form_id: int) -> List[Dict[str, Any]]:
        """Get all responses for a form with responder info"""
        rows = db.execute(
            """SELECT r.*, resp.responder_name 
               FROM responses r 
               JOIN responders resp ON r.responder_id = resp.responder_id 
               WHERE r.form_id = ?""",
            form_id
        )
        return rows

    @classmethod
    def get_option_counts(cls, form_id: int) -> List[Dict[str, Any]]:
        """Get option answer counts for statistics"""
        rows = db.execute(
            """SELECT o.option, COUNT(r.response_id) AS count, r.q_id AS question_id 
               FROM responses r 
               JOIN options o ON r.q_id = o.q_id AND r.answer = o.option 
               WHERE r.form_id = ?
               GROUP BY o.option_id, o.q_id""",
            form_id
        )
        return rows

    @classmethod
    def create_bulk(cls, responses_data: List[Dict[str, Any]], form_id: int, responder_id: int) -> None:
        """Create multiple responses at once"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for response_data in responses_data:
            db.execute(
                "INSERT INTO responses (answer, datetime_resp, q_id, form_id, responder_id) VALUES (?, ?, ?, ?, ?)",
                response_data['answer'], current_time, response_data['q_id'], form_id, responder_id
            )
