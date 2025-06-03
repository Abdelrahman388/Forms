# Forms - Modern Google Forms Clone

A sophisticated Flask-based form builder application that allows users to create, manage, and analyze custom forms with real-time statistics and modern UI.

## 🚀 Features

### ✨ Enhanced Features (Recently Added)
- **AJAX-powered interface** - All form operations work without page refreshes
- **Modern Bootstrap 5 UI** - Clean, responsive design with Bootstrap Icons
- **Dark Mode Toggle** - Seamless theme switching with smooth transitions
- **Real-time Charts** - Response statistics powered by Chart.js
- **Flask-Login Authentication** - Secure user management and sessions
- **Flask-WTF Forms** - CSRF protection and form validation
- **Blueprint Architecture** - Clean, modular code organization
- **OOP Models** - Object-oriented database models with class methods

### 📋 Core Features
- **Form Builder** - Create forms with various question types (text, radio, checkbox)
- **Response Collection** - Collect and manage form responses
- **Statistics Dashboard** - View response analytics with interactive charts
- **User Authentication** - Secure login and registration system
- **Response Restrictions** - Limit responses per user if needed

## 🏗️ Architecture

### Modern Flask Application Structure
```
├── application.py          # Flask application factory
├── run.py                 # Application entry point
├── start.ps1              # PowerShell startup script
├── requirements.txt       # Python dependencies
├── models.py              # OOP database models
├── forms.py               # Flask-WTF form classes
├── auth.py                # Authentication blueprint
├── main.py                # Main routes blueprint
├── builder.py             # Form builder blueprint
├── respond.py             # Response handling blueprint
├── helper.py              # Utility functions
├── project.db             # SQLite database
├── static/
│   ├── styles.css         # Enhanced CSS with dark mode
│   └── js/
│       └── main.js        # AJAX functionality & Chart.js
└── templates/
    ├── layout1.html       # Bootstrap 5 base template
    ├── index.html         # Dashboard
    ├── create.html        # Form builder
    ├── respond.html       # Form response interface
    ├── responses.html     # Analytics dashboard
    ├── login.html         # Authentication
    ├── register.html      # User registration
    ├── success.html       # Success confirmation
    ├── 404.html           # Error pages
    └── 500.html
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+ 
- Windows (PowerShell)

### Quick Start
1. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Run Application**
   ```powershell
   .\start.ps1
   ```
   Or manually:
   ```powershell
   python run.py
   ```

3. **Access Application**
   Open your browser to: `http://127.0.0.1:5000`

## 🎨 UI/UX Features

### Bootstrap 5 Integration
- **Responsive Grid System** - Works on all device sizes
- **Modern Cards & Components** - Clean, professional interface
- **Floating Labels** - Enhanced form experience
- **Toast Notifications** - Real-time user feedback

### Dark Mode Support
- **CSS Custom Properties** - Efficient theme switching
- **Smooth Transitions** - Polished user experience
- **Persistent Theme** - Remembers user preference

### Interactive Elements
- **AJAX Form Handling** - No page refreshes needed
- **Real-time Validation** - Instant feedback on form inputs
- **Dynamic Question Management** - Add/edit/delete questions seamlessly
- **Chart.js Integration** - Beautiful response statistics

## 📊 Technical Improvements

### Security Enhancements
- **CSRF Protection** - Flask-WTF integration
- **Secure Sessions** - Flask-Login user management  
- **Input Validation** - Server-side form validation
- **SQL Injection Prevention** - CS50 SQL wrapper

### Performance Optimizations
- **Modular JavaScript** - Organized, maintainable code
- **CSS Custom Properties** - Efficient styling system
- **Blueprint Architecture** - Scalable Flask structure
- **Database Optimization** - Efficient queries and relationships

### Developer Experience
- **Error Handling** - Comprehensive error pages and JSON responses
- **Code Organization** - Clean separation of concerns
- **Documentation** - Well-commented code and README
- **Debugging Support** - Flask debug mode with detailed error messages

## 🔧 Usage

### Creating Forms
1. **Register/Login** to your account
2. **Click "Create New Form"** on the dashboard
3. **Add Questions** using the form builder interface
4. **Configure Settings** (response restrictions, etc.)
5. **Save and Share** your form

### Managing Responses
1. **View Forms** on your dashboard
2. **Click "View Responses"** for analytics
3. **See Charts** showing response distribution
4. **Export Data** (if needed)

### Theme Switching
- **Click the moon/sun icon** in the navigation bar
- **Theme persists** across page refreshes and sessions

## 🚀 Future Enhancements

- [ ] **Form Templates** - Pre-built form templates
- [ ] **File Uploads** - Support for file upload questions
- [ ] **Email Notifications** - Response notifications
- [ ] **Advanced Analytics** - More detailed statistics
- [ ] **Export Options** - CSV, PDF export functionality
- [ ] **Form Sharing** - Public form links and embedding
- [ ] **Conditional Logic** - Show/hide questions based on responses

## 📝 License

This project is part of CS50x coursework and follows academic integrity guidelines.

---

**Built with ❤️ using Flask, Bootstrap 5, and modern web technologies**
