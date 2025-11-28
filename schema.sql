-- Email Marketing Lists and Employee Management Database Schema
-- Created for managing newsletter subscriptions and company employees

-- Departments Table
-- Each department has 1 head of department
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    head_of_department_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (head_of_department_id) REFERENCES employees(id)
);

-- Employees Table
-- Employees can be supervisors or heads of department
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department_id INTEGER NOT NULL,
    is_supervisor BOOLEAN DEFAULT 0,
    is_head BOOLEAN DEFAULT 0,
    position TEXT,
    hire_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
);

-- Email Subscriptions Table
-- All newsletter subscriptions from the company website
CREATE TABLE IF NOT EXISTS email_subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'unsubscribed', 'bounced')),
    source TEXT,
    notes TEXT
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department_id);
CREATE INDEX IF NOT EXISTS idx_employees_supervisor ON employees(is_supervisor);
CREATE INDEX IF NOT EXISTS idx_email_subscriptions_status ON email_subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_email_subscriptions_email ON email_subscriptions(email);

-- Insert sample data for testing
-- First, create some departments
INSERT OR IGNORE INTO departments (id, name) VALUES 
    (1, 'Marketing'),
    (2, 'Sales'),
    (3, 'IT');

-- Insert sample employees (we'll update head_of_department after employees are created)
INSERT OR IGNORE INTO employees (id, name, email, department_id, is_supervisor, is_head, position, hire_date) VALUES
    (1, 'John Smith', 'john.smith@company.com', 1, 1, 1, 'Head of Marketing', '2020-01-15'),
    (2, 'Jane Doe', 'jane.doe@company.com', 1, 1, 0, 'Marketing Supervisor', '2021-03-20'),
    (3, 'Bob Johnson', 'bob.johnson@company.com', 2, 1, 1, 'Head of Sales', '2019-06-10'),
    (4, 'Alice Williams', 'alice.williams@company.com', 2, 1, 0, 'Sales Supervisor', '2020-09-05'),
    (5, 'Charlie Brown', 'charlie.brown@company.com', 3, 1, 1, 'Head of IT', '2018-11-12'),
    (6, 'Diana Prince', 'diana.prince@company.com', 3, 1, 0, 'IT Supervisor', '2021-07-18');

-- Update departments with head_of_department_id
UPDATE departments SET head_of_department_id = 1 WHERE id = 1;
UPDATE departments SET head_of_department_id = 3 WHERE id = 2;
UPDATE departments SET head_of_department_id = 5 WHERE id = 3;

-- Insert sample email subscriptions
INSERT OR IGNORE INTO email_subscriptions (email, status, source) VALUES
    ('customer1@example.com', 'active', 'website'),
    ('customer2@example.com', 'active', 'website'),
    ('customer3@example.com', 'active', 'newsletter'),
    ('customer4@example.com', 'unsubscribed', 'website'),
    ('customer5@example.com', 'active', 'social_media');

