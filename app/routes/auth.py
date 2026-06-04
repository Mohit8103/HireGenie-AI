from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models import Admin
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(email=email).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('auth/login.html')

from email_validator import validate_email, EmailNotValidError

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Deep Email Validation
        try:
            valid = validate_email(email, check_deliverability=True)
            email = valid.normalized
            
            # Block disposable / temporary emails
            domain = email.split('@')[1]
            try:
                from disposable_email_domains import blocklist
                if domain in blocklist:
                    flash('Disposable or temporary email addresses are not allowed.', 'danger')
                    return redirect(url_for('auth.register'))
            except ImportError:
                pass # Fail silently if package isn't loaded properly
                
        except EmailNotValidError as e:
            flash(f'Invalid email address: {str(e)}', 'danger')
            return redirect(url_for('auth.register'))
            
        admin_exists = Admin.query.filter_by(email=email).first()
        if admin_exists:
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))
            
        new_admin = Admin(name=name, email=email)
        new_admin.set_password(password)
        
        db.session.add(new_admin)
        db.session.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
