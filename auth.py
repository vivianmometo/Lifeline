from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.notifications import create_user_notification
from app.models import User
from app.forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html', form=form, title='Login')

# @auth.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.dashboard'))
    
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(
#             username=form.username.data,
#             email=form.email.data,
#             role='public'  # Default role for self-registration
#         )
#         user.set_password(form.password.data)
        
#         db.session.add(user)
#         db.session.commit()
        
#         flash('Registration successful! You can now login.', 'success')
#         return redirect(url_for('auth.login'))
    
#     return render_template('auth/register.html', form=form, title='Register')
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        requested_role = form.role.data
        branch_id = form.branch_id.data if requested_role == 'pharmacist' and form.branch_id.data else None
        
        # If public, active immediately. If pharmacist, maybe active too for demo?
        # Let's make them active immediately for now as per user request to "fix" it.
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=requested_role,
            branch_id=branch_id
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Notify admins about new registration
        create_user_notification(user, 'new_user_registered')
        
        flash(f'Account created! You are now registered as {requested_role}. Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))