from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class JobDescription(db.Model):
    __tablename__ = 'job_descriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100))
    required_skills = db.Column(db.Text, nullable=False) # Store as comma-separated or JSON string
    experience_required = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    match_results = db.relationship('MatchResult', backref='job', lazy=True, cascade="all, delete-orphan")

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    skills = db.Column(db.Text)
    education = db.Column(db.Text)
    experience = db.Column(db.Text)
    certifications = db.Column(db.Text)
    projects = db.Column(db.Text)
    linkedin = db.Column(db.String(255))
    github = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    resume = db.relationship('Resume', backref='candidate', uselist=False, cascade="all, delete-orphan")
    ai_analysis = db.relationship('AiAnalysis', backref='candidate', uselist=False, cascade="all, delete-orphan")
    match_results = db.relationship('MatchResult', backref='candidate', lazy=True, cascade="all, delete-orphan")

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

class AiAnalysis(db.Model):
    __tablename__ = 'ai_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    summary = db.Column(db.Text)
    strengths = db.Column(db.Text)
    weaknesses = db.Column(db.Text)
    skill_assessment = db.Column(db.Text)
    communication_assessment = db.Column(db.Text)
    career_level = db.Column(db.String(100))
    suitability_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MatchResult(db.Model):
    __tablename__ = 'match_results'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False)
    score = db.Column(db.Integer)
    matching_skills = db.Column(db.Text)
    missing_skills = db.Column(db.Text)
    recommendation = db.Column(db.String(50)) # e.g., 'Strong Match', 'Moderate Match', 'Weak Match'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
