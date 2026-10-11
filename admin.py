
# from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
# from flask_login import login_required, current_user
# from app import db
# from app.models import User, Medicine, Branch, Inventory, Notification
# from app.forms import MedicineForm, BranchForm, UserForm
# from app.utils import admin_required
# from datetime import datetime

# admin = Blueprint('admin', __name__)

# @admin.before_request
# @login_required
# @admin_required
# def require_admin():
#     pass

# @admin.route('/dashboard')
# def dashboard():
#     total_users = User.query.count()
#     total_medicines = Medicine.query.count()
#     total_branches = Branch.query.count()
    
#     # System statistics
#     low_stock_count = Inventory.query.filter(Inventory.quantity <= Inventory.min_stock_level).count()
#     out_of_stock_count = Inventory.query.filter(Inventory.quantity == 0).count()
    
#     # Recent activities
#     recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
#     recent_medicines = Medicine.query.order_by(Medicine.created_at.desc()).limit(5).all()
    
#     return render_template('admin/dashboard.html',
#                          title='Admin Dashboard',
#                          total_users=total_users,
#                          total_medicines=total_medicines,
#                          total_branches=total_branches,
#                          low_stock_count=low_stock_count,
#                          out_of_stock_count=out_of_stock_count,
#                          recent_users=recent_users,
#                          recent_medicines=recent_medicines)

# @admin.route('/users')
# def users():
#     users = User.query.all()
#     return render_template('admin/users.html', title='Manage Users', users=users)

# @admin.route('/user/add', methods=['GET', 'POST'])
# def add_user():
#     form = UserForm()
#     if form.validate_on_submit():
#         user = User(
#             username=form.username.data,
#             email=form.email.data,
#             role=form.role.data,
#             branch_id=form.branch_id.data if form.branch_id.data != 0 else None,
#             is_active=form.is_active.data
#         )
#         user.set_password('default123')  # Default password
#         db.session.add(user)
#         db.session.commit()
#         flash('User added successfully! Default password: default123', 'success')
#         return redirect(url_for('admin.users'))
#     return render_template('admin/user_form.html', form=form, title='Add User')

# @admin.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
# def edit_user(user_id):
#     user = User.query.get_or_404(user_id)
#     form = UserForm(obj=user)
#     if form.validate_on_submit():
#         user.username = form.username.data
#         user.email = form.email.data
#         user.role = form.role.data
#         user.branch_id = form.branch_id.data if form.branch_id.data != 0 else None
#         user.is_active = form.is_active.data
#         db.session.commit()
#         flash('User updated successfully!', 'success')
#         return redirect(url_for('admin.users'))
#     return render_template('admin/user_form.html', form=form, title='Edit User')

# @admin.route('/users/<int:user_id>/approve')
# def approve_user(user_id):
#     user = User.query.get_or_404(user_id)
#     user.role = 'public'  # or 'pharmacist' based on registration
#     db.session.commit()
    
#     # Notify user about approval
#     create_user_notification(user, 'user_approved', admin_user=current_user)
    
#     flash(f'User {user.username} has been approved.', 'success')
#     return redirect(url_for('admin.users'))

# @admin.route('/medicines')
# def medicines():
#     medicines = Medicine.query.all()
#     today = datetime.now().date()
#     return render_template('admin/medicines.html', 
#                          title='Manage Medicines', 
#                          medicines=medicines,
#                          today=today)

# @admin.route('/medicine/add', methods=['GET', 'POST'])
# def add_medicine():
#     form = MedicineForm()
#     if form.validate_on_submit():
#         medicine = Medicine(
#             name=form.name.data,
#             category=form.category.data,
#             description=form.description.data,
#             expiry_date=form.expiry_date.data
#         )
#         db.session.add(medicine)
#         db.session.commit()
#         flash('Medicine added successfully!', 'success')
#         return redirect(url_for('admin.medicines'))
#     return render_template('admin/medicine_form.html', form=form, title='Add Medicine')

# @admin.route('/branches')
# def branches():
#     branches = Branch.query.all()
#     return render_template('admin/branches.html', title='Manage Branches', branches=branches)

# @admin.route('/branch/add', methods=['GET', 'POST'])
# def add_branch():
#     form = BranchForm()
#     if form.validate_on_submit():
#         branch = Branch(
#             name=form.name.data,
#             region=form.region.data,
#             address=form.address.data,
#             phone=form.phone.data
#         )
#         db.session.add(branch)
#         db.session.commit()
#         flash('Branch added successfully!', 'success')
#         return redirect(url_for('admin.branches'))  # Fixed: changed from 'admin.manage_branches' to 'admin.branches'
#     return render_template('admin/branch_form.html', form=form, title='Add Branch')

# @admin.route('/reports')
# def reports():
#     # Generate various reports
#     medicine_distribution = db.session.query(
#         Medicine.category,
#         db.func.count(Medicine.medicine_id)
#     ).group_by(Medicine.category).all()
    
#     regional_stock = db.session.query(
#         Branch.region,
#         db.func.sum(Inventory.quantity)
#     ).join(Inventory).group_by(Branch.region).all()
    
#     return render_template('admin/reports.html',
#                          title='Reports',
#                          medicine_distribution=medicine_distribution,
#                          regional_stock=regional_stock)

# # ADD THE MISSING INVENTORY ROUTES HERE
# @admin.route('/inventory')
# def inventory():
#     """Admin view of all inventory across all branches"""
#     inventory_items = Inventory.query.all()
#     return render_template('admin/inventory.html', 
#                          title='Inventory Management', 
#                          inventory_items=inventory_items)

# @admin.route('/inventory/assign', methods=['GET', 'POST'])
# def assign_inventory():
#     """Assign medicine to branch inventory"""
#     from app.forms import InventoryForm
    
#     form = InventoryForm()
    
#     # Set choices for branches and medicines
#     form.branch_id.choices = [(b.branch_id, b.name) for b in Branch.query.all()]
#     form.medicine_id.choices = [(m.medicine_id, m.name) for m in Medicine.query.all()]
    
#     if form.validate_on_submit():
#         # Check if inventory already exists for this branch-medicine combination
#         existing = Inventory.query.filter_by(
#             branch_id=form.branch_id.data,
#             medicine_id=form.medicine_id.data
#         ).first()
        
#         if existing:
#             flash('This medicine is already in inventory for this branch!', 'warning')
#         else:
#             inventory = Inventory(
#                 branch_id=form.branch_id.data,
#                 medicine_id=form.medicine_id.data,
#                 quantity=form.quantity.data,
#                 min_stock_level=form.min_stock_level.data
#             )
#             db.session.add(inventory)
#             db.session.commit()
#             flash('Medicine successfully added to inventory!', 'success')
#             return redirect(url_for('admin.inventory'))
    
#     return render_template('admin/assign_inventory.html', 
#                          form=form, 
#                          title='Assign Medicine to Inventory')

# # Add the missing delete and toggle routes
# @admin.route('/medicine/<int:medicine_id>/delete', methods=['POST'])
# def delete_medicine(medicine_id):
#     """Delete a medicine"""
#     medicine = Medicine.query.get_or_404(medicine_id)
    
#     try:
#         db.session.delete(medicine)
#         db.session.commit()
#         return jsonify({'success': True, 'message': 'Medicine deleted successfully'})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'success': False, 'message': str(e)}), 500

# @admin.route('/user/<int:user_id>/toggle-status', methods=['POST'])
# def toggle_user_status(user_id):
#     """Toggle user active status"""
#     if user_id == current_user.id:
#         return jsonify({'success': False, 'message': 'Cannot change your own status'}), 400
    
#     user = User.query.get_or_404(user_id)
    
#     try:
#         user.is_active = not user.is_active
#         db.session.commit()
#         return jsonify({'success': True, 'message': 'User status updated successfully'})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'success': False, 'message': str(e)}), 500
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Medicine, Branch, Inventory, Notification
from app.forms import MedicineForm, BranchForm, UserForm
from app.utils import admin_required
from app.notifications import create_user_notification, create_inventory_notification, create_system_notification
from datetime import datetime

admin = Blueprint('admin', __name__)

