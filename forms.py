from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Register as', choices=[
        ('public', 'Public User'),
        ('pharmacist', 'Pharmacist')
    ], validators=[DataRequired()])
    branch_id = SelectField('Select Branch (Pharmacists Only)', coerce=int, validators=[Optional()])
    submit = SubmitField('Register')
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        from app.models import Branch
        self.branch_id.choices = [(0, 'Select Branch')] + [(b.branch_id, b.name) for b in Branch.query.all()]

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class MedicineForm(FlaskForm):
    name = StringField('Medicine Name', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Category', choices=[
        ('antibiotic', 'Antibiotic'),
        ('analgesic', 'Analgesic'),
        ('antiviral', 'Antiviral'),
        ('vitamin', 'Vitamin'),
        ('cardiac', 'Cardiac'),
        ('diabetes', 'Diabetes'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Description')
    expiry_date = DateField('Expiry Date', validators=[DataRequired()])
    submit = SubmitField('Add Medicine')

class BranchForm(FlaskForm):
    name = StringField('Branch Name', validators=[DataRequired(), Length(max=100)])
    region = SelectField('Region', choices=[
        ('north', 'North Region'),
        ('south', 'South Region'),
        ('east', 'East Region'),
        ('west', 'West Region'),
        ('central', 'Central Region')
    ], validators=[DataRequired()])
    address = TextAreaField('Address')
    phone = StringField('Phone Number')
    submit = SubmitField('Add Branch')

class InventoryForm(FlaskForm):
    # branch_id = SelectField('Branch', coerce=int, validators=[DataRequired()])
    # medicine_id = SelectField('Medicine', coerce=int, validators=[DataRequired()])
    # quantity = IntegerField('Quantity', validators=[DataRequired()])
    # min_stock_level = IntegerField('Minimum Stock Level', default=10)
    # submit = SubmitField('Update Inventory')
    branch_id = SelectField('Branch', coerce=int, validators=[DataRequired()])
    medicine_id = SelectField('Medicine', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Initial Quantity', validators=[DataRequired()], default=0)
    min_stock_level = IntegerField('Minimum Stock Level', default=10)
    submit = SubmitField('Add to Inventory')

# class UserForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     role = SelectField('Role', choices=[
#         ('admin', 'Administrator'),
#         ('pharmacist', 'Pharmacist'),
#         ('public', 'Public User')
#     ], validators=[DataRequired()])
#     is_active = BooleanField('Active', default=True)
#     submit = SubmitField('Save User')
class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[
        ('admin', 'Administrator'),
        ('pharmacist', 'Pharmacist'),
        ('public', 'Public User')
    ], validators=[DataRequired()])
    branch_id = SelectField('Assigned Branch', coerce=int)  # Add this line
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save User')
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Set branch choices dynamically
        from app.models import Branch
        self.branch_id.choices = [(0, 'No Branch')] + [(b.branch_id, b.name) for b in Branch.query.all()]
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')