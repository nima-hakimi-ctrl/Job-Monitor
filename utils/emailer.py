import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def send_email_alert(jobs):
    """
    Send email alert with new job listings.
    
    Args:
        jobs: List of job dictionaries to alert about
    """
    if not jobs:
        print("No jobs to alert about")
        return False
    
    # Email configuration
    sender_email = os.getenv('EMAIL_FROM')
    sender_password = os.getenv('EMAIL_PASSWORD')
    recipient_email = os.getenv('EMAIL_TO')
    
    if not all([sender_email, sender_password, recipient_email]):
        print("ERROR: Email credentials not configured in .env file")
        return False
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🎯 {len(jobs)} New Job Match{'es' if len(jobs) > 1 else ''} - {datetime.now().strftime('%b %d, %Y')}"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    # Create HTML email body
    html_body = create_html_email(jobs)
    text_body = create_text_email(jobs)
    
    # Attach both plain text and HTML versions
    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')
    msg.attach(part1)
    msg.attach(part2)
    
    # Send email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        print(f"✅ Email sent successfully to {recipient_email}")
        return True
    
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

def create_html_email(jobs):
    """Create HTML formatted email body."""
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: #1a73e8; color: white; padding: 20px; text-align: center; }}
            .job-card {{ 
                border: 1px solid #ddd; 
                border-radius: 8px; 
                padding: 20px; 
                margin: 20px 0;
                background: #f9f9f9;
            }}
            .job-title {{ color: #1a73e8; font-size: 20px; font-weight: bold; margin-bottom: 10px; }}
            .company {{ font-size: 16px; color: #555; margin-bottom: 5px; }}
            .location {{ color: #777; margin-bottom: 10px; }}
            .score {{ 
                display: inline-block;
                background: #34a853; 
                color: white; 
                padding: 5px 10px; 
                border-radius: 4px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .score.high {{ background: #34a853; }}
            .score.medium {{ background: #fbbc04; }}
            .description {{ 
                color: #666; 
                margin: 15px 0;
                padding: 10px;
                background: white;
                border-left: 3px solid #1a73e8;
            }}
            .apply-btn {{
                display: inline-block;
                background: #1a73e8;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 4px;
                margin-top: 10px;
            }}
            .meta {{ color: #999; font-size: 12px; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 New Job Matches Found</h1>
            <p>{len(jobs)} relevant posting{'s' if len(jobs) > 1 else ''} discovered</p>
        </div>
        
        <div style="padding: 20px;">
    """
    
    for job in sorted(jobs, key=lambda x: x['score'], reverse=True):
        score_class = 'high' if job['score'] >= 8 else 'medium'
        description_snippet = job.get('description', '')[:300] + '...' if len(job.get('description', '')) > 300 else job.get('description', 'No description available')
        
        html += f"""
        <div class="job-card">
            <div class="job-title">{job['title']}</div>
            <div class="company">🏢 {job['company']}</div>
            <div class="location">📍 {job['location']}</div>
            <span class="score {score_class}">Match Score: {job['score']}/15</span>
            
            <div class="description">
                {description_snippet}
            </div>
            
            <a href="{job['url']}" class="apply-btn">View & Apply →</a>
            
            <div class="meta">
                Source: {job['source']} | Discovered: {job['discovered_date'][:10]}
            </div>
        </div>
        """
    
    html += """
        </div>
    </body>
    </html>
    """
    
    return html

def create_text_email(jobs):
    """Create plain text email body."""
    
    text = f"NEW JOB MATCHES - {datetime.now().strftime('%B %d, %Y')}\n"
    text += "=" * 60 + "\n\n"
    text += f"Found {len(jobs)} relevant job posting{'s' if len(jobs) > 1 else ''}:\n\n"
    
    for i, job in enumerate(sorted(jobs, key=lambda x: x['score'], reverse=True), 1):
        text += f"{i}. {job['title']}\n"
        text += f"   Company: {job['company']}\n"
        text += f"   Location: {job['location']}\n"
        text += f"   Match Score: {job['score']}/15\n"
        text += f"   Apply: {job['url']}\n"
        text += f"   Source: {job['source']}\n"
        text += "-" * 60 + "\n\n"
    
    return text

def send_test_email():
    """Send a test email to verify configuration."""
    test_jobs = [{
        'title': 'Credit Analyst Intern - Test',
        'company': 'Test Company',
        'location': 'Seattle, WA',
        'description': 'This is a test job posting to verify email delivery.',
        'url': 'https://example.com',
        'source': 'Test',
        'score': 10,
        'discovered_date': datetime.now().isoformat()
    }]
    
    return send_email_alert(test_jobs)

if __name__ == '__main__':
    print("Testing email system...")
    if send_test_email():
        print("✅ Test email sent successfully!")
    else:
        print("❌ Test email failed. Check your .env configuration.")