@admin.before_request
@login_required
@admin_required
def require_admin():
    pass

@admin.route('/dashboard')
def dashboard():
    total_users = User.query.count()
    total_medicines = Medicine.query.count()
    total_branches = Branch.query.count()
    
 
    low_stock_count = Inventory.query.filter(Inventory.quantity <= Inventory.min_stock_level).count()
    out_of_stock_count = Inventory.query.filter(Inventory.quantity == 0).count()
    
  
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_medicines = Medicine.query.order_by(Medicine.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         total_users=total_users,
                         total_medicines=total_medicines,
                         total_branches=total_branches,
                         low_stock_count=low_stock_count,
                         out_of_stock_count=out_of_stock_count,
                         recent_users=recent_users,
                         recent_medicines=recent_medicines)

@admin.route('/users')
def users():
    users = User.query.all()
    return render_template('admin/users.html', title='Manage Users', users=users)

@admin.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data,
            branch_id=form.branch_id.data if form.branch_id.data != 0 else None,
            is_active=form.is_active.data
        )
        user.set_password('default123') 
        db.session.add(user)
        db.session.commit()
        
       
        create_user_notification(user, 'new_user_registered')
        
        flash('User added successfully! Default password: default123', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/user_form.html', form=form, title='Add User')

@admin.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        old_role = user.role
        old_branch_id = user.branch_id
        
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        user.branch_id = form.branch_id.data if form.branch_id.data != 0 else None
        user.is_active = form.is_active.data
        db.session.commit()
        
      
        if old_role != user.role:
            create_user_notification(user, 'role_changed', admin_user=current_user)
        
      
        if old_branch_id != user.branch_id and user.branch_id:
            create_user_notification(user, 'branch_assigned', admin_user=current_user)
        
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/user_form.html', form=form, title='Edit User')

@admin.route('/users/<int:user_id>/approve')
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.role = 'public' 
    db.session.commit()
    
   
    create_user_notification(user, 'user_approved', admin_user=current_user)
    
    flash(f'User {user.username} has been approved.', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/medicines')
def medicines():
    medicines = Medicine.query.all()
    today = datetime.now().date()
    return render_template('admin/medicines.html', 
                         title='Manage Medicines', 
                         medicines=medicines,
                         today=today)

@admin.route('/medicine/add', methods=['GET', 'POST'])
def add_medicine():
    form = MedicineForm()
    if form.validate_on_submit():
        medicine = Medicine(
            name=form.name.data,
            category=form.category.data,
            description=form.description.data,
            expiry_date=form.expiry_date.data
        )
        db.session.add(medicine)
        db.session.commit()
        flash('Medicine added successfully!', 'success')
        return redirect(url_for('admin.medicines'))
    return render_template('admin/medicine_form.html', form=form, title='Add Medicine')

@admin.route('/branches')
def branches():
    branches = Branch.query.all()
    return render_template('admin/branches.html', title='Manage Branches', branches=branches)

@admin.route('/branch/add', methods=['GET', 'POST'])
def add_branch():
    form = BranchForm()
    if form.validate_on_submit():
        branch = Branch(
            name=form.name.data,
            region=form.region.data,
            address=form.address.data,
            phone=form.phone.data
        )
        db.session.add(branch)
        db.session.commit()
        flash('Branch added successfully!', 'success')
        return redirect(url_for('admin.branches'))
    return render_template('admin/branch_form.html', form=form, title='Add Branch')

@admin.route('/reports')
def reports():
    """Generate dynamic reports with real data"""
    from datetime import datetime, timedelta
    from sqlalchemy import func, extract
    
    
    today = datetime.now().date()
    month_start = today.replace(day=1)
    
  
    medicine_distribution = db.session.query(
        Medicine.category,
        func.count(Medicine.medicine_id)
    ).group_by(Medicine.category).all()
    
  
    regional_stock = db.session.query(
        Branch.region,
        func.sum(Inventory.quantity)
    ).join(Inventory).group_by(Branch.region).all()
    
   
    expiring_soon = Medicine.query.filter(
        Medicine.expiry_date <= today + timedelta(days=30),
        Medicine.expiry_date >= today
    ).count()
    
   
    low_stock_count = Inventory.query.filter(
        Inventory.quantity <= Inventory.min_stock_level
    ).count()
    
    
    out_of_stock_count = Inventory.query.filter(
        Inventory.quantity == 0
    ).count()
    
    # User statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    admin_users = User.query.filter_by(role='admin').count()
    pharmacist_users = User.query.filter_by(role='pharmacist').count()
    
    # Branch statistics
    total_branches = Branch.query.count()
    
    # Recent activity (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    recent_notifications = Notification.query.filter(
        Notification.created_at >= week_ago
    ).count()
    
    # Medicine statistics
    total_medicines = Medicine.query.count()
    expired_medicines = Medicine.query.filter(
        Medicine.expiry_date < today
    ).count()
    
    return render_template('admin/reports.html',
                         title='Reports',
                         medicine_distribution=medicine_distribution,
                         regional_stock=regional_stock,
                         expiring_soon=expiring_soon,
                         low_stock_count=low_stock_count,
                         out_of_stock_count=out_of_stock_count,
                         total_users=total_users,
                         active_users=active_users,
                         admin_users=admin_users,
                         pharmacist_users=pharmacist_users,
                         total_branches=total_branches,
                         recent_notifications=recent_notifications,
                         total_medicines=total_medicines,
                         expired_medicines=expired_medicines,
                         today=today)
@admin.route('/inventory')
def inventory():
    """Admin view of all inventory across all branches"""
    inventory_items = Inventory.query.all()
    return render_template('admin/inventory.html', 
                         title='Inventory Management', 
                         inventory_items=inventory_items)

@admin.route('/inventory/assign', methods=['GET', 'POST'])
def assign_inventory():
    """Assign medicine to branch inventory"""
    from app.forms import InventoryForm
    
    form = InventoryForm()
    
    
    form.branch_id.choices = [(b.branch_id, b.name) for b in Branch.query.all()]
    form.medicine_id.choices = [(m.medicine_id, m.name) for m in Medicine.query.all()]
    
    if form.validate_on_submit():
        
        existing = Inventory.query.filter_by(
            branch_id=form.branch_id.data,
            medicine_id=form.medicine_id.data
        ).first()
        
        if existing:
            flash('This medicine is already in inventory for this branch!', 'warning')
        else:
            inventory = Inventory(
                branch_id=form.branch_id.data,
                medicine_id=form.medicine_id.data,
                quantity=form.quantity.data,
                min_stock_level=form.min_stock_level.data
            )
            db.session.add(inventory)
            db.session.commit()
            
        
            if inventory.quantity <= inventory.min_stock_level:
                create_inventory_notification(inventory, 'low_stock')
            
            flash('Medicine successfully added to inventory!', 'success')
            return redirect(url_for('admin.inventory'))
    
    return render_template('admin/assign_inventory.html', 
                         form=form, 
                         title='Assign Medicine to Inventory')

@admin.route('/medicine/<int:medicine_id>/delete', methods=['POST'])
def delete_medicine(medicine_id):
    """Delete a medicine"""
    medicine = Medicine.query.get_or_404(medicine_id)
    
    try:
        db.session.delete(medicine)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Medicine deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin.route('/user/<int:user_id>/toggle-status', methods=['POST'])
def toggle_user_status(user_id):
    """Toggle user active status"""
    if user_id == current_user.id:
        return jsonify({'success': False, 'message': 'Cannot change your own status'}), 400
    
    user = User.query.get_or_404(user_id)
    
    try:
        user.is_active = not user.is_active
        db.session.commit()
        return jsonify({'success': True, 'message': 'User status updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin.route('/notifications/send-system', methods=['POST'])
def send_system_notification():
    """Send system-wide notification"""
    title = request.form.get('title')
    message = request.form.get('message')
    priority = request.form.get('priority', 'medium')
    
    if title and message:
        create_system_notification('system_maintenance', extra_data={
            'title': title,
            'message': message,
            'priority': priority
        })
        flash('System notification sent successfully!', 'success')
    else:
        flash('Title and message are required.', 'error')
    
    return redirect(url_for('admin.dashboard'))