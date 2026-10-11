# from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
# from flask_login import login_required, current_user
# from app import db
# from app.models import Medicine, Branch, Inventory, Notification
# from app.forms import InventoryForm
# from app.utils import pharmacist_required

# pharmacist = Blueprint('pharmacist', __name__)

# @pharmacist.before_request
# @login_required
# @pharmacist_required
# def require_pharmacist():
#     pass


# @pharmacist.route('/dashboard')
# def dashboard():
#     # Get pharmacist's assigned branch
#     branch = current_user.branch
    
#     if branch:
#         inventory_items = Inventory.query.filter_by(branch_id=branch.branch_id).all()
#         low_stock_items = [item for item in inventory_items if item.is_low_stock()]
#         out_of_stock_items = [item for item in inventory_items if item.is_out_of_stock()]
#     else:
#         # Fallback to first branch if no branch assigned
#         branch = Branch.query.first()
#         inventory_items = Inventory.query.filter_by(branch_id=branch.branch_id).all() if branch else []
#         low_stock_items = []
#         out_of_stock_items = []
#         flash('No branch assigned! Showing first branch as default.', 'warning')
    
#     return render_template('pharmacist/dashboard.html',
#                          title='Pharmacist Dashboard',
#                          branch=branch,
#                          inventory_items=inventory_items,
#                          low_stock_items=low_stock_items,
#                          out_of_stock_items=out_of_stock_items)

# @pharmacist.route('/inventory')
# def inventory():
#     # Get pharmacist's assigned branch
#     branch = current_user.branch
    
#     if branch:
#         inventory_items = Inventory.query.filter_by(branch_id=branch.branch_id).all()
#     else:
#         # Fallback to first branch
#         branch = Branch.query.first()
#         inventory_items = Inventory.query.filter_by(branch_id=branch.branch_id).all() if branch else []
#         flash('No branch assigned! Showing first branch as default.', 'warning')
    
#     return render_template('pharmacist/inventory.html',
#                          title='Inventory Management',
#                          branch=branch,
#                          inventory_items=inventory_items)

# @pharmacist.route('/inventory/update/<int:inventory_id>', methods=['GET', 'POST'])
# def update_inventory(inventory_id):
#     inventory_item = Inventory.query.get_or_404(inventory_id)
#     form = InventoryForm(obj=inventory_item)
    
#     # Set choices for branches and medicines
#     form.branch_id.choices = [(b.branch_id, b.name) for b in Branch.query.all()]
#     form.medicine_id.choices = [(m.medicine_id, m.name) for m in Medicine.query.all()]
    
#     if form.validate_on_submit():
#         old_quantity = inventory_item.quantity
#         new_quantity = form.quantity.data
        
#         inventory_item.quantity = new_quantity
#         inventory_item.min_stock_level = form.min_stock_level.data
#         db.session.commit()
        
#         # Check for stock status changes and create notifications
#         if old_quantity == 0 and new_quantity > 0:
#             notification = Notification(
#                 medicine_id=inventory_item.medicine_id,
#                 branch_id=inventory_item.branch_id,
#                 status='available',
#                 message=f'{inventory_item.medicine.name} is now available at {inventory_item.branch.name}'
#             )
#             db.session.add(notification)
#             db.session.commit()
#             flash('Inventory updated and notification sent for restocked medicine!', 'success')
#         elif old_quantity > 0 and new_quantity == 0:
#             notification = Notification(
#                 medicine_id=inventory_item.medicine_id,
#                 branch_id=inventory_item.branch_id,
#                 status='out-of-stock',
#                 message=f'{inventory_item.medicine.name} is out of stock at {inventory_item.branch.name}'
#             )
#             db.session.add(notification)
#             db.session.commit()
#             flash('Inventory updated and notification sent for out-of-stock medicine!', 'warning')
#         else:
#             flash('Inventory updated successfully!', 'success')
        
#         return redirect(url_for('pharmacist.inventory'))
    
#     return render_template('pharmacist/inventory_form.html',
#                          form=form,
#                          title='Update Inventory',
#                          inventory_item=inventory_item)


# @pharmacist.route('/notifications')
# def notifications():
#     # Show notifications only for the user's assigned branch
#     user_branch_id = current_user.branch_id
    
#     if user_branch_id:
#         notifications = Notification.query\
#             .filter_by(branch_id=user_branch_id)\
#             .order_by(Notification.created_at.desc())\
#             .all()
#     else:
#         # Admin sees all notifications
#         notifications = Notification.query\
#             .order_by(Notification.created_at.desc())\
#             .all()
    
#     return render_template('pharmacist/notifications.html',
#                          title='Notifications',
#                          notifications=notifications)

# @pharmacist.route('/notifications/<int:notification_id>/read')
# def mark_notification_read(notification_id):
#     """Mark a single notification as read"""
#     notification = Notification.query.get_or_404(notification_id)
    
#     # Check if notification belongs to user's branch
#     if notification.branch_id != current_user.branch_id:
#         flash('You do not have permission to modify this notification.', 'error')
#         return redirect(url_for('pharmacist.notifications'))
    
#     notification.is_read = True
#     db.session.commit()
#     flash('Notification marked as read', 'info')
#     return redirect(url_for('pharmacist.notifications'))

# @pharmacist.route('/notifications/mark-all-read', methods=['POST'])
# def mark_all_notifications_read():
#     """Mark all notifications as read for the current branch"""
#     notifications = Notification.query\
#         .filter_by(branch_id=current_user.branch_id, is_read=False)\
#         .all()
    
#     for notification in notifications:
#         notification.is_read = True
    
#     db.session.commit()
#     flash('All notifications marked as read.', 'success')
#     return redirect(url_for('pharmacist.notifications'))

# @pharmacist.route('/api/notifications/count')
# def get_notification_count():
#     """Get unread notification count for AJAX updates"""
#     unread_count = Notification.query\
#         .filter_by(branch_id=current_user.branch_id, is_read=False)\
#         .count()
    
#     return jsonify({'unread_count': unread_count})
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Medicine, Branch, Inventory, Notification, User
from app.forms import InventoryForm
from app.utils import pharmacist_required
from app.notifications import create_inventory_notification, create_pharmacist_reply_notification

pharmacist = Blueprint('pharmacist', __name__)

@pharmacist.before_request
@login_required
@pharmacist_required
def require_pharmacist():
    pass

@pharmacist.route('/dashboard')
def dashboard():
    # Get pharmacist's assigned branch
    branch = current_user.branch
    
    if branch:
        inventory_items = Inventory.query.filter_by(branch_id=branch.branch_id).all()
        low_stock_items = [item for item in inventory_items if item.is_low_stock()]
        out_of_stock_items = [item for item in inventory_items if item.is_out_of_stock()]
    else:
        # Fallback to first branch if no branch assigned
        branch = Branch.query.first()
        inventory_items = Inventory.query.filter_by(branch_id=branch.branch_id).all() if branch else []
        low_stock_items = []
        out_of_stock_items = []
        flash('No branch assigned! Showing first branch as default.', 'warning')
    
    return render_template('pharmacist/dashboard.html',
                         title='Pharmacist Dashboard',
                         branch=branch,
                         inventory_items=inventory_items,
                         low_stock_items=low_stock_items,
                         out_of_stock_items=out_of_stock_items)

@pharmacist.route('/inventory')
def inventory():
    # Get pharmacist's assigned branch
    branch = current_user.branch
    
    if branch:
        inventory_items = Inventory.query.filter_by(branch_id=branch.branch_id).all()
    else:
        # Fallback to first branch
        branch = Branch.query.first()
        inventory_items = Inventory.query.filter_by(branch_id=branch.branch_id).all() if branch else []
        flash('No branch assigned! Showing first branch as default.', 'warning')
    
    return render_template('pharmacist/inventory.html',
                         title='Inventory Management',
                         branch=branch,
                         inventory_items=inventory_items)

@pharmacist.route('/inventory/update/<int:inventory_id>', methods=['GET', 'POST'])
def update_inventory(inventory_id):
    inventory_item = Inventory.query.get_or_404(inventory_id)
    form = InventoryForm(obj=inventory_item)
    
    # Set choices for branches and medicines
    form.branch_id.choices = [(b.branch_id, b.name) for b in Branch.query.all()]
    form.medicine_id.choices = [(m.medicine_id, m.name) for m in Medicine.query.all()]
    
    if form.validate_on_submit():
        old_quantity = inventory_item.quantity
        new_quantity = form.quantity.data
        
        inventory_item.quantity = new_quantity
        inventory_item.min_stock_level = form.min_stock_level.data
        db.session.commit()
        
        # AUTOMATIC NOTIFICATION GENERATION
        if old_quantity > 0 and new_quantity == 0:
            create_inventory_notification(inventory_item, 'out_of_stock', old_quantity)
            flash('Inventory updated and out-of-stock notification created!', 'warning')
        elif old_quantity == 0 and new_quantity > 0:
            create_inventory_notification(inventory_item, 'restocked', old_quantity)
            flash('Inventory updated and restock notification created!', 'success')
        elif new_quantity <= inventory_item.min_stock_level:
            create_inventory_notification(inventory_item, 'low_stock', old_quantity)
            flash('Inventory updated and low stock notification created!', 'warning')
        else:
            flash('Inventory updated successfully!', 'success')
        
        db.session.commit()
        return redirect(url_for('pharmacist.inventory'))
    
    return render_template('pharmacist/inventory_form.html',
                         form=form,
                         title='Update Inventory',
                         inventory_item=inventory_item)

@pharmacist.route('/notifications')
def notifications():
    # Enhanced notifications query with priority sorting
    user_branch_id = current_user.branch_id
    
    if current_user.role == 'admin':
        # Admins see all branch notifications and system notifications
        notifications = Notification.query.filter(
            (Notification.branch_id.isnot(None)) | 
            (Notification.user_id.is_(None))
        )
    elif user_branch_id:
        # Pharmacists see their branch notifications and personal notifications
        notifications = Notification.query.filter(
            (Notification.branch_id == user_branch_id) |
            (Notification.user_id == current_user.id)
        )
    else:
        # Users without branch see only personal notifications
        notifications = Notification.query.filter(
            Notification.user_id == current_user.id
        )
    
    notifications = notifications.order_by(
        db.case(
            (Notification.priority == 'high', 1),
            (Notification.priority == 'medium', 2),
            (Notification.priority == 'low', 3),
            else_=4
        ),
        Notification.created_at.desc()
    ).all()
    
    return render_template('pharmacist/notifications.html',
                         title='Notifications',
                         notifications=notifications)

@pharmacist.route('/notifications/<int:notification_id>/read')
def mark_notification_read(notification_id):
    """Mark a single notification as read"""
    notification = Notification.query.get_or_404(notification_id)
    
    # Check permissions
    if (notification.branch_id and notification.branch_id != current_user.branch_id and 
        current_user.role != 'admin'):
        flash('You do not have permission to modify this notification.', 'error')
        return redirect(url_for('pharmacist.notifications'))
    
    if notification.user_id and notification.user_id != current_user.id:
        flash('You do not have permission to modify this notification.', 'error')
        return redirect(url_for('pharmacist.notifications'))
    
    notification.is_read = True
    db.session.commit()
    flash('Notification marked as read', 'info')
    return redirect(url_for('pharmacist.notifications'))

@pharmacist.route('/notifications/mark-all-read', methods=['POST'])
def mark_all_notifications_read():
    """Mark all notifications as read for the current user/branch"""
    if current_user.role == 'admin':
        notifications = Notification.query.filter_by(is_read=False).all()
    else:
        notifications = Notification.query.filter(
            db.or_(
                Notification.branch_id == current_user.branch_id,
                Notification.user_id == current_user.id
            ),
            Notification.is_read == False
        ).all()
    
    for notification in notifications:
        notification.is_read = True
    
    db.session.commit()
    flash('All notifications marked as read.', 'success')
    return redirect(url_for('pharmacist.notifications'))

@pharmacist.route('/api/notifications/count')
def get_notification_count():
    """Get unread notification count for AJAX updates"""
    if current_user.role == 'admin':
        unread_count = Notification.query.filter_by(is_read=False).count()
    else:
        unread_count = Notification.query.filter(
            db.or_(
                Notification.branch_id == current_user.branch_id,
                Notification.user_id == current_user.id
            ),
            Notification.is_read == False
        ).count()
    
    
    return jsonify({'unread_count': unread_count})

@pharmacist.route('/reply_inquiry', methods=['POST'])
def reply_inquiry():
    """Handle reply to user inquiry"""
    data = request.get_json()
    user_email = data.get('email')
    message = data.get('message')
    
    print(f"DEBUG: Reply Inquiry Request - Email: {user_email}, Message: {message}")
    
    if not user_email or not message:
        print("DEBUG: Missing email or message")
        return jsonify({'success': False, 'message': 'Missing email or message'})
        
    # Find user by email
    user = User.query.filter_by(email=user_email).first()
    
    if not user:
        print(f"DEBUG: User not found for email {user_email}")
        return jsonify({'success': False, 'message': 'User not found. This feature only works for registered users.'})
        
    # Create notification
    if create_pharmacist_reply_notification(user, message, current_user):
        print(f"DEBUG: Notification created for user {user.username}")
        return jsonify({'success': True})
    else:
        print("DEBUG: Failed to create notification")
        return jsonify({'success': False, 'message': 'Failed to send reply'})