from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.models import Medicine, Branch, Inventory, Notification
from app import db

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('public/index.html', title='Home')

@main.route('/dashboard')
@login_required
def dashboard():
    # Role-based redirection
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif current_user.role == 'pharmacist':
        return redirect(url_for('pharmacist.dashboard'))
        
    # User Dashboard (Public Users)
    # Get pharmacist replies
    replies = Notification.query.filter_by(
        user_id=current_user.id,
        type='pharmacist_reply'
    ).order_by(Notification.created_at.desc()).limit(10).all()
    
    return render_template('public/user_dashboard.html', 
                         title='My Health Dashboard',
                         replies=replies)

@main.route('/search')
def search_medicines():
    query = request.args.get('q', '')
    region = request.args.get('region', '')
    
    # Base query
    inventory_query = Inventory.query.join(Medicine).join(Branch)
    
    if query:
        inventory_query = inventory_query.filter(Medicine.name.ilike(f'%{query}%'))
    
    if region:
        inventory_query = inventory_query.filter(Branch.region == region)
    
    # Only show items with stock
    inventory_query = inventory_query.filter(Inventory.quantity > 0)
    
    results = inventory_query.all()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request - return JSON
        data = []
        for item in results:
            data.append({
                'medicine_name': item.medicine.name,
                'branch_name': item.branch.name,
                'region': item.branch.region,
                'quantity': item.quantity,
                'address': item.branch.address
            })
        return jsonify(data)
    
    return render_template('public/search.html', 
                         title='Search Medicines',
                         results=results,
                         query=query,
                         region=region)

@main.route('/medicine/<int:medicine_id>')
def medicine_detail(medicine_id):
    medicine = Medicine.query.get_or_404(medicine_id)
    inventory_items = Inventory.query.filter_by(medicine_id=medicine_id).all()
    
    return render_template('public/medicine_detail.html',
                         title=medicine.name,
                         medicine=medicine,
                         inventory_items=inventory_items)

@main.route('/api/medicines')
def api_medicines():
    medicines = Medicine.query.all()
    data = []
    for medicine in medicines:
        data.append({
            'medicine_id': medicine.medicine_id,
            'name': medicine.name,
            'category': medicine.category
        })
    return jsonify(data)

@main.route('/api/inventory/<int:branch_id>')
def api_inventory(branch_id):
    inventory_items = Inventory.query.filter_by(branch_id=branch_id).all()
    data = []
    for item in inventory_items:
        data.append({
            'medicine_name': item.medicine.name,
            'quantity': item.quantity,
            'min_stock_level': item.min_stock_level,
            'status': 'out-of-stock' if item.quantity == 0 else 'low-stock' if item.quantity <= item.min_stock_level else 'available'
        })
    return jsonify(data)