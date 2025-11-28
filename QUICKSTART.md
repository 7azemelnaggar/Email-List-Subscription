# Quick Start Guide

## Running the Application

### GUI Application (Recommended)
```bash
python gui_app.py
```

This opens a graphical interface with 4 tabs:
- **Departments**: Manage company departments
- **Employees**: Manage employee records
- **Email Subscriptions**: Manage newsletter subscriptions
- **Export/Import**: Export email lists to CSV/Excel or import from CSV

### Command Line Interface
```bash
python cli_app.py
```

Interactive menu-driven interface for all operations.

## Testing

Run the test script to verify everything works:
```bash
python test_database.py
```

## Key Features

✅ **Database Schema**
- Departments table (with head of department)
- Employees table (with supervisors)
- Email subscriptions table

✅ **CRUD Operations**
- Full Create, Read, Update, Delete for all tables
- Available via GUI, CLI, or Python API

✅ **Export Functionality**
- Export email list to CSV
- Export email list to Excel (.xlsx)
- Filter by status (active, unsubscribed, bounced)

✅ **Import Functionality** (Bonus)
- Import email subscriptions from CSV
- Automatic duplicate detection
- Error handling and reporting

## Sample Data

The database comes pre-loaded with:
- 3 departments (Marketing, Sales, IT)
- 6 employees (including supervisors and heads)
- 5 sample email subscriptions

## Database File

The application creates `email_marketing.db` in the project directory. This SQLite database file contains all your data.

