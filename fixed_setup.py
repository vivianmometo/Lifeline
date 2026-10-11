import pyodbc
from datetime import datetime, timedelta

def setup_database_properly():
    """Proper database setup with permissions"""
    try:
        print("Step 1: Connecting to master database...")
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=Safa and Salsabel-PC;'
            'Database=master;'
            'Trusted_Connection=yes;'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Step 2: Checking/Creating database...")
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'pharmacy_db'")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE pharmacy_db")
            print("✅ Database 'pharmacy_db' created")
        else:
            print("✅ Database 'pharmacy_db' already exists")
        
        print("Step 3: Setting up user permissions...")
        # Grant user access to the database
        try:
            cursor.execute("USE pharmacy_db")
            cursor.execute("""
                IF NOT EXISTS (SELECT name FROM sys.database_principals WHERE name = 'Safa and Salsabel-PC\\Safa and Salsabel')
                BEGIN
                    CREATE USER [Safa and Salsabel-PC\\Safa and Salsabel] FOR LOGIN [Safa and Salsabel-PC\\Safa and Salsabel]
                END
            """)
            cursor.execute("ALTER ROLE db_owner ADD MEMBER [Safa and Salsabel-PC\\Safa and Salsabel]")
            print("✅ User permissions granted")
        except Exception as e:
            print(f"⚠️  Permission setup warning: {e}")
        
        cursor.close()
        conn.close()
        
        print("Step 4: Creating tables and sample data...")
        create_tables_and_data()
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")

def create_tables_and_data():
    """Create tables and sample data"""
    from app import create_app, db
    from app.models import User, Medicine, Branch, Inventory
    
    app = create_app()
    
    with app.app_context():
        try:
            db.create_all()
            print("✅ Tables created successfully")
            
            if User.query.first() is None:
                # Create sample users
                admin_user = User(username='admin', email='admin@pharmacy.gov', role='admin')
                admin_user.set_password('admin123')
                
                pharmacist_user = User(username='pharmacist', email='pharmacist@pharmacy.gov', role='pharmacist')
                pharmacist_user.set_password('pharma123')
                
                public_user = User(username='public', email='public@example.com', role='public')
                public_user.set_password('public123')
                
                db.session.add_all([admin_user, pharmacist_user, public_user])
                db.session.commit()
                
                print("✅ Sample users created")
                print("   Admin: admin / admin123")
                print("   Pharmacist: pharmacist / pharma123")
                print("   Public: public / public123")
            else:
                print("✅ Sample data already exists")
                
        except Exception as e:
            print(f"❌ Error creating tables/data: {e}")

if __name__ == '__main__':
    setup_database_properly()