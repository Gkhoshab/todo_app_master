import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def setup_postgres_db(dbname, user, password, host='localhost', port=5432):
    """Create PostgreSQL database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database {dbname}")
            cursor.execute(f"CREATE DATABASE {dbname}")
            print(f"Database {dbname} created successfully")
        else:
            print(f"Database {dbname} already exists")
            
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

def migrate_data(sqlite_path, pg_conn_string):
    """Migrate data from SQLite to PostgreSQL"""
    try:
        # Create Flask app context for SQLAlchemy
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = pg_conn_string
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Initialize database with this app
        db = SQLAlchemy(app)
        
        # Define models within this context
        class User(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(64), index=True, unique=True)
            email = db.Column(db.String(120), index=True, unique=True)
            password_hash = db.Column(db.String(128))
            todos = db.relationship('Todo', backref='owner', lazy='dynamic')
            
        class Todo(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            title = db.Column(db.String(100), nullable=False)
            description = db.Column(db.Text, nullable=True)
            created_at = db.Column(db.DateTime, nullable=False)
            due_date = db.Column(db.DateTime, nullable=True)
            completed = db.Column(db.Boolean, default=False)
            priority = db.Column(db.Integer, default=1)
            reminder_time = db.Column(db.DateTime, nullable=True)
            reminder_sent = db.Column(db.Boolean, default=False)
            user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
            
        with app.app_context():
            # Initialize database schema in PostgreSQL
            db.create_all()
            
            # Connect to SQLite database
            sqlite_conn = sqlite3.connect(sqlite_path)
            sqlite_conn.row_factory = sqlite3.Row
            sqlite_cursor = sqlite_conn.cursor()
            
            # Migrate Users
            print("Migrating users...")
            sqlite_cursor.execute("SELECT * FROM user")
            users = sqlite_cursor.fetchall()
            
            for user_row in users:
                user = User(
                    id=user_row['id'],
                    username=user_row['username'],
                    email=user_row['email'],
                    password_hash=user_row['password_hash']
                )
                db.session.add(user)
            
            # Commit users to ensure they exist before adding todos
            db.session.commit()
            print(f"Migrated {len(users)} users")
            
            # Migrate Todos
            print("Migrating todos...")
            sqlite_cursor.execute("SELECT * FROM todo")
            todos = sqlite_cursor.fetchall()
            
            for todo_row in todos:
                todo = Todo(
                    id=todo_row['id'],
                    title=todo_row['title'],
                    description=todo_row['description'],
                    created_at=todo_row['created_at'],
                    due_date=todo_row['due_date'],
                    completed=bool(todo_row['completed']),
                    priority=todo_row['priority'],
                    reminder_time=todo_row['reminder_time'],
                    reminder_sent=bool(todo_row['reminder_sent']),
                    user_id=todo_row['user_id']
                )
                db.session.add(todo)
            
            db.session.commit()
            print(f"Migrated {len(todos)} todos")
            
            sqlite_conn.close()
            
        return True
    except Exception as e:
        print(f"Error migrating data: {e}")
        return False

if __name__ == "__main__":
    # Default paths and credentials
    sqlite_path = "instance/todos.db"
    pg_dbname = "todo_app"
    pg_user = "postgres"
    pg_password = "8503"
    pg_host = "localhost"
    pg_port = "5432"
    
    # Allow command-line overrides
    if len(sys.argv) > 1:
        sqlite_path = sys.argv[1]
    if len(sys.argv) > 2:
        pg_dbname = sys.argv[2]
    if len(sys.argv) > 3:
        pg_user = sys.argv[3]
    if len(sys.argv) > 4:
        pg_password = sys.argv[4]
    if len(sys.argv) > 5:
        pg_host = sys.argv[5]
    if len(sys.argv) > 6:
        pg_port = sys.argv[6]
    
    print(f"Setting up PostgreSQL database {pg_dbname}...")
    if setup_postgres_db(pg_dbname, pg_user, pg_password, pg_host, int(pg_port)):
        pg_conn_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_dbname}"
        print(f"Migrating data from {sqlite_path} to PostgreSQL...")
        if migrate_data(sqlite_path, pg_conn_string):
            print("Migration completed successfully!")
        else:
            print("Migration failed.")
    else:
        print("Failed to set up PostgreSQL database.") 