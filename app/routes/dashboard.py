from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from ..models import Candidate, Resume, AiAnalysis, JobDescription, MatchResult
from .. import db
import collections
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    total_candidates = Candidate.query.filter_by(admin_id=current_user.id).count()
    total_jobs = JobDescription.query.filter_by(admin_id=current_user.id).count()
    
    # Calculate average suitability score for current user's candidates
    avg_score = db.session.query(func.avg(AiAnalysis.suitability_score)).join(Candidate).filter(Candidate.admin_id == current_user.id).scalar()
    avg_score = round(avg_score, 1) if avg_score else 0
    
    # Pending Review
    pending_count = Candidate.query.filter_by(admin_id=current_user.id).outerjoin(AiAnalysis).filter(AiAnalysis.id == None).count()
    
    recent_candidates = Candidate.query.filter_by(admin_id=current_user.id).order_by(Candidate.created_at.desc()).limit(5).all()
    
    return render_template('dashboard/index.html', 
                           total_candidates=total_candidates,
                           active_jobs=total_jobs,
                           avg_score=avg_score,
                           pending_count=pending_count,
                           recent_candidates=recent_candidates)

@dashboard_bp.route('/analytics')
@login_required
def analytics():
    # 1. Skills Distribution
    all_candidates = Candidate.query.filter_by(admin_id=current_user.id).all()
    skill_counts = collections.Counter()
    
    for cand in all_candidates:
        if cand.skills:
            # Split by comma and strip whitespace
            skills = [s.strip() for s in cand.skills.split(',')]
            skill_counts.update(skills)
            
    # Get top 6 skills
    top_skills = skill_counts.most_common(6)
    skills_labels = [skill[0] for skill in top_skills]
    skills_data = [skill[1] for skill in top_skills]
    
    # 2. Monthly Trend (Simple grouping by month name)
    month_counts = collections.Counter()
    for cand in all_candidates:
        if cand.created_at:
            month_name = cand.created_at.strftime('%b')
            month_counts[month_name] += 1
            
    # Standardize to last 6 months (simplification for dashboard)
    trend_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'] 
    trend_data = [month_counts.get(m, 0) for m in trend_labels]
    
    # 3. Hiring Funnel
    total_applied = len(all_candidates)
    ai_screened = AiAnalysis.query.join(Candidate).filter(Candidate.admin_id == current_user.id).count()
    interview_count = AiAnalysis.query.join(Candidate).filter(Candidate.admin_id == current_user.id, AiAnalysis.suitability_score >= 70).count()
    offered_count = MatchResult.query.join(Candidate).filter(Candidate.admin_id == current_user.id, MatchResult.recommendation == 'Strong Match').count()
    
    funnel_data = [total_applied, ai_screened, interview_count, offered_count]
    
    # 4. Roles
    # Group by Job Title using SQLAlchemy
    role_stats = db.session.query(
        JobDescription.title, 
        func.count(MatchResult.id)
    ).outerjoin(MatchResult, JobDescription.id == MatchResult.job_id).filter(JobDescription.admin_id == current_user.id).group_by(JobDescription.title).all()
    
    roles_labels = [stat[0] for stat in role_stats]
    roles_data = [stat[1] for stat in role_stats]
    
    return render_template('dashboard/analytics.html', 
                           skills_labels=skills_labels,
                           skills_data=skills_data,
                           trend_labels=trend_labels,
                           trend_data=trend_data,
                           funnel_data=funnel_data,
                           roles_labels=roles_labels,
                           roles_data=roles_data)
