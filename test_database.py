"""
Quick test script to verify database setup and functionality
"""

from database import DatabaseManager

def test_database():
    """Test basic database operations"""
    print("Testing database setup...")
    
    # Initialize database
    db = DatabaseManager()
    
    # Test departments
    print("\n1. Testing Departments:")
    departments = db.get_all_departments()
    print(f"   Found {len(departments)} departments")
    for dept in departments:
        print(f"   - {dept['name']} (ID: {dept['id']})")
    
    # Test employees
    print("\n2. Testing Employees:")
    employees = db.get_all_employees()
    print(f"   Found {len(employees)} employees")
    supervisors = [e for e in employees if e['is_supervisor']]
    heads = [e for e in employees if e['is_head']]
    print(f"   - Supervisors: {len(supervisors)}")
    print(f"   - Heads of Department: {len(heads)}")
    
    # Test email subscriptions
    print("\n3. Testing Email Subscriptions:")
    subscriptions = db.get_all_email_subscriptions()
    print(f"   Found {len(subscriptions)} email subscriptions")
    active = [s for s in subscriptions if s['status'] == 'active']
    print(f"   - Active: {len(active)}")
    
    # Test export
    print("\n4. Testing CSV Export:")
    if db.export_emails_to_csv("test_export.csv"):
        print("   [OK] CSV export successful")
    else:
        print("   [FAIL] CSV export failed")
    
    # Test import
    print("\n5. Testing CSV Import:")
    try:
        successful, failed = db.import_emails_from_csv("sample_emails.csv")
        print(f"   [OK] Import successful: {successful} imported, {failed} failed")
    except Exception as e:
        print(f"   [FAIL] Import failed: {e}")
    
    # Verify schema rules
    print("\n6. Verifying Schema Rules:")
    all_departments = db.get_all_departments()
    rule1 = len(all_departments) >= 3
    print(f"   - At least 3 departments: {'[OK]' if rule1 else '[FAIL]'} ({len(all_departments)})")
    
    rule2 = True
    rule3 = True
    for dept in all_departments:
        supervisors = db.get_supervisors_by_department(dept['id'])
        if len(supervisors) < 1:
            rule2 = False
        if not dept['head_of_department_id']:
            rule3 = False
    
    print(f"   - Each department has at least 1 supervisor: {'[OK]' if rule2 else '[FAIL]'}")
    print(f"   - Each department has 1 head: {'[OK]' if rule3 else '[FAIL]'}")
    
    db.close()
    print("\n[OK] All tests completed!")

if __name__ == "__main__":
    test_database()

