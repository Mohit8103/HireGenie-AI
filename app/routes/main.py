from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('main/landing.html')

@main_bp.route('/page/<page_name>')
def static_page(page_name):
    allowed_pages = {
        'pricing': 'Pricing', 
        'security': 'Security', 
        'privacy': 'Privacy Policy', 
        'terms': 'Terms of Service'
    }
    if page_name not in allowed_pages:
        return "Page not found", 404
    return render_template('main/page.html', title=allowed_pages[page_name])
