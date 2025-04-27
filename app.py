#CSE 412 DATABASE PROJECT
#TASK MASTER
#GROUP 30
#TEAM MEMBERS:
#1. Giovanni Khoshaba
#2. Andrew Ramirez
#3. Sebastian Deras
#4.Tinh Nhi Nguyen
#4/26/2025


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message  # New: for sending emails
from apscheduler.schedulers.background import BackgroundScheduler  # New: for background scheduling
import atexit
from flask_migrate import Migrate



# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_testing')
# Update database configuration for PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:8503@localhost:5432/todo_app')
# If the DATABASE_URL from environment starts with 'postgres://', update it to 'postgresql://' for SQLAlchemy 1.4+
db_url = app.config['SQLALCHEMY_DATABASE_URI']
if db_url.startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') 
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', 'yes', '1', 't')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() in ('true', 'yes', '1', 't')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])
mail = Mail(app)

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    todos = db.relationship('Todo', backref='owner', lazy=True, cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=1)  # 1=Low, 2=Medium, 3=High
    # New fields for reminder functionality:
    reminder_time = db.Column(db.DateTime, nullable=True)
    reminder_sent = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Todo {self.title}>'

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_now():
    return {'now': lambda: datetime.utcnow()}

# Function to send an email reminder for a Todo task
def send_reminder_email(todo):
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        print("Email configuration incomplete. Please set MAIL_USERNAME and MAIL_PASSWORD environment variables.")
        return False
    
    try:
        user = todo.owner
        
        # Format dates nicely if available
        due_date_str = "Not set"
        if todo.due_date:
            due_date_str = todo.due_date.strftime("%Y-%m-%d %I:%M %p")
            
        reminder_time_str = "Not set" 
        if todo.reminder_time:
            reminder_time_str = todo.reminder_time.strftime("%Y-%m-%d %I:%M %p")
        
        msg = Message(f"Task Master - Reminder: {todo.title}",
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    recipients=[user.email])
        
        msg.body = (f"Hello {user.username},\n\n"
                    f"This is a reminder for your task:\n\n"
                    f"Title: {todo.title}\n"
                    f"Description: {todo.description or 'No description'}\n"
                    f"Due Date: {due_date_str}\n"
                    f"Reminder set for: {reminder_time_str}\n\n"
                    f"Visit Task Master to manage your tasks.\n\n" + "http://192.168.0.252:5002\n"
                    f"Thank you!")
        
        mail.send(msg)
        print(f"Email sent successfully to {user.email} for todo: {todo.title}")
        return True
    except Exception as e:
        print(f"Error sending email for todo {todo.id}: {str(e)}")
        return False

# Background job to check for due reminders
def check_reminders():
    try:
        with app.app_context():
            now = datetime.utcnow()
            print(f"Checking for due reminders at {now}")
            
            # Find todos with a reminder time that has passed and not yet sent
            todos = Todo.query.filter(
                Todo.reminder_time != None,
                Todo.reminder_time <= now,
                Todo.reminder_sent == False
            ).all()
            
            if not todos:
                print("No due reminders found")
                return
                
            print(f"Found {len(todos)} due reminders to send")
            
            for todo in todos:
                try:
                    if send_reminder_email(todo):
                        todo.reminder_sent = True  # mark as sent to avoid duplicate emails
                        db.session.commit()
                        print(f"Marked reminder for todo {todo.id} as sent")
                    else:
                        print(f"Failed to send reminder for todo {todo.id}")
                except Exception as e:
                    print(f"Error processing reminder for todo {todo.id}: {str(e)}")
    except Exception as e:
        print(f"Error in check_reminders job: {str(e)}")

# Set up APScheduler to run the reminder check every 60 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_reminders, trigger="interval", seconds=60)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if username or email already exists
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Username or email already exists', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
            
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard'))
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    todos = Todo.query.filter_by(user_id=current_user.id).order_by(
        Todo.completed, Todo.priority.desc(), Todo.due_date
    ).all()
    return render_template('dashboard.html', todos=todos)

