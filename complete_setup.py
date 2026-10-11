import pyodbc
from datetime import datetime, timedelta

def setup_database_complete():
    """Complete database setup with proper permissions"""
    print("🚀 Starting complete database setup...")
    
    try:
        # Step 1: Connect to master database
        print("Step 1: Connecting to master database...")
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=.;'
            'Database=master;'
            'Trusted_Connection=yes;'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Step 2: Create database
        print("Step 2: Creating database 'pharmacy_db'...")
        cursor.execute("CREATE DATABASE pharmacy_db")
        print("✅ Database 'pharmacy_db' created successfully!")
        
        # Step 3: Switch to pharmacy_db and set up permissions
        # print("Step 3: Setting up database permissions...")
        # cursor.execute("USE pharmacy_db")
        
        # Grant db_owner role to current user
        # cursor.execute("""
        #     CREATE USER [Safa and Salsabel-PC\\Safa and Salsabel] FOR LOGIN [Safa and Salsabel-PC\\Safa and Salsabel]
        # """)
        # cursor.execute("ALTER ROLE db_owner ADD MEMBER [Safa and Salsabel-PC\\Safa and Salsabel]")
        # print("✅ User permissions granted successfully!")
        
        # cursor.close()
        # conn.close()
        
        # Step 4: Create tables and sample data
        print("Step 4: Creating tables and sample data...")
        create_tables_and_data()
        
        print("🎉 Database setup completed successfully!")
        print("\nYou can now run: python run.py")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("\nTrying alternative approach...")
        try_alternative_setup()

def try_alternative_setup():
    """Alternative setup if the first one fails"""
    try:
        print("Trying alternative setup...")
        
        # Simple approach - just create the database
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=.;'
            'Database=master;'
            'Trusted_Connection=yes;'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        cursor.execute("CREATE DATABASE pharmacy_db")
        print("✅ Database created (alternative method)")
        
        cursor.close()
        conn.close()
        
        # Now try to create tables
        create_tables_and_data()
        
    except Exception as e:
        print(f"❌ Alternative setup also failed: {e}")
        print("\nLet's use SQLite for now...")
        use_sqlite_temporary()

def use_sqlite_temporary():
    """Use SQLite temporarily to get the app running"""
    print("Setting up SQLite database temporarily...")
    
    # Update config to use SQLite
    config_content = '''
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pharmacy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_SERVE_LOCAL = True
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
'''
    
    with open('config.py', 'w') as f:
        f.write(config_content)
    
    print("✅ SQLite configuration set")
    create_tables_and_data()

def create_tables_and_data():
    """Create tables and sample data"""
    try:
        from app import create_app, db
        from app.models import User, Medicine, Branch, Inventory
        
        app = create_app()
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Tables created successfully")
            
            # Check if sample data already exists
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
                
                # Create sample medicines
                medicines = [
                    Medicine(name='Paracetamol 500mg', category='analgesic', description='Pain reliever', expiry_date=datetime.now() + timedelta(days=365)),
                    Medicine(name='Amoxicillin 250mg', category='antibiotic', description='Antibiotic', expiry_date=datetime.now() + timedelta(days=300)),
                    Medicine(name='Vitamin C 1000mg', category='vitamin', description='Immune support', expiry_date=datetime.now() + timedelta(days=400)),
                ]
                
                db.session.add_all(medicines)
                db.session.commit()
                
                # Create sample branches
                branches = [
                    Branch(name='Central Hospital', region='central', address='123 Main St'),
                    Branch(name='North Clinic', region='north', address='456 North Ave'),
                ]
                
                db.session.add_all(branches)
                db.session.commit()
                
                print("✅ Sample data created successfully!")
                print("\n📋 Demo Login Credentials:")
                print("   Admin: admin / admin123")
                print("   Pharmacist: pharmacist / pharma123")
                print("   Public: public / public123")
            else:
                print("✅ Sample data already exists")
                
    except Exception as e:
        print(f"❌ Error creating tables/data: {e}")

if __name__ == '__main__':
    setup_database_complete()