from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Administrator access required.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def pharmacist_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'pharmacist']:
            flash('Pharmacist access required.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def generate_sample_data():
    """Generate sample data for testing/demo purposes"""
    from app import db
    from app.models import User, Medicine, Branch, Inventory
    from datetime import datetime, timedelta
    
    # Create sample users
    admin_user = User(username='admin', email='admin@pharmacy.gov', role='admin')
    admin_user.set_password('admin123')
    
    pharmacist_user = User(username='pharmacist', email='pharmacist@pharmacy.gov', role='pharmacist')
    pharmacist_user.set_password('pharma123')
    
    public_user = User(username='public', email='public@example.com', role='public')
    public_user.set_password('public123')
    
    db.session.add_all([admin_user, pharmacist_user, public_user])
    
    # Create sample medicines
    medicines = [
        Medicine(name='Paracetamol 500mg', category='analgesic', description='Pain reliever and fever reducer', expiry_date=datetime.now() + timedelta(days=365)),
        Medicine(name='Amoxicillin 250mg', category='antibiotic', description='Broad-spectrum antibiotic', expiry_date=datetime.now() + timedelta(days=300)),
        Medicine(name='Vitamin C 1000mg', category='vitamin', description='Immune system support', expiry_date=datetime.now() + timedelta(days=400)),
        Medicine(name='Metformin 500mg', category='diabetes', description='Type 2 diabetes medication', expiry_date=datetime.now() + timedelta(days=350)),
    ]
    
    db.session.add_all(medicines)
    
    # Create sample branches
    branches = [
        Branch(name='Central Hospital Pharmacy', region='central', address='123 Main St, Central City', phone='+1234567890'),
        Branch(name='North Regional Clinic', region='north', address='456 North Ave, North Town', phone='+1234567891'),
        Branch(name='South Medical Center', region='south', address='789 South Rd, South Village', phone='+1234567892'),
    ]
    
    db.session.add_all(branches)
    
    db.session.commit()
    
    # Create sample inventory
    for branch in branches:
        for medicine in medicines:
            inventory = Inventory(
                branch_id=branch.branch_id,
                medicine_id=medicine.medicine_id,
                quantity=50 if medicine.name == 'Paracetamol 500mg' else 30,
                min_stock_level=10
            )
            db.session.add(inventory)
    
    db.session.commit()