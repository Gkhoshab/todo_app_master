# Task Master Todo App

A feature-rich Flask-based todo application with user authentication, email reminders, and PostgreSQL database integration.

## Features

- User registration and authentication
- Create, read, update, and delete todo items
- Set priorities and due dates for tasks
- Email reminders for upcoming tasks
- PostgreSQL database for data persistence
- Responsive design for mobile and desktop use

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database server
- SMTP access for email functionality (Gmail account recommended)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Gkhoshab/todo_app_master.git
cd todo_app_master
```

### 2. Create a virtual environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file and update it with your settings:

```bash
cp .env.example .env
```

Edit the `.env` file and update the following:

- `DATABASE_URL`: Set your PostgreSQL database credentials
- `MAIL_USERNAME`: Your email address (Gmail recommended)
- `MAIL_PASSWORD`: Your app password for Gmail (see note below)
- `MAIL_DEFAULT_SENDER`: Your email address for sending reminders
- `SECRET_KEY`: A secure random string for session encryption

**Note on Gmail App Passwords**: 
If you're using Gmail, you'll need to create an App Password. See `EMAIL_SETUP.md` for detailed instructions.

### 5. Set up PostgreSQL

Make sure PostgreSQL is installed and running. Then create a new database:

```bash
# Log into PostgreSQL
psql -U postgres

# In PostgreSQL command line, create the database
CREATE DATABASE todo_app;
\q
```

### 6. Initialize the database

```bash
# Run the database initialization script
python init_postgres_db.py

# Run migrations
flask db upgrade
```

## Running the Application

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000/`

## Database Migration

If you want to migrate from SQLite to PostgreSQL or need to perform database migrations, see `POSTGRESQL_MIGRATION.md` for detailed instructions.

## Email Reminders

The application includes an automatic reminder system that will send emails for tasks with reminder dates. Make sure your email configuration is correct in the `.env` file.

See `EMAIL_SETUP.md` for detailed instructions on setting up email functionality.

## Project Structure

```
todo_app_master/
├── app.py                 # Main application file
├── static/                # Static assets (CSS, JS, images)
├── templates/             # HTML templates
├── migrations/            # Database migrations
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Troubleshooting

### Database Connection Issues

If you encounter database connection issues:

1. Verify PostgreSQL is running
2. Check your database credentials in the `.env` file
3. Ensure the database exists
4. Check network connectivity if using a remote database

### Email Sending Issues

If emails are not being sent:

1. Verify your email credentials in the `.env` file
2. Make sure you're using an App Password if using Gmail
3. Check your network connectivity
4. Review the application logs for any error messages

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

- Flask framework
- Bootstrap for UI
- Font Awesome for icons 