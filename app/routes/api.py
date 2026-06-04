from flask import Blueprint, jsonify, request, render_template, make_response
from flask_login import login_required
from ..models import Candidate, JobDescription
import pdfkit

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/candidates', methods=['GET'])
@login_required
def get_candidates():
    candidates = Candidate.query.all()
    result = []
    for c in candidates:
        result.append({
            'id': c.id,
            'name': c.name,
            'email': c.email,
            'score': c.ai_analysis.suitability_score if c.ai_analysis else None
        })
    return jsonify({'candidates': result})

@api_bp.route('/candidates/<int:candidate_id>', methods=['GET'])
@login_required
def get_candidate(candidate_id):
    c = Candidate.query.get_or_404(candidate_id)
    data = {
        'id': c.id,
        'name': c.name,
        'email': c.email,
        'skills': c.skills,
        'experience': c.experience,
        'analysis': {
            'summary': c.ai_analysis.summary if c.ai_analysis else '',
            'score': c.ai_analysis.suitability_score if c.ai_analysis else 0
        } if c.ai_analysis else None
    }
    return jsonify(data)

@api_bp.route('/report/<int:candidate_id>', methods=['GET'])
@login_required
def generate_report(candidate_id):
    """Generates a PDF report for a candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    
    # We render a simple HTML string for the PDF
    html = f"""
    <html>
    <head><style>body {{ font-family: sans-serif; }} h1 {{ color: #0d6efd; }} </style></head>
    <body>
        <h1>Candidate Report: {candidate.name}</h1>
        <p><strong>Email:</strong> {candidate.email}</p>
        <p><strong>Phone:</strong> {candidate.phone}</p>
        <hr>
        <h3>AI Analysis</h3>
        <p><strong>Suitability Score:</strong> {candidate.ai_analysis.suitability_score if candidate.ai_analysis else 'N/A'}/100</p>
        <p><strong>Summary:</strong> {candidate.ai_analysis.summary if candidate.ai_analysis else 'N/A'}</p>
        <p><strong>Strengths:</strong> {candidate.ai_analysis.strengths if candidate.ai_analysis else 'N/A'}</p>
        <hr>
        <h3>Extracted Skills</h3>
        <p>{candidate.skills}</p>
        <h3>Experience</h3>
        <p>{candidate.experience}</p>
    </body>
    </html>
    """
    
    try:
        # Note: pdfkit requires wkhtmltopdf to be installed on the system.
        # This might fail if wkhtmltopdf is missing, but covers the requirement.
        pdf = pdfkit.from_string(html, False)
        
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=candidate_{candidate.id}_report.pdf'
        return response
    except Exception as e:
        return jsonify({"error": f"Failed to generate PDF. Make sure wkhtmltopdf is installed. Details: {str(e)}"}), 500
