from app import db
from app.models import Notification, User, Inventory, Medicine, Branch
from datetime import datetime, timedelta

def create_inventory_notification(inventory_item, notification_type, old_quantity=None):
    """Create inventory-related notifications"""
    if notification_type == 'low_stock':
        data = {
            'title': 'Low Stock Alert',
            'message': f'{inventory_item.medicine.name} is running low at {inventory_item.branch.name}. Current: {inventory_item.quantity}',
            'priority': 'high',
            'type': 'low_stock'
        }
    elif notification_type == 'out_of_stock':
        data = {
            'title': 'Out of Stock',
            'message': f'{inventory_item.medicine.name} is out of stock at {inventory_item.branch.name}',
            'priority': 'high',
            'type': 'out_of_stock'
        }
    elif notification_type == 'restocked':
        data = {
            'title': 'Medicine Restocked',
            'message': f'{inventory_item.medicine.name} has been restocked at {inventory_item.branch.name}. New quantity: {inventory_item.quantity}',
            'priority': 'medium',
            'type': 'available'
        }
    elif notification_type == 'expiring_soon':
        data = {
            'title': 'Medicine Expiring Soon',
            'message': f'{inventory_item.medicine.name} expires on {inventory_item.medicine.expiry_date.strftime("%Y-%m-%d")}',
            'priority': 'high',
            'type': 'expiry_warning'
        }
    else:
        return False
    
    notification = Notification(
        branch_id=inventory_item.branch_id,
        type=data['type'],
        title=data['title'],
        message=data['message'],
        priority=data['priority'],
        is_read=False
    )
    db.session.add(notification)
    return True

def create_user_notification(user, notification_type, admin_user=None):
    """Create user-related notifications"""
    if notification_type == 'new_user_registered':
        data = {
            'title': 'New User Registration',
            'message': f'New user {user.username} ({user.role}) registered and needs approval.',
            'priority': 'medium',
            'type': 'user_registration',
            'target': 'admin'
        }
    elif notification_type == 'user_approved':
        data = {
            'title': 'Account Approved',
            'message': f'Your account has been approved by {admin_user.username}. You can now access the system.' if admin_user else 'Your account has been approved. You can now access the system.',
            'priority': 'medium',
            'type': 'user_approved',
            'target': 'user'
        }
    elif notification_type == 'user_rejected':
        data = {
            'title': 'Account Rejected',
            'message': f'Your registration has been reviewed and rejected.',
            'priority': 'medium',
            'type': 'user_rejected', 
            'target': 'user'
        }
    elif notification_type == 'role_changed':
        data = {
            'title': 'Role Updated',
            'message': f'Your role has been changed to {user.role} by {admin_user.username}.' if admin_user else f'Your role has been changed to {user.role}.',
            'priority': 'medium',
            'type': 'role_changed',
            'target': 'user'
        }
    elif notification_type == 'branch_assigned':
        data = {
            'title': 'Branch Assignment', 
            'message': f'You have been assigned to {user.branch.name} branch.' if user.branch else 'You have been assigned to a branch.',
            'priority': 'low',
            'type': 'branch_assigned',
            'target': 'user'
        }
    else:
        return False
    
    notification = Notification(
        user_id=user.id if data['target'] == 'user' else None,
        branch_id=user.branch_id,
        type=data['type'],
        title=data['title'],
        message=data['message'],
        priority=data['priority'],
        is_read=False
    )
    db.session.add(notification)
    return True

def create_system_notification(notification_type, branch_id=None, user_id=None, extra_data=None):
    """Create system-wide notifications"""
    notification_data = {
        'system_maintenance': {
            'title': 'System Maintenance',
            'message': 'System maintenance scheduled for tomorrow from 2:00 AM to 4:00 AM.',
            'priority': 'medium',
            'type': 'system_maintenance'
        },
        'new_feature': {
            'title': 'New Feature Available',
            'message': 'New inventory reporting feature is now available. Check the reports section.',
            'priority': 'low',
            'type': 'new_feature'
        },
        'security_alert': {
            'title': 'Security Alert',
            'message': 'Multiple failed login attempts detected from your account.',
            'priority': 'high',
            'type': 'security_alert'
        }
    }
    
    if notification_type in notification_data:
        data = notification_data[notification_type]
        notification = Notification(
            user_id=user_id,
            branch_id=branch_id,
            type=data['type'],
            title=data['title'],
            message=data['message'],
            priority=data['priority'],
            is_read=False
        )
        db.session.add(notification)
        return True
    return False

def check_expiry_notifications():
    """Check for medicines expiring soon and create notifications"""
    soon = datetime.now().date() + timedelta(days=30)  # 30 days from now
    
    expiring_medicines = Medicine.query.filter(
        Medicine.expiry_date <= soon,
        Medicine.expiry_date >= datetime.now().date()
    ).all()
    
    for medicine in expiring_medicines:
        # Get all branches that have this medicine
        inventories = Inventory.query.filter_by(medicine_id=medicine.medicine_id).all()
        
        for inventory in inventories:
            # Check if expiry notification already exists
            existing = Notification.query.filter(
                Notification.medicine_id == medicine.medicine_id,
                Notification.branch_id == inventory.branch_id,
                Notification.type == 'expiry_warning',
                Notification.created_at >= datetime.now().date()
            ).first()
            
            if not existing:
                create_inventory_notification(inventory, 'expiring_soon')

def check_low_stock_notifications():
    """Check for low stock items and create notifications"""
    low_stock_items = Inventory.query.filter(
        Inventory.quantity <= Inventory.min_stock_level
    ).all()
    
    for item in low_stock_items:
        # Check if low stock notification already exists today
        existing = Notification.query.filter(
            Notification.medicine_id == item.medicine_id,
            Notification.branch_id == item.branch_id,
            Notification.type == 'low_stock',
            Notification.created_at >= datetime.now().date()
        ).first()
        
        if not existing:
            create_inventory_notification(item, 'low_stock')

def create_pharmacist_notification(message, contact_info=None):
    """Create a notification for pharmacists from a user inquiry"""
    
    # Find all pharmacists
    pharmacists = User.query.filter_by(role='pharmacist').all()
    # If no pharmacists, fall back to admins
    if not pharmacists:
        pharmacists = User.query.filter_by(role='admin').all()
        
    count = 0
    safe_contact = contact_info if contact_info else "No contact info provided"
    
    for pharmacist in pharmacists:
        notification = Notification(
            user_id=pharmacist.id,
            type='user_inquiry',
            title='New User Inquiry',
            message=f"Inquiry: {message}\nContact: {safe_contact}",
            priority='medium',
            is_read=False
        )
        db.session.add(notification)
        count += 1
        
    db.session.commit()
    return count > 0

def create_pharmacist_reply_notification(user, message, pharmacist_user):
    """Create a reply notification for a user from a pharmacist"""
    notification = Notification(
        user_id=user.id,
        type='pharmacist_reply',
        title='Message from Pharmacist',
        message=message,
        priority='medium',
        is_read=False
    )
    db.session.add(notification)
    db.session.commit()
    return True