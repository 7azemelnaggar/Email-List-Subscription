"""
GUI Application for Email Marketing Lists and Employee Management
Built with tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import DatabaseManager
from datetime import datetime
import os


class EmailMarketingApp:
    """Main GUI application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Email Marketing & Employee Management System")
        self.root.geometry("1200x700")
        
        # Initialize database
        self.db = DatabaseManager()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_departments_tab()
        self.create_employees_tab()
        self.create_emails_tab()
        self.create_export_tab()
        
        # Status bar
        self.status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    # ==================== DEPARTMENTS TAB ====================
    
    def create_departments_tab(self):
        """Create departments management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Departments")
        
        # Left panel - Form
        left_panel = ttk.LabelFrame(frame, text="Department Information", padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        
        ttk.Label(left_panel, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.dept_name_entry = ttk.Entry(left_panel, width=30)
        self.dept_name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(left_panel, text="Head of Department:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dept_head_combo = ttk.Combobox(left_panel, width=27, state="readonly")
        self.dept_head_combo.grid(row=1, column=1, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(left_panel)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add", command=self.add_department).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_department).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_department).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_department_form).pack(side=tk.LEFT, padx=5)
        
        # Right panel - List
        right_panel = ttk.LabelFrame(frame, text="Departments List", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview
        columns = ("ID", "Name", "Head of Department")
        self.dept_tree = ttk.Treeview(right_panel, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.dept_tree.heading(col, text=col)
            self.dept_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.dept_tree.yview)
        self.dept_tree.configure(yscrollcommand=scrollbar.set)
        
        self.dept_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.dept_tree.bind("<Double-1>", self.on_department_select)
        
        ttk.Button(right_panel, text="Refresh", command=self.refresh_departments).pack(pady=5)
        
        self.refresh_departments()
    
    def refresh_departments(self):
        """Refresh departments list"""
        # Clear tree
        for item in self.dept_tree.get_children():
            self.dept_tree.delete(item)
        
        # Load departments
        departments = self.db.get_all_departments()
        employees = self.db.get_all_employees()
        employee_dict = {emp['id']: emp['name'] for emp in employees}
        
        for dept in departments:
            head_name = employee_dict.get(dept['head_of_department_id'], 'N/A')
            self.dept_tree.insert("", tk.END, values=(
                dept['id'], dept['name'], head_name
            ))
        
        # Update head combo
        self.dept_head_combo['values'] = [f"{emp['id']} - {emp['name']}" for emp in employees]
    
    def on_department_select(self, event):
        """Handle department selection"""
        selection = self.dept_tree.selection()
        if selection:
            item = self.dept_tree.item(selection[0])
            dept_id = item['values'][0]
            dept = self.db.get_department(dept_id)
            if dept:
                self.dept_name_entry.delete(0, tk.END)
                self.dept_name_entry.insert(0, dept['name'])
                if dept['head_of_department_id']:
                    self.dept_head_combo.set(f"{dept['head_of_department_id']} - {self.db.get_employee(dept['head_of_department_id'])['name']}")
                self.current_dept_id = dept_id
    
    def add_department(self):
        """Add new department"""
        name = self.dept_name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Department name is required")
            return
        
        head_str = self.dept_head_combo.get()
        head_id = None
        if head_str:
            head_id = int(head_str.split(' - ')[0])
        
        try:
            self.db.create_department(name, head_id)
            messagebox.showinfo("Success", "Department added successfully")
            self.clear_department_form()
            self.refresh_departments()
            self.update_status("Department added")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add department: {e}")
    
    def update_department(self):
        """Update selected department"""
        if not hasattr(self, 'current_dept_id'):
            messagebox.showerror("Error", "Please select a department to update")
            return
        
        name = self.dept_name_entry.get().strip()
        head_str = self.dept_head_combo.get()
        head_id = None
        if head_str:
            head_id = int(head_str.split(' - ')[0])
        
        try:
            self.db.update_department(self.current_dept_id, name, head_id)
            messagebox.showinfo("Success", "Department updated successfully")
            self.clear_department_form()
            self.refresh_departments()
            self.update_status("Department updated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update department: {e}")
    
    def delete_department(self):
        """Delete selected department"""
        if not hasattr(self, 'current_dept_id'):
            messagebox.showerror("Error", "Please select a department to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this department?"):
            try:
                self.db.delete_department(self.current_dept_id)
                messagebox.showinfo("Success", "Department deleted successfully")
                self.clear_department_form()
                self.refresh_departments()
                self.update_status("Department deleted")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete department: {e}")
    
    def clear_department_form(self):
        """Clear department form"""
        self.dept_name_entry.delete(0, tk.END)
        self.dept_head_combo.set('')
        if hasattr(self, 'current_dept_id'):
            delattr(self, 'current_dept_id')
    
    # ==================== EMPLOYEES TAB ====================
    
    def create_employees_tab(self):
        """Create employees management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Employees")
        
        # Left panel - Form
        left_panel = ttk.LabelFrame(frame, text="Employee Information", padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        
        ttk.Label(left_panel, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.emp_name_entry = ttk.Entry(left_panel, width=30)
        self.emp_name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(left_panel, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.emp_email_entry = ttk.Entry(left_panel, width=30)
        self.emp_email_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(left_panel, text="Department:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.emp_dept_combo = ttk.Combobox(left_panel, width=27, state="readonly")
        self.emp_dept_combo.grid(row=2, column=1, pady=5)
        
        ttk.Label(left_panel, text="Position:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.emp_position_entry = ttk.Entry(left_panel, width=30)
        self.emp_position_entry.grid(row=3, column=1, pady=5)
        
        ttk.Label(left_panel, text="Hire Date (YYYY-MM-DD):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.emp_hire_date_entry = ttk.Entry(left_panel, width=30)
        self.emp_hire_date_entry.grid(row=4, column=1, pady=5)
        
        self.emp_supervisor_var = tk.BooleanVar()
        ttk.Checkbutton(left_panel, text="Is Supervisor", variable=self.emp_supervisor_var).grid(row=5, column=0, columnspan=2, pady=5)
        
        self.emp_head_var = tk.BooleanVar()
        ttk.Checkbutton(left_panel, text="Is Head of Department", variable=self.emp_head_var).grid(row=6, column=0, columnspan=2, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(left_panel)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add", command=self.add_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_employee_form).pack(side=tk.LEFT, padx=5)
        
        # Right panel - List
        right_panel = ttk.LabelFrame(frame, text="Employees List", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview
        columns = ("ID", "Name", "Email", "Department", "Position", "Supervisor", "Head")
        self.emp_tree = ttk.Treeview(right_panel, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.emp_tree.heading(col, text=col)
            self.emp_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.emp_tree.yview)
        self.emp_tree.configure(yscrollcommand=scrollbar.set)
        
        self.emp_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.emp_tree.bind("<Double-1>", self.on_employee_select)
        
        ttk.Button(right_panel, text="Refresh", command=self.refresh_employees).pack(pady=5)
        
        self.refresh_employees()
    
    def refresh_employees(self):
        """Refresh employees list"""
        # Clear tree
        for item in self.emp_tree.get_children():
            self.emp_tree.delete(item)
        
        # Load employees
        employees = self.db.get_all_employees()
        for emp in employees:
            self.emp_tree.insert("", tk.END, values=(
                emp['id'], emp['name'], emp['email'], 
                emp.get('department_name', 'N/A'), emp.get('position', ''),
                'Yes' if emp['is_supervisor'] else 'No',
                'Yes' if emp['is_head'] else 'No'
            ))
        
        # Update department combo
        departments = self.db.get_all_departments()
        self.emp_dept_combo['values'] = [f"{dept['id']} - {dept['name']}" for dept in departments]
    
    def on_employee_select(self, event):
        """Handle employee selection"""
        selection = self.emp_tree.selection()
        if selection:
            item = self.emp_tree.item(selection[0])
            emp_id = item['values'][0]
            emp = self.db.get_employee(emp_id)
            if emp:
                self.emp_name_entry.delete(0, tk.END)
                self.emp_name_entry.insert(0, emp['name'])
                self.emp_email_entry.delete(0, tk.END)
                self.emp_email_entry.insert(0, emp['email'])
                dept = self.db.get_department(emp['department_id'])
                if dept:
                    self.emp_dept_combo.set(f"{dept['id']} - {dept['name']}")
                self.emp_position_entry.delete(0, tk.END)
                if emp.get('position'):
                    self.emp_position_entry.insert(0, emp['position'])
                if emp.get('hire_date'):
                    self.emp_hire_date_entry.delete(0, tk.END)
                    self.emp_hire_date_entry.insert(0, emp['hire_date'])
                self.emp_supervisor_var.set(bool(emp['is_supervisor']))
                self.emp_head_var.set(bool(emp['is_head']))
                self.current_emp_id = emp_id
    
    def add_employee(self):
        """Add new employee"""
        name = self.emp_name_entry.get().strip()
        email = self.emp_email_entry.get().strip()
        dept_str = self.emp_dept_combo.get()
        
        if not name or not email or not dept_str:
            messagebox.showerror("Error", "Name, email, and department are required")
            return
        
        dept_id = int(dept_str.split(' - ')[0])
        position = self.emp_position_entry.get().strip() or None
        hire_date = self.emp_hire_date_entry.get().strip() or None
        
        try:
            self.db.create_employee(
                name, email, dept_id,
                self.emp_supervisor_var.get(), self.emp_head_var.get(),
                position, hire_date
            )
            messagebox.showinfo("Success", "Employee added successfully")
            self.clear_employee_form()
            self.refresh_employees()
            self.refresh_departments()  # Update department heads
            self.update_status("Employee added")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add employee: {e}")
    
    def update_employee(self):
        """Update selected employee"""
        if not hasattr(self, 'current_emp_id'):
            messagebox.showerror("Error", "Please select an employee to update")
            return
        
        name = self.emp_name_entry.get().strip()
        email = self.emp_email_entry.get().strip()
        dept_str = self.emp_dept_combo.get()
        
        if not name or not email or not dept_str:
            messagebox.showerror("Error", "Name, email, and department are required")
            return
        
        dept_id = int(dept_str.split(' - ')[0])
        position = self.emp_position_entry.get().strip() or None
        hire_date = self.emp_hire_date_entry.get().strip() or None
        
        try:
            self.db.update_employee(
                self.current_emp_id, name, email, dept_id,
                self.emp_supervisor_var.get(), self.emp_head_var.get(),
                position, hire_date
            )
            messagebox.showinfo("Success", "Employee updated successfully")
            self.clear_employee_form()
            self.refresh_employees()
            self.refresh_departments()
            self.update_status("Employee updated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update employee: {e}")
    
    def delete_employee(self):
        """Delete selected employee"""
        if not hasattr(self, 'current_emp_id'):
            messagebox.showerror("Error", "Please select an employee to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            try:
                self.db.delete_employee(self.current_emp_id)
                messagebox.showinfo("Success", "Employee deleted successfully")
                self.clear_employee_form()
                self.refresh_employees()
                self.refresh_departments()
                self.update_status("Employee deleted")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete employee: {e}")
    
    def clear_employee_form(self):
        """Clear employee form"""
        self.emp_name_entry.delete(0, tk.END)
        self.emp_email_entry.delete(0, tk.END)
        self.emp_dept_combo.set('')
        self.emp_position_entry.delete(0, tk.END)
        self.emp_hire_date_entry.delete(0, tk.END)
        self.emp_supervisor_var.set(False)
        self.emp_head_var.set(False)
        if hasattr(self, 'current_emp_id'):
            delattr(self, 'current_emp_id')
    
    # ==================== EMAILS TAB ====================
    
    def create_emails_tab(self):
        """Create email subscriptions management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Email Subscriptions")
        
        # Left panel - Form
        left_panel = ttk.LabelFrame(frame, text="Email Subscription Information", padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        
        ttk.Label(left_panel, text="Email:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(left_panel, width=30)
        self.email_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(left_panel, text="Status:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_status_combo = ttk.Combobox(left_panel, width=27, values=['active', 'unsubscribed', 'bounced'], state="readonly")
        self.email_status_combo.set('active')
        self.email_status_combo.grid(row=1, column=1, pady=5)
        
        ttk.Label(left_panel, text="Source:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_source_entry = ttk.Entry(left_panel, width=30)
        self.email_source_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(left_panel, text="Notes:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.email_notes_text = tk.Text(left_panel, width=30, height=3)
        self.email_notes_text.grid(row=3, column=1, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(left_panel)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add", command=self.add_email).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_email).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_email).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_email_form).pack(side=tk.LEFT, padx=5)
        
        # Filter frame
        filter_frame = ttk.LabelFrame(left_panel, text="Filter", padding=5)
        filter_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky=tk.EW)
        
        ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        self.email_filter_combo = ttk.Combobox(filter_frame, values=['All', 'active', 'unsubscribed', 'bounced'], state="readonly", width=15)
        self.email_filter_combo.set('All')
        self.email_filter_combo.pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Apply Filter", command=self.filter_emails).pack(side=tk.LEFT, padx=5)
        
        # Right panel - List
        right_panel = ttk.LabelFrame(frame, text="Email Subscriptions List", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview
        columns = ("ID", "Email", "Subscribed At", "Status", "Source")
        self.email_tree = ttk.Treeview(right_panel, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.email_tree.heading(col, text=col)
            self.email_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.email_tree.yview)
        self.email_tree.configure(yscrollcommand=scrollbar.set)
        
        self.email_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.email_tree.bind("<Double-1>", self.on_email_select)
        
        ttk.Button(right_panel, text="Refresh", command=self.refresh_emails).pack(pady=5)
        
        self.refresh_emails()
    
    def refresh_emails(self, status=None):
        """Refresh email subscriptions list"""
        # Clear tree
        for item in self.email_tree.get_children():
            self.email_tree.delete(item)
        
        # Load emails
        subscriptions = self.db.get_all_email_subscriptions(status)
        for sub in subscriptions:
            self.email_tree.insert("", tk.END, values=(
                sub['id'], sub['email'], sub['subscribed_at'], 
                sub['status'], sub.get('source', '')
            ))
    
    def filter_emails(self):
        """Filter emails by status"""
        status = self.email_filter_combo.get()
        if status == 'All':
            self.refresh_emails()
        else:
            self.refresh_emails(status)
    
    def on_email_select(self, event):
        """Handle email selection"""
        selection = self.email_tree.selection()
        if selection:
            item = self.email_tree.item(selection[0])
            email_id = item['values'][0]
            sub = self.db.get_email_subscription(email_id)
            if sub:
                self.email_entry.delete(0, tk.END)
                self.email_entry.insert(0, sub['email'])
                self.email_status_combo.set(sub['status'])
                self.email_source_entry.delete(0, tk.END)
                if sub.get('source'):
                    self.email_source_entry.insert(0, sub['source'])
                self.email_notes_text.delete(1.0, tk.END)
                if sub.get('notes'):
                    self.email_notes_text.insert(1.0, sub['notes'])
                self.current_email_id = email_id
    
    def add_email(self):
        """Add new email subscription"""
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showerror("Error", "Email is required")
            return
        
        status = self.email_status_combo.get()
        source = self.email_source_entry.get().strip() or None
        notes = self.email_notes_text.get(1.0, tk.END).strip() or None
        
        try:
            self.db.create_email_subscription(email, status, source, notes)
            messagebox.showinfo("Success", "Email subscription added successfully")
            self.clear_email_form()
            self.refresh_emails()
            self.update_status("Email subscription added")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add email subscription: {e}")
    
    def update_email(self):
        """Update selected email subscription"""
        if not hasattr(self, 'current_email_id'):
            messagebox.showerror("Error", "Please select an email subscription to update")
            return
        
        email = self.email_entry.get().strip()
        status = self.email_status_combo.get()
        source = self.email_source_entry.get().strip() or None
        notes = self.email_notes_text.get(1.0, tk.END).strip() or None
        
        try:
            self.db.update_email_subscription(self.current_email_id, email, status, source, notes)
            messagebox.showinfo("Success", "Email subscription updated successfully")
            self.clear_email_form()
            self.refresh_emails()
            self.update_status("Email subscription updated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update email subscription: {e}")
    
    def delete_email(self):
        """Delete selected email subscription"""
        if not hasattr(self, 'current_email_id'):
            messagebox.showerror("Error", "Please select an email subscription to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this email subscription?"):
            try:
                self.db.delete_email_subscription(self.current_email_id)
                messagebox.showinfo("Success", "Email subscription deleted successfully")
                self.clear_email_form()
                self.refresh_emails()
                self.update_status("Email subscription deleted")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete email subscription: {e}")
    
    def clear_email_form(self):
        """Clear email form"""
        self.email_entry.delete(0, tk.END)
        self.email_status_combo.set('active')
        self.email_source_entry.delete(0, tk.END)
        self.email_notes_text.delete(1.0, tk.END)
        if hasattr(self, 'current_email_id'):
            delattr(self, 'current_email_id')
    
    # ==================== EXPORT TAB ====================
    
    def create_export_tab(self):
        """Create export/import tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Export/Import")
        
        # Export section
        export_frame = ttk.LabelFrame(frame, text="Export Email List", padding=20)
        export_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(export_frame, text="Export Format:").pack(anchor=tk.W, pady=5)
        self.export_format_var = tk.StringVar(value="CSV")
        ttk.Radiobutton(export_frame, text="CSV", variable=self.export_format_var, value="CSV").pack(anchor=tk.W)
        ttk.Radiobutton(export_frame, text="Excel (.xlsx)", variable=self.export_format_var, value="Excel").pack(anchor=tk.W)
        
        ttk.Label(export_frame, text="Filter by Status:").pack(anchor=tk.W, pady=5)
        self.export_status_combo = ttk.Combobox(export_frame, values=['All', 'active', 'unsubscribed', 'bounced'], state="readonly", width=20)
        self.export_status_combo.set('All')
        self.export_status_combo.pack(anchor=tk.W, pady=5)
        
        ttk.Button(export_frame, text="Export Email List", command=self.export_emails).pack(pady=10)
        
        # Import section
        import_frame = ttk.LabelFrame(frame, text="Import Email List from CSV", padding=20)
        import_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(import_frame, text="Select CSV file to import:").pack(anchor=tk.W, pady=5)
        ttk.Button(import_frame, text="Browse and Import", command=self.import_emails).pack(pady=10)
        
        # Results section
        results_frame = ttk.LabelFrame(frame, text="Results", padding=20)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.results_text = tk.Text(results_frame, height=10, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
    
    def export_emails(self):
        """Export emails to CSV or Excel"""
        format_type = self.export_format_var.get()
        status = self.export_status_combo.get()
        status_filter = None if status == 'All' else status
        
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{'csv' if format_type == 'CSV' else 'xlsx'}",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx"),
                ("All files", "*.*")
            ] if format_type == 'CSV' else [
                ("Excel files", "*.xlsx"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                if format_type == 'CSV':
                    success = self.db.export_emails_to_csv(filename, status_filter)
                else:
                    success = self.db.export_emails_to_excel(filename, status_filter)
                
                if success:
                    messagebox.showinfo("Success", f"Email list exported successfully to {filename}")
                    self.results_text.insert(tk.END, f"Export successful: {filename}\n")
                    self.results_text.insert(tk.END, f"Format: {format_type}, Status filter: {status}\n\n")
                    self.update_status(f"Exported to {filename}")
                else:
                    messagebox.showerror("Error", "Failed to export email list")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")
    
    def import_emails(self):
        """Import emails from CSV"""
        filename = filedialog.askopenfilename(
            filetypes=[
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                successful, failed = self.db.import_emails_from_csv(filename)
                messagebox.showinfo(
                    "Import Complete",
                    f"Import completed!\n\nSuccessful: {successful}\nFailed: {failed}"
                )
                self.results_text.insert(tk.END, f"Import from: {filename}\n")
                self.results_text.insert(tk.END, f"Successful imports: {successful}\n")
                self.results_text.insert(tk.END, f"Failed imports: {failed}\n\n")
                self.refresh_emails()
                self.update_status(f"Imported {successful} emails from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Import failed: {e}")
    
    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'db'):
            self.db.close()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = EmailMarketingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

