"""
Command-line interface for Email Marketing Lists and Employee Management
Alternative to GUI for command-line users
"""

import sys
from database import DatabaseManager


def print_menu():
    """Print main menu"""
    print("\n" + "="*60)
    print("Email Marketing & Employee Management System")
    print("="*60)
    print("1. Departments")
    print("2. Employees")
    print("3. Email Subscriptions")
    print("4. Export Email List")
    print("5. Import Email List")
    print("6. View Statistics")
    print("0. Exit")
    print("="*60)


def departments_menu(db):
    """Department management menu"""
    while True:
        print("\n--- Departments ---")
        print("1. List all departments")
        print("2. Add department")
        print("3. Update department")
        print("4. Delete department")
        print("5. View department details")
        print("0. Back to main menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == "1":
            departments = db.get_all_departments()
            print("\nDepartments:")
            print("-" * 60)
            for dept in departments:
                head = db.get_employee(dept['head_of_department_id']) if dept['head_of_department_id'] else None
                head_name = head['name'] if head else "N/A"
                print(f"ID: {dept['id']}, Name: {dept['name']}, Head: {head_name}")
        
        elif choice == "2":
            name = input("Department name: ").strip()
            if name:
                head_id = input("Head of department ID (press Enter to skip): ").strip()
                head_id = int(head_id) if head_id else None
                try:
                    dept_id = db.create_department(name, head_id)
                    print(f"Department created with ID: {dept_id}")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Department name is required")
        
        elif choice == "3":
            dept_id = input("Department ID to update: ").strip()
            if dept_id:
                name = input("New name (press Enter to skip): ").strip() or None
                head_id = input("New head of department ID (press Enter to skip): ").strip()
                head_id = int(head_id) if head_id else None
                try:
                    if db.update_department(int(dept_id), name, head_id):
                        print("Department updated successfully")
                    else:
                        print("Department not found or no changes made")
                except Exception as e:
                    print(f"Error: {e}")
        
        elif choice == "4":
            dept_id = input("Department ID to delete: ").strip()
            if dept_id:
                confirm = input("Are you sure? (yes/no): ").strip().lower()
                if confirm == "yes":
                    try:
                        if db.delete_department(int(dept_id)):
                            print("Department deleted successfully")
                        else:
                            print("Department not found")
                    except Exception as e:
                        print(f"Error: {e}")
        
        elif choice == "5":
            dept_id = input("Department ID: ").strip()
            if dept_id:
                dept = db.get_department(int(dept_id))
                if dept:
                    print(f"\nDepartment Details:")
                    print(f"ID: {dept['id']}")
                    print(f"Name: {dept['name']}")
                    head = db.get_employee(dept['head_of_department_id']) if dept['head_of_department_id'] else None
                    print(f"Head: {head['name'] if head else 'N/A'}")
                    employees = db.get_employees_by_department(int(dept_id))
                    print(f"Employees: {len(employees)}")
                else:
                    print("Department not found")
        
        elif choice == "0":
            break


def employees_menu(db):
    """Employee management menu"""
    while True:
        print("\n--- Employees ---")
        print("1. List all employees")
        print("2. Add employee")
        print("3. Update employee")
        print("4. Delete employee")
        print("5. View employee details")
        print("6. List employees by department")
        print("0. Back to main menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == "1":
            employees = db.get_all_employees()
            print("\nEmployees:")
            print("-" * 80)
            for emp in employees:
                dept_name = emp.get('department_name', 'N/A')
                supervisor = "Yes" if emp['is_supervisor'] else "No"
                head = "Yes" if emp['is_head'] else "No"
                print(f"ID: {emp['id']}, Name: {emp['name']}, Email: {emp['email']}, "
                      f"Dept: {dept_name}, Supervisor: {supervisor}, Head: {head}")
        
        elif choice == "2":
            name = input("Employee name: ").strip()
            email = input("Email: ").strip()
            dept_id = input("Department ID: ").strip()
            position = input("Position (press Enter to skip): ").strip() or None
            hire_date = input("Hire date (YYYY-MM-DD, press Enter to skip): ").strip() or None
            is_supervisor = input("Is supervisor? (yes/no): ").strip().lower() == "yes"
            is_head = input("Is head of department? (yes/no): ").strip().lower() == "yes"
            
            if name and email and dept_id:
                try:
                    emp_id = db.create_employee(name, email, int(dept_id), is_supervisor, is_head, position, hire_date)
                    print(f"Employee created with ID: {emp_id}")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Name, email, and department ID are required")
        
        elif choice == "3":
            emp_id = input("Employee ID to update: ").strip()
            if emp_id:
                name = input("New name (press Enter to skip): ").strip() or None
                email = input("New email (press Enter to skip): ").strip() or None
                dept_id = input("New department ID (press Enter to skip): ").strip()
                dept_id = int(dept_id) if dept_id else None
                position = input("New position (press Enter to skip): ").strip() or None
                hire_date = input("New hire date (YYYY-MM-DD, press Enter to skip): ").strip() or None
                
                try:
                    if db.update_employee(int(emp_id), name, email, dept_id, None, None, position, hire_date):
                        print("Employee updated successfully")
                    else:
                        print("Employee not found or no changes made")
                except Exception as e:
                    print(f"Error: {e}")
        
        elif choice == "4":
            emp_id = input("Employee ID to delete: ").strip()
            if emp_id:
                confirm = input("Are you sure? (yes/no): ").strip().lower()
                if confirm == "yes":
                    try:
                        if db.delete_employee(int(emp_id)):
                            print("Employee deleted successfully")
                        else:
                            print("Employee not found")
                    except Exception as e:
                        print(f"Error: {e}")
        
        elif choice == "5":
            emp_id = input("Employee ID: ").strip()
            if emp_id:
                emp = db.get_employee(int(emp_id))
                if emp:
                    dept = db.get_department(emp['department_id'])
                    print(f"\nEmployee Details:")
                    print(f"ID: {emp['id']}")
                    print(f"Name: {emp['name']}")
                    print(f"Email: {emp['email']}")
                    print(f"Department: {dept['name'] if dept else 'N/A'}")
                    print(f"Position: {emp.get('position', 'N/A')}")
                    print(f"Supervisor: {'Yes' if emp['is_supervisor'] else 'No'}")
                    print(f"Head of Department: {'Yes' if emp['is_head'] else 'No'}")
                else:
                    print("Employee not found")
        
        elif choice == "6":
            dept_id = input("Department ID: ").strip()
            if dept_id:
                employees = db.get_employees_by_department(int(dept_id))
                print(f"\nEmployees in Department:")
                print("-" * 60)
                for emp in employees:
                    print(f"ID: {emp['id']}, Name: {emp['name']}, Email: {emp['email']}")
        
        elif choice == "0":
            break


def emails_menu(db):
    """Email subscription management menu"""
    while True:
        print("\n--- Email Subscriptions ---")
        print("1. List all subscriptions")
        print("2. Add subscription")
        print("3. Update subscription")
        print("4. Delete subscription")
        print("5. View subscription details")
        print("6. Filter by status")
        print("0. Back to main menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == "1":
            subscriptions = db.get_all_email_subscriptions()
            print("\nEmail Subscriptions:")
            print("-" * 80)
            for sub in subscriptions:
                print(f"ID: {sub['id']}, Email: {sub['email']}, Status: {sub['status']}, "
                      f"Subscribed: {sub['subscribed_at']}")
        
        elif choice == "2":
            email = input("Email address: ").strip()
            status = input("Status (active/unsubscribed/bounced, default: active): ").strip() or "active"
            source = input("Source (press Enter to skip): ").strip() or None
            notes = input("Notes (press Enter to skip): ").strip() or None
            
            if email:
                try:
                    sub_id = db.create_email_subscription(email, status, source, notes)
                    print(f"Email subscription created with ID: {sub_id}")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Email is required")
        
        elif choice == "3":
            sub_id = input("Subscription ID to update: ").strip()
            if sub_id:
                email = input("New email (press Enter to skip): ").strip() or None
                status = input("New status (press Enter to skip): ").strip() or None
                source = input("New source (press Enter to skip): ").strip() or None
                notes = input("New notes (press Enter to skip): ").strip() or None
                
                try:
                    if db.update_email_subscription(int(sub_id), email, status, source, notes):
                        print("Subscription updated successfully")
                    else:
                        print("Subscription not found or no changes made")
                except Exception as e:
                    print(f"Error: {e}")
        
        elif choice == "4":
            sub_id = input("Subscription ID to delete: ").strip()
            if sub_id:
                confirm = input("Are you sure? (yes/no): ").strip().lower()
                if confirm == "yes":
                    try:
                        if db.delete_email_subscription(int(sub_id)):
                            print("Subscription deleted successfully")
                        else:
                            print("Subscription not found")
                    except Exception as e:
                        print(f"Error: {e}")
        
        elif choice == "5":
            sub_id = input("Subscription ID: ").strip()
            if sub_id:
                sub = db.get_email_subscription(int(sub_id))
                if sub:
                    print(f"\nSubscription Details:")
                    print(f"ID: {sub['id']}")
                    print(f"Email: {sub['email']}")
                    print(f"Status: {sub['status']}")
                    print(f"Subscribed At: {sub['subscribed_at']}")
                    print(f"Source: {sub.get('source', 'N/A')}")
                    print(f"Notes: {sub.get('notes', 'N/A')}")
                else:
                    print("Subscription not found")
        
        elif choice == "6":
            status = input("Status (active/unsubscribed/bounced): ").strip()
            subscriptions = db.get_all_email_subscriptions(status)
            print(f"\nEmail Subscriptions (Status: {status}):")
            print("-" * 80)
            for sub in subscriptions:
                print(f"ID: {sub['id']}, Email: {sub['email']}, Subscribed: {sub['subscribed_at']}")
        
        elif choice == "0":
            break


def export_emails(db):
    """Export email list"""
    print("\n--- Export Email List ---")
    format_type = input("Format (csv/excel): ").strip().lower()
    status = input("Filter by status (press Enter for all): ").strip() or None
    
    filename = input("Output filename: ").strip()
    if not filename:
        print("Filename is required")
        return
    
    try:
        if format_type == "csv":
            success = db.export_emails_to_csv(filename, status)
        elif format_type == "excel":
            success = db.export_emails_to_excel(filename, status)
        else:
            print("Invalid format. Use 'csv' or 'excel'")
            return
        
        if success:
            print(f"Email list exported successfully to {filename}")
        else:
            print("Export failed")
    except Exception as e:
        print(f"Error: {e}")


def import_emails(db):
    """Import email list"""
    print("\n--- Import Email List ---")
    filename = input("CSV filename: ").strip()
    
    if not filename:
        print("Filename is required")
        return
    
    try:
        successful, failed = db.import_emails_from_csv(filename)
        print(f"\nImport completed!")
        print(f"Successful imports: {successful}")
        print(f"Failed imports: {failed}")
    except Exception as e:
        print(f"Error: {e}")


def view_statistics(db):
    """View database statistics"""
    print("\n--- Database Statistics ---")
    
    departments = db.get_all_departments()
    employees = db.get_all_employees()
    subscriptions = db.get_all_email_subscriptions()
    
    active_emails = len([s for s in subscriptions if s['status'] == 'active'])
    
    print(f"Total Departments: {len(departments)}")
    print(f"Total Employees: {len(employees)}")
    print(f"Total Email Subscriptions: {len(subscriptions)}")
    print(f"Active Email Subscriptions: {active_emails}")
    
    print("\nDepartments Breakdown:")
    for dept in departments:
        dept_employees = db.get_employees_by_department(dept['id'])
        supervisors = db.get_supervisors_by_department(dept['id'])
        print(f"  {dept['name']}: {len(dept_employees)} employees, {len(supervisors)} supervisors")


def main():
    """Main CLI application"""
    db = DatabaseManager()
    
    try:
        while True:
            print_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                departments_menu(db)
            elif choice == "2":
                employees_menu(db)
            elif choice == "3":
                emails_menu(db)
            elif choice == "4":
                export_emails(db)
            elif choice == "5":
                import_emails(db)
            elif choice == "6":
                view_statistics(db)
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\n\nExiting...")
    finally:
        db.close()


if __name__ == "__main__":
    main()

