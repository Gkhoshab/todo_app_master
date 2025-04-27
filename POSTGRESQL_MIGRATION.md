# Migrating Todo App from SQLite to PostgreSQL

This document provides step-by-step instructions for migrating the Todo application from SQLite to PostgreSQL.

## Prerequisites

1. **Install PostgreSQL**: Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/) or use a package manager.

2. **Create a PostgreSQL Database**: Create a database for the Todo app:
   ```bash
   psql -U postgres
   CREATE DATABASE todo_app;
   \q
   ```

3. **Install Requirements**: Make sure you have all required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Migration Steps

### 1. Update Environment Variables (Recommended)

Create a `.env` file in the project root with your database connection details:

```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
```

Replace `username` and `password` with your PostgreSQL credentials.

### 2. Initialize PostgreSQL Database

Run the initialization script to create the database tables:

```bash
python init_postgres_db.py
```

### 3. Migrate Data from SQLite to PostgreSQL

If you have existing data in SQLite that you want to migrate, run:

```bash
python migrate_to_postgres.py
```

You can provide custom paths and credentials as arguments:

```bash
python migrate_to_postgres.py path/to/sqlite.db dbname username password host port
```

### 4. Verify Migration

1. Start your application:
   ```bash
   python app.py
   ```

2. Log in with an existing account to verify that your data was migrated successfully.

## Troubleshooting

### Database Connection Issues

If you encounter connection issues, check:
- PostgreSQL service is running
- Database credentials are correct
- Database exists
- Firewall settings are allowing connections to PostgreSQL

### Data Migration Issues

If data migration fails:
- Check your SQLite database path
- Ensure you have proper permissions to read the SQLite database
- Verify PostgreSQL connection details

### Schema Issues

If you encounter schema issues:
- Use Flask-Migrate to handle schema changes:
  ```bash
  flask db init  # Only if migrations folder doesn't exist
  flask db migrate -m "migrate to postgresql"
  flask db upgrade
  ```

## Production Deployment

For production environments:

1. Set a secure PostgreSQL password
2. Configure SSL for database connections
3. Limit database access to application servers only
4. Set up regular database backups 