from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), nullable=False, default='public')
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=True) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    branch = db.relationship('Branch', backref='users')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username} - {self.role}>'

class Medicine(db.Model):
    __tablename__ = 'medicines'
    
    medicine_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    expiry_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    inventory_items = db.relationship('Inventory', backref='medicine', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Medicine {self.name}>'

class Branch(db.Model):
    __tablename__ = 'branches'
    
    branch_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    inventory_items = db.relationship('Inventory', backref='branch', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Branch {self.name} - {self.region}>'

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    inventory_id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.medicine_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    min_stock_level = db.Column(db.Integer, default=10)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def is_low_stock(self):
        return self.quantity <= self.min_stock_level
    
    def is_out_of_stock(self):
        return self.quantity == 0
    
    def __repr__(self):
        return f'<Inventory {self.medicine.name} at {self.branch.name}: {self.quantity}>'


class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.medicine_id'), nullable=True)
    type = db.Column(db.String(50), nullable=False)  # low_stock, out_of_stock, user_approved, etc.
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='medium')  # high, medium, low
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    branch = db.relationship('Branch', backref='notifications')
    medicine = db.relationship('Medicine', backref='notifications')

    @property
    def inquiry_contact(self):
        """Extract contact info from message for user inquiries"""
        if self.type == 'user_inquiry' and 'Contact: ' in self.message:
            try:
                # Format is "Inquiry: ...\nContact: email@example.com"
                return self.message.split('Contact: ')[-1].strip()
            except:
                return None
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))