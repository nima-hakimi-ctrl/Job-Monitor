import requests
from bs4 import BeautifulSoup
import time
import hashlib
from urllib.parse import urlencode, quote
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import job_exists, save_job
from utils.scorer import score_job

def scrape_linkedin(query, location, max_results=25):
    """
    Scrape LinkedIn jobs using their public job search.
    
    Note: LinkedIn heavily rate-limits and may require authentication for full access.
    This uses the public job search page which is more limited but doesn't require login.
    
    Args:
        query: Search query string
        location: Location string
        max_results: Maximum results to retrieve
    
    Returns:
        List of new jobs found
    """
    
    new_jobs = []
    
    # LinkedIn job search URL
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    # Build search parameters
    params = {
        'keywords': query,
        'location': location,
        'sortBy': 'DD',  # Sort by date (most recent)
        'f_TPR': 'r86400',  # Last 24 hours (r604800 = last week)
        'start': 0
    }
    
    try:
        print(f"Scraping LinkedIn: {query} in {location}")
        
        # LinkedIn pagination
        for start in range(0, min(max_results, 100), 25):
            params['start'] = start
            
            url = f"{base_url}?{urlencode(params)}"
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job cards
            job_cards = soup.find_all('li')
            
            if not job_cards:
                print(f"  No more jobs found at offset {start}")
                break
            
            for card in job_cards:
                try:
                    # Find the job link
                    link = card.find('a', class_='base-card__full-link')
                    if not link:
                        continue
                    
                    job_url = link.get('href', '')
                    if not job_url:
                        continue
                    
                    # Extract job ID from URL
                    if '/jobs/view/' in job_url:
                        job_key = job_url.split('/jobs/view/')[1].split('?')[0]
                    else:
                        continue
                    
                    job_id = f"linkedin_{job_key}"
                    
                    # Skip if exists
                    if job_exists(job_id):
                        continue
                    
                    # Extract title
                    title_elem = card.find('h3', class_='base-search-card__title')
                    title = title_elem.get_text(strip=True) if title_elem else 'Unknown Title'
                    
                    # Extract company
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    if not company_elem:
                        company_elem = card.find('a', class_='hidden-nested-link')
                    company = company_elem.get_text(strip=True) if company_elem else 'Unknown Company'
                    
                    # Extract location
                    location_elem = card.find('span', class_='job-search-card__location')
                    job_location = location_elem.get_text(strip=True) if location_elem else location
                    
                    # Extract description snippet
                    desc_elem = card.find('p', class_='base-search-card__snippet')
                    description = desc_elem.get_text(strip=True) if desc_elem else ''
                    
                    # Score the job
                    job_score, reasons = score_job(title, description, job_location, company)
                    
                    # Prepare job data
                    job_data = {
                        'job_id': job_id,
                        'title': title,
                        'company': company,
                        'location': job_location,
                        'description': description,
                        'url': job_url,
                        'source': 'LinkedIn',
                        'score': job_score
                    }
                    
                    # Save to database
                    if save_job(job_data):
                        new_jobs.append(job_data)
                        print(f"  ✅ Found: {title} at {company} (Score: {job_score})")
                
                except Exception as e:
                    print(f"  ⚠️  Error parsing job: {str(e)}")
                    continue
            
            # Respectful delay
            time.sleep(3)
    
    except Exception as e:
        print(f"  ❌ LinkedIn scraping error: {str(e)}")
    
    return new_jobs

def scrape_all_linkedin_searches():
    """Run all LinkedIn job searches."""
    
    searches = [
        ("Credit Analyst Intern", "Seattle, Washington"),
        ("Credit Analyst Intern", "San Francisco, California"),
        ("Commercial Banking Intern", "Seattle, Washington"),
        ("Commercial Banking Intern", "United States"),
        ("Corporate Banking Intern", "Seattle, Washington"),
        ("Corporate Banking Intern", "United States"),
        ("Summer Analyst Corporate Banking", "United States"),
        ("Summer Analyst Lending", "United States"),
        ("Investment Analyst Direct Lending", "Remote"),
        ("Corporate Banking Analyst", "Seattle, Washington"),
        ("Relationship Banking Analyst", "United States"),
        ("BDC Analyst", "United States"),
    ]
    
    all_new_jobs = []
    
    for query, location in searches:
        jobs = scrape_linkedin(query, location)
        all_new_jobs.extend(jobs)
        time.sleep(5)  # Longer delay between searches
    
    return all_new_jobs

if __name__ == '__main__':
    from utils.database import init_database
    
    init_database()
    
    print("\n" + "="*60)
    print("LINKEDIN JOB SCRAPER")
    print("="*60 + "\n")
    
    new_jobs = scrape_all_linkedin_searches()
    
    print("\n" + "="*60)
    print(f"SUMMARY: Found {len(new_jobs)} new jobs")
    print("="*60)
