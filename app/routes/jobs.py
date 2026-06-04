from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import JobDescription
from .. import db

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/')
@login_required
def list_jobs():
    jobs = JobDescription.query.filter_by(admin_id=current_user.id).order_by(JobDescription.created_at.desc()).all()
    return render_template('jobs/list.html', jobs=jobs)

@jobs_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_job():
    if request.method == 'POST':
        title = request.form.get('title')
        department = request.form.get('department')
        required_skills = request.form.get('required_skills')
        experience_required = request.form.get('experience_required')
        description = request.form.get('description')
        
        new_job = JobDescription(
            admin_id=current_user.id,
            title=title,
            department=department,
            required_skills=required_skills,
            experience_required=experience_required,
            description=description
        )
        db.session.add(new_job)
        db.session.commit()
        
        flash('Job description created successfully.', 'success')
        return redirect(url_for('jobs.list_jobs'))
        
    return render_template('jobs/create.html')

@jobs_bp.route('/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = JobDescription.query.filter_by(id=job_id, admin_id=current_user.id).first_or_404()
    if request.method == 'POST':
        job.title = request.form.get('title')
        job.department = request.form.get('department')
        job.required_skills = request.form.get('required_skills')
        job.experience_required = request.form.get('experience_required')
        job.description = request.form.get('description')
        
        db.session.commit()
        flash('Job description updated successfully.', 'success')
        return redirect(url_for('jobs.list_jobs'))
        
    return render_template('jobs/create.html', job=job)

@jobs_bp.route('/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    job = JobDescription.query.filter_by(id=job_id, admin_id=current_user.id).first_or_404()
    db.session.delete(job)
    db.session.commit()
    flash('Job description deleted successfully.', 'success')
    return redirect(url_for('jobs.list_jobs'))
