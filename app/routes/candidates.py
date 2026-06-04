import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from ..models import Candidate, Resume, AiAnalysis, MatchResult, JobDescription
from ..services.parser import extract_text_from_pdf
from ..services.gemini import analyze_resume, match_candidate_to_job
from .. import db

candidates_bp = Blueprint('candidates', __name__, url_prefix='/candidates')

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@candidates_bp.route('/')
@login_required
def list_candidates():
    # Module 9: Search & Filtering
    search = request.args.get('search', '')
    job_id = request.args.get('job_id', type=int)
    
    query = Candidate.query.filter_by(admin_id=current_user.id)
    if search:
        query = query.filter(Candidate.name.ilike(f'%{search}%') | Candidate.skills.ilike(f'%{search}%'))
    
    if job_id:
        query = query.join(MatchResult).filter(MatchResult.job_id == job_id)
        
    candidates = query.order_by(Candidate.created_at.desc()).all()
    jobs = JobDescription.query.filter_by(admin_id=current_user.id).all()
    
    return render_template('candidates/list.html', candidates=candidates, jobs=jobs)

@candidates_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_resume():
    if request.method == 'POST':
        if 'resumes' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
            
        files = request.files.getlist('resumes')
        target_job_id = request.form.get('job_id')
        
        if not files or files[0].filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        success_count = 0
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                # 1. Parse PDF
                resume_text = extract_text_from_pdf(file_path)
                
                if not resume_text:
                    flash(f'Failed to extract text from {filename}', 'warning')
                    continue
                    
                # 2. Analyze with Gemini
                analysis_data = analyze_resume(resume_text)
                
                if not analysis_data:
                    flash(f'AI Analysis failed for {filename}. Please check your API key.', 'danger')
                    continue
                    
                cand_data = analysis_data.get('candidate', {})
                ai_data = analysis_data.get('analysis', {})
                
                # 3. Save Candidate
                candidate = Candidate(
                    admin_id=current_user.id,
                    name=cand_data.get('name', 'Unknown'),
                    email=cand_data.get('email', ''),
                    phone=cand_data.get('phone', ''),
                    skills=cand_data.get('skills', ''),
                    education=cand_data.get('education', ''),
                    experience=cand_data.get('experience', ''),
                    certifications=cand_data.get('certifications', ''),
                    projects=cand_data.get('projects', ''),
                    linkedin=cand_data.get('linkedin', ''),
                    github=cand_data.get('github', '')
                )
                db.session.add(candidate)
                db.session.flush() # Get candidate ID
                
                # 4. Save Resume record
                resume = Resume(
                    candidate_id=candidate.id,
                    file_name=filename,
                    file_path=file_path
                )
                db.session.add(resume)
                
                # 5. Save AI Analysis
                analysis = AiAnalysis(
                    candidate_id=candidate.id,
                    summary=ai_data.get('summary', ''),
                    strengths=ai_data.get('strengths', ''),
                    weaknesses=ai_data.get('weaknesses', ''),
                    skill_assessment=ai_data.get('skill_assessment', ''),
                    communication_assessment=ai_data.get('communication_assessment', ''),
                    career_level=ai_data.get('career_level', ''),
                    suitability_score=ai_data.get('suitability_score', 0)
                )
                db.session.add(analysis)
                
                # 6. Match against job if selected
                if target_job_id:
                    job = JobDescription.query.filter_by(id=target_job_id, admin_id=current_user.id).first()
                    if job:
                        match_data = match_candidate_to_job(cand_data, ai_data, job.description, job.required_skills)
                        if match_data:
                            match_result = MatchResult(
                                candidate_id=candidate.id,
                                job_id=job.id,
                                score=match_data.get('score', 0),
                                matching_skills=match_data.get('matching_skills', ''),
                                missing_skills=match_data.get('missing_skills', ''),
                                recommendation=match_data.get('recommendation', '')
                            )
                            db.session.add(match_result)
                        
                db.session.commit()
                success_count += 1
                
        if success_count > 0:
            flash(f'Successfully processed {success_count} resume(s).', 'success')
            return redirect(url_for('candidates.list_candidates'))
            
    jobs = JobDescription.query.filter_by(admin_id=current_user.id).all()
    return render_template('candidates/upload.html', jobs=jobs)

@candidates_bp.route('/<int:candidate_id>')
@login_required
def profile(candidate_id):
    candidate = Candidate.query.filter_by(id=candidate_id, admin_id=current_user.id).first_or_404()
    return render_template('candidates/profile.html', candidate=candidate)