# CRUD operations for Todos
@app.route('/todo/new', methods=['GET', 'POST'])
@login_required
def new_todo():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        priority = int(request.form.get('priority', 1))
        
        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        
        if not title:
            flash('Title is required', 'danger')
            return redirect(url_for('new_todo'))
            
        todo = Todo(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            user_id=current_user.id
        )
        
        db.session.add(todo)
        db.session.commit()
        
        flash('Todo created successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('todo_form.html', todo=None)

@app.route('/todo/<int:todo_id>')
@login_required
def view_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    return render_template('todo_details.html', todo=todo)

@app.route('/todo/<int:todo_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        priority = int(request.form.get('priority', 1))
        completed = 'completed' in request.form
        
        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        
        if not title:
            flash('Title is required', 'danger')
            return redirect(url_for('edit_todo', todo_id=todo.id))
            
        todo.title = title
        todo.description = description
        todo.due_date = due_date
        todo.priority = priority
        todo.completed = completed
        
        db.session.commit()
        
        flash('Todo updated successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('todo_form.html', todo=todo)

@app.route('/todo/<int:todo_id>/delete', methods=['POST'])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    
    db.session.delete(todo)
    db.session.commit()
    
    flash('Todo deleted successfully!', 'info')
    return redirect(url_for('dashboard'))

@app.route('/todo/<int:todo_id>/toggle', methods=['POST'])
@login_required
def toggle_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    
    todo.completed = not todo.completed
    db.session.commit()
    
    return redirect(url_for('dashboard'))

# New Route: Set a reminder for a specific Todo
@app.route('/todo/<int:todo_id>/set_reminder', methods=['GET', 'POST'])
@login_required
def set_reminder(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    
    # For sent reminders, only save the "sent" status but don't clear the time immediately
    # This way we can still display when the reminder was sent
    if request.method == 'GET' and todo.reminder_sent:
        flash('A reminder has already been sent for this task. You can set a new one.', 'info')
    
    if request.method == 'POST':
        reminder_time_str = request.form.get('reminder_time')
        if reminder_time_str:
            try:
                # Expecting format 'YYYY-MM-DDTHH:MM' from a datetime-local input
                reminder_time = datetime.strptime(reminder_time_str, '%Y-%m-%dT%H:%M')
                todo.reminder_time = reminder_time
                todo.reminder_sent = False  # reset flag if user updates the reminder
                db.session.commit()
                flash('Reminder set successfully!', 'success')
            except Exception as e:
                flash('Invalid date format. Please try again.', 'danger')
        else:
            flash('Please provide a reminder time.', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('set_reminder.html', todo=todo)

@app.route('/todo/<int:todo_id>/delete_reminder', methods=['POST'])
@login_required
def delete_reminder(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    todo.reminder_time = None
    todo.reminder_sent = False
    db.session.commit()
    flash('Reminder deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# API routes for potential future front-end frameworks
@app.route('/api/todos', methods=['GET'])
@login_required
def api_get_todos():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return {
        'todos': [
            {
                'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'created_at': todo.created_at.isoformat(),
                'due_date': todo.due_date.isoformat() if todo.due_date else None,
                'completed': todo.completed,
                'priority': todo.priority,
                'reminder_time': todo.reminder_time.isoformat() if todo.reminder_time else None,
                'reminder_sent': todo.reminder_sent
            } for todo in todos
        ]
    }

@app.route('/api/todos', methods=['POST'])
@login_required
def api_create_todo():
    data = request.json
    
    todo = Todo(
        title=data.get('title'),
        description=data.get('description'),
        due_date=datetime.fromisoformat(data.get('due_date')) if data.get('due_date') else None,
        priority=data.get('priority', 1),
        user_id=current_user.id
    )
    
    db.session.add(todo)
    db.session.commit()
    
    return {
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'created_at': todo.created_at.isoformat(),
        'due_date': todo.due_date.isoformat() if todo.due_date else None,
        'completed': todo.completed,
        'priority': todo.priority
    }

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
@login_required
def api_update_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    data = request.json
    
    if 'title' in data:
        todo.title = data['title']
    if 'description' in data:
        todo.description = data['description']
    if 'due_date' in data:
        todo.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
    if 'priority' in data:
        todo.priority = data['priority']
    if 'completed' in data:
        todo.completed = data['completed']
    
    db.session.commit()
    
    return {
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'created_at': todo.created_at.isoformat(),
        'due_date': todo.due_date.isoformat() if todo.due_date else None,
        'completed': todo.completed,
        'priority': todo.priority
    }

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@login_required
def api_delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    
    db.session.delete(todo)
    db.session.commit()
    
    return {'message': 'Todo deleted successfully'}

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Test route for email functionality
@app.route('/test-email')
@login_required
def test_email():
    try:
        now = datetime.utcnow()
        msg = Message(
            subject="Task Master - Test Email",
            recipients=[current_user.email],
            body=f"Hello {current_user.username},\n\n"
                 f"This is a test email from Task Master to verify email functionality is working correctly.\n\n"
                 f"Time sent: {now.strftime('%Y-%m-%d %I:%M %p')}\n\n"
                 f"Regards,\nTask Master Team",
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
        flash('Test email sent successfully! Please check your inbox.', 'success')
    except Exception as e:
        flash(f'Error sending test email: {str(e)}', 'danger')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True, host = "0.0.0.0", port = 5002)
