
import pyodbc
from datetime import datetime, timedelta

def create_database():
    """Create database if it doesn't exist"""
    try:
   
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=.;'
            'Database=master;'
            'Trusted_Connection=yes;'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
      
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'pharmacy_db'")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE pharmacy_db")
            print("Database 'pharmacy_db' created successfully.")
        else:
            print("Database 'pharmacy_db' already exists.")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating database: {e}")
        
def init_database():
    """Initialize database with tables and sample data"""
    from app import create_app, db
    from app.models import User, Medicine, Branch, Inventory
    
    app = create_app()
    
    with app.app_context():
      
        db.create_all()
        print("All tables created successfully.")
        
    
        if User.query.first() is None:
            create_sample_data()
            create_sample_notifications() 
            print("Sample data created successfully.")
        else:
            print("Sample data already exists.")

def create_sample_data():
    """Create sample data for testing - UPDATED FOR BRANCH RELATIONSHIP"""
    from app import db
    from app.models import User, Medicine, Branch, Inventory
    
  
    branches = [
        Branch(
            name='Central Hospital Pharmacy', 
            region='central', 
            address='123 Main St, Central City',
            phone='+1234567890'
        ),
        Branch(
            name='North Regional Clinic', 
            region='north', 
            address='456 North Ave, North Town',
            phone='+1234567891'
        ),
        Branch(
            name='South Medical Center', 
            region='south', 
            address='789 South Rd, South Village',
            phone='+1234567892'
        ),
    ]
    
    db.session.add_all(branches)
    db.session.commit()
    
   
    admin_user = User(
        username='admin', 
        email='admin@pharmacy.gov', 
        role='admin',
        branch_id=branches[0].branch_id  
    )
    admin_user.set_password('admin123')
    
    pharmacist_user = User(
        username='pharmacist', 
        email='pharmacist@pharmacy.gov', 
        role='pharmacist',
        branch_id=branches[0].branch_id  
    )
    pharmacist_user.set_password('pharma123')
    
    public_user = User(
        username='public', 
        email='public@example.com', 
        role='public',
        branch_id=None 
    )
    public_user.set_password('public123')
    
    db.session.add_all([admin_user, pharmacist_user, public_user])
    db.session.commit()
    
   
    medicines = [
        Medicine(
            name='Paracetamol 500mg', 
            category='analgesic', 
            description='Pain reliever and fever reducer',
            expiry_date=datetime.now() + timedelta(days=365)
        ),
        Medicine(
            name='Amoxicillin 250mg', 
            category='antibiotic', 
            description='Broad-spectrum antibiotic',
            expiry_date=datetime.now() + timedelta(days=300)
        ),
        Medicine(
            name='Vitamin C 1000mg', 
            category='vitamin', 
            description='Immune system support',
            expiry_date=datetime.now() + timedelta(days=400)
        ),
        Medicine(
            name='Metformin 500mg', 
            category='diabetes', 
            description='Type 2 diabetes medication',
            expiry_date=datetime.now() + timedelta(days=350)
        ),
    ]
    
    db.session.add_all(medicines)
    db.session.commit()
    
    
    for branch in Branch.query.all():
        for medicine in Medicine.query.all():
          
            if medicine.name == 'Paracetamol 500mg':
                quantity = 50
            elif medicine.name == 'Amoxicillin 250mg':
                quantity = 15 
            elif medicine.name == 'Vitamin C 1000mg':
                quantity = 0  
            else:
                quantity = 30
                
            inventory = Inventory(
                branch_id=branch.branch_id,
                medicine_id=medicine.medicine_id,
                quantity=quantity,
                min_stock_level=10
            )
            db.session.add(inventory)
    
    db.session.commit()

def create_sample_notifications():
    """Create sample notifications for testing"""
    from app import db
    from app.models import Notification, Branch, Medicine
    from datetime import datetime, timedelta
    
    try:
      
        branch = Branch.query.first()
        medicines = Medicine.query.all()
        
        if not branch or not medicines:
            print("❌ Cannot create notifications - no branches or medicines found")
            return
        
        
        Notification.query.delete()
        
       
        notifications = [
            Notification(
                medicine_id=medicines[0].medicine_id,
                branch_id=branch.branch_id,
                type='low-stock',
                message=f'Low stock alert for {medicines[0].name}. Current quantity: 15',
                is_read=False,
                created_at=datetime.now() - timedelta(hours=2)
            ),
            Notification(
                medicine_id=medicines[1].medicine_id,
                branch_id=branch.branch_id,
                type='out-of-stock',
                message=f'{medicines[1].name} is out of stock. Please restock.',
                is_read=True,
                created_at=datetime.now() - timedelta(days=1)
            ),
            Notification(
                medicine_id=medicines[2].medicine_id,
                branch_id=branch.branch_id,
                type='available',
                message=f'{medicines[2].name} has been restocked.',
                is_read=False,
                created_at=datetime.now() - timedelta(hours=6)
            ),
            Notification(
                medicine_id=medicines[3].medicine_id if len(medicines) > 3 else medicines[0].medicine_id,
                branch_id=branch.branch_id,
                type='low-stock',
                message=f'Stock running low for {medicines[3].name if len(medicines) > 3 else medicines[0].name}. Only 5 units remaining.',
                is_read=False,
                created_at=datetime.now() - timedelta(hours=1)
            )
        ]
        
        db.session.add_all(notifications)
        db.session.commit()
        print(f"✅ Created {len(notifications)} sample notifications")
        
    except Exception as e:
        print(f"❌ Error creating sample notifications: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
    """Create sample notifications for testing"""
    from app import db 
    from app.models import Notification, Branch, Medicine  
    
    try:
      
        branch = Branch.query.first()
        medicines = Medicine.query.all()
        
        if not branch or not medicines:
            print("❌ Cannot create notifications - no branches or medicines found")
            return
        
        notifications = [
            Notification(
                medicine_id=medicines[0].medicine_id,
                branch_id=branch.branch_id,
                status='low-stock',
                message=f'Low stock alert for {medicines[0].name}. Current quantity: 15',
                is_read=False
            ),
            Notification(
                medicine_id=medicines[1].medicine_id,
                branch_id=branch.branch_id,
                status='out-of-stock',
                message=f'{medicines[1].name} is out of stock. Please restock.',
                is_read=True
            ),
            Notification(
                medicine_id=medicines[2].medicine_id,
                branch_id=branch.branch_id,
                status='available',
                message=f'{medicines[2].name} has been restocked.',
                is_read=False
            ),
            Notification(
                medicine_id=medicines[3].medicine_id if len(medicines) > 3 else medicines[0].medicine_id,
                branch_id=branch.branch_id,
                status='low-stock',
                message=f'Stock running low for {medicines[3].name if len(medicines) > 3 else medicines[0].name}. Only 5 units remaining.',
                is_read=False
            )
        ]
        
        db.session.add_all(notifications)
        db.session.commit()
        print(f"✅ Created {len(notifications)} sample notifications")
        
    except Exception as e:
        print(f"❌ Error creating sample notifications: {e}")
        db.session.rollback()