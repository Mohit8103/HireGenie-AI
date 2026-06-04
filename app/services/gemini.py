from google import genai
import os
import json

def get_client():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None

def analyze_resume(resume_text):
    """Uses Gemini to parse candidate info and provide an AI analysis from a resume."""
    client = get_client()
    if not client:
        return None
        
    prompt = f"""
    You are an expert technical recruiter and resume analyzer.
    Parse the following resume text and extract the candidate's details and provide an AI assessment.
    
    Return the response ONLY as a valid JSON object with the following structure:
    {{
        "candidate": {{
            "name": "string",
            "email": "string",
            "phone": "string",
            "skills": "comma separated string",
            "education": "string",
            "experience": "string",
            "certifications": "string",
            "projects": "string",
            "linkedin": "url string",
            "github": "url string"
        }},
        "analysis": {{
            "summary": "2-3 sentences summarizing the candidate",
            "strengths": "bullet points or comma separated",
            "weaknesses": "bullet points or comma separated",
            "skill_assessment": "paragraph assessing technical skills",
            "communication_assessment": "paragraph assessing communication based on resume writing",
            "career_level": "Junior, Mid-Level, Senior, Lead, etc.",
            "suitability_score": int (0-100 score of general professional quality)
        }}
    }}
    
    Resume Text:
    {resume_text}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        # Strip markdown formatting if present
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.endswith('```'):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        print(f"Error in Gemini analyze_resume: {e}")
        return None

def match_candidate_to_job(candidate_data, ai_analysis_data, job_description_text, job_skills):
    """Compares the candidate profile against a job description."""
    client = get_client()
    if not client:
        return None
        
    prompt = f"""
    You are an expert technical recruiter. Compare the candidate profile with the job description and evaluate the match.
    
    Candidate Skills: {candidate_data.get('skills', '')}
    Candidate Experience: {candidate_data.get('experience', '')}
    Candidate AI Summary: {ai_analysis_data.get('summary', '')}
    
    Job Requirements: {job_description_text}
    Required Skills: {job_skills}
    
    Return the response ONLY as a valid JSON object with the following structure:
    {{
        "score": int (0-100 representing how well the candidate matches the job),
        "matching_skills": "comma separated string of matching skills",
        "missing_skills": "comma separated string of required skills the candidate lacks",
        "recommendation": "Strong Match, Moderate Match, or Weak Match"
    }}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.endswith('```'):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        print(f"Error in Gemini match_candidate_to_job: {e}")
        return None

