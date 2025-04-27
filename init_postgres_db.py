import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def init_db():
    # Get database URL from environment or use default
    database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:8503@localhost:5432/todo_app')
    
    # If using Heroku, adjust the URL format if needed
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Create a minimal Flask application
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy and Migrations
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    
    # Import models to ensure they're registered with SQLAlchemy
    from app import User, Todo
    
    # Create tables
    with app.app_context():
        db.create_all()
        print("PostgreSQL database tables created successfully!")

if __name__ == "__main__":
    init_db() 