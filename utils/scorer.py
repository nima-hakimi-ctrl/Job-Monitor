import os
from dotenv import load_dotenv

load_dotenv()

# Load keywords from environment or use defaults
POSITIVE_KEYWORDS = os.getenv('KEYWORDS', 'Credit Analyst,Summer Analyst,Corporate Banking,Commercial Banking,Investment Analyst,Underwriting,Direct Lending,BDC,Lending,Relationship Banking').split(',')
POSITIVE_KEYWORDS = [kw.strip().lower() for kw in POSITIVE_KEYWORDS]

LOCATIONS = os.getenv('LOCATIONS', 'Seattle,Bellevue,San Francisco,Phoenix,New York,Remote').split(',')
LOCATIONS = [loc.strip().lower() for loc in LOCATIONS]

EXCLUDE_KEYWORDS = os.getenv('EXCLUDE_KEYWORDS', 'Senior,Manager,Director,VP,Vice President').split(',')
EXCLUDE_KEYWORDS = [kw.strip().lower() for kw in EXCLUDE_KEYWORDS]

# Title-specific high-value keywords
HIGH_VALUE_TITLES = [
    'credit analyst intern',
    'summer analyst',
    'corporate banking analyst',
    'investment analyst',
    'underwriting analyst',
    'credit associate',
    'commercial banking intern',
    'corporate banking intern',
    'summer analyst intern',
    'lending analyst',
    'relationship banking',
    'corporate banking summer analyst',
    'commercial banking summer analyst'
]

# Student-friendly indicators
STUDENT_INDICATORS = [
    'intern',
    'internship',
    'degree in progress',
    'current student',
    'undergraduate',
    'part-time',
    'summer 2026',
    'summer 2027',
    'summer 2028'
]

# Critical student-level terms (must have at least one for high score)
STUDENT_LEVEL_TERMS = ['intern', 'internship', 'summer analyst', 'analyst intern', 'summer 2026', 'summer 2027', 'summer 2028']

def score_job(title, description, location, company):
    """
    Score a job posting based on relevance.
    
    Returns: (score, reasons) tuple
    - score: integer score (higher = more relevant)
    - reasons: list of strings explaining the score
    """
    score = 0
    reasons = []
    
    # Combine all text for analysis
    full_text = f"{title} {description} {location}".lower()
    title_lower = title.lower()
    
    # DISQUALIFIERS - Auto-reject
    for exclude in EXCLUDE_KEYWORDS:
        if exclude in title_lower:
            return (0, [f"Excluded: Contains '{exclude}' in title"])
    
    # CHECK: Must be student-level role (intern OR summer analyst)
    is_student_level = False
    for term in STUDENT_LEVEL_TERMS:
        if term in title_lower or term in description.lower():
            is_student_level = True
            break
    
    # If not student-level, cap the max score (prevents experienced roles from scoring high)
    max_score_cap = 15 if is_student_level else 6
    
    # HIGH VALUE: Perfect title match
    for high_value in HIGH_VALUE_TITLES:
        if high_value in title_lower:
            score += 5
            reasons.append(f"+5: Title matches '{high_value}'")
            break
    
    # BONUS: Contains "Summer Analyst" OR "Intern" in title (extra emphasis)
    if 'summer analyst' in title_lower:
        score += 3
        reasons.append(f"+3: 'Summer Analyst' in title")
    elif 'intern' in title_lower and 'internship' not in title_lower:
        score += 3
        reasons.append(f"+3: 'Intern' in title")
    
    # MEDIUM VALUE: Student-friendly indicators
    for indicator in STUDENT_INDICATORS:
        if indicator in full_text:
            score += 2
            reasons.append(f"+2: Student-friendly ('{indicator}')")
            break  # Only count once
    
    # KEYWORD MATCHING: Positive keywords in title (higher weight)
    title_keyword_count = 0
    for keyword in POSITIVE_KEYWORDS:
        if keyword in title_lower:
            score += 2
            title_keyword_count += 1
    if title_keyword_count > 0:
        reasons.append(f"+{title_keyword_count * 2}: {title_keyword_count} keywords in title")
    
    # KEYWORD MATCHING: Positive keywords in description (lower weight)
    desc_keyword_count = 0
    for keyword in POSITIVE_KEYWORDS:
        if keyword in description.lower():
            score += 1
            desc_keyword_count += 1
    if desc_keyword_count > 0:
        reasons.append(f"+{desc_keyword_count}: {desc_keyword_count} keywords in description")
    
    # LOCATION MATCHING
    location_match = False
    for preferred_loc in LOCATIONS:
        if preferred_loc in location.lower():
            score += 3
            reasons.append(f"+3: Preferred location ('{preferred_loc}')")
            location_match = True
            break
    
    # COMPANY BONUS: Target companies
    target_companies = os.getenv('COMPANIES', '').split(',')
    target_companies = [c.strip().lower() for c in target_companies if c.strip()]
    
    for target in target_companies:
        if target in company.lower():
            score += 2
            reasons.append(f"+2: Target company ('{company}')")
            break
    
    # MINIMUM VIABILITY: Must have at least one keyword match
    if title_keyword_count == 0 and desc_keyword_count == 0:
        score = 0
        reasons = ["No relevant keywords found"]
    
    # Apply student-level cap (prevents experienced roles from scoring high)
    if score > max_score_cap:
        original_score = score
        score = max_score_cap
        if not is_student_level:
            reasons.append(f"⚠️ Capped at {max_score_cap} (not student-level role)")
    
    return (score, reasons)

def format_score_report(job_data):
    """Generate a human-readable score report for a job."""
    score, reasons = score_job(
        job_data['title'],
        job_data.get('description', ''),
        job_data.get('location', ''),
        job_data['company']
    )
    
    report = f"Job: {job_data['title']} at {job_data['company']}\n"
    report += f"Score: {score}\n"
    report += "Reasoning:\n"
    for reason in reasons:
        report += f"  - {reason}\n"
    
    return report

if __name__ == '__main__':
    # Test scoring
    test_job = {
        'title': 'Credit Analyst Intern - Summer 2027',
        'company': 'Wells Fargo',
        'location': 'Seattle, WA',
        'description': 'Looking for undergraduate students to join our Corporate Banking team. Will assist with credit underwriting and financial analysis.'
    }
    
    print(format_score_report(test_job))
