import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(to_email, subject, body):
    """Sends an email notification via SMTP."""
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    if not all([smtp_server, smtp_username, smtp_password]):
        print("Email configuration missing. Skipping email notification.")
        return False
        
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def notify_candidate_status(candidate_name, candidate_email, status, job_title=""):
    """Template for candidate status notification"""
    subject = f"Update on your application {('for ' + job_title) if job_title else ''}"
    
    if status == 'Approved':
        body = f"""
        <html><body>
        <h2>Congratulations, {candidate_name}!</h2>
        <p>We are pleased to inform you that your application has been approved.</p>
        <p>Our team will contact you shortly with next steps.</p>
        </body></html>
        """
    elif status == 'Interview Scheduled':
        body = f"""
        <html><body>
        <h2>Interview Invitation: {candidate_name}</h2>
        <p>We would like to invite you to an interview.</p>
        <p>Please let us know your availability for next week.</p>
        </body></html>
        """
    else:
        body = f"""
        <html><body>
        <h2>Application Update: {candidate_name}</h2>
        <p>Thank you for applying. At this time, we have decided to move forward with other candidates.</p>
        <p>We wish you the best in your job search.</p>
        </body></html>
        """
        
    return send_email(candidate_email, subject, body)
