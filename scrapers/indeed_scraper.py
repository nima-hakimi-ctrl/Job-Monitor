import requests
from bs4 import BeautifulSoup
import time
import hashlib
from urllib.parse import urlencode
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import job_exists, save_job
from utils.scorer import score_job

def scrape_indeed(query, location, max_results=50):
    """
    Scrape Indeed for job postings.
    
    Args:
        query: Search query string (e.g., "Credit Analyst Intern")
        location: Location string (e.g., "Seattle, WA")
        max_results: Maximum number of results to scrape
    
    Returns:
        List of new jobs found
    """
    
    new_jobs = []
    base_url = "https://www.indeed.com/jobs"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Indeed uses pagination with 'start' parameter (0, 10, 20, etc.)
    for start in range(0, max_results, 10):
        params = {
            'q': query,
            'l': location,
            'start': start,
            'sort': 'date'  # Sort by most recent
        }
        
        url = f"{base_url}?{urlencode(params)}"
        
        try:
            print(f"Scraping Indeed: {query} in {location} (page {start//10 + 1})")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Indeed job cards have specific structure
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            if not job_cards:
                print(f"No job cards found on page {start//10 + 1}. Indeed may have changed structure.")
                break
            
            for card in job_cards:
                try:
                    # Extract job details
                    title_elem = card.find('h2', class_='jobTitle')
                    if not title_elem:
                        continue
                    
                    title_link = title_elem.find('a')
                    if not title_link:
                        title_link = title_elem.find('span', attrs={'title': True})
                    
                    title = title_link.get('title', '') or title_link.get_text(strip=True)
                    
                    # Get job ID from data attribute or link
                    job_key = card.get('data-jk', '')
                    if not job_key:
                        # Try to extract from link
                        link = title_link.get('href', '')
                        if 'jk=' in link:
                            job_key = link.split('jk=')[1].split('&')[0]
                    
                    if not job_key:
                        # Fallback: create hash from title + company
                        company_elem = card.find('span', class_='companyName')
                        company = company_elem.get_text(strip=True) if company_elem else 'Unknown'
                        job_key = hashlib.md5(f"{title}{company}".encode()).hexdigest()[:16]
                    
                    job_id = f"indeed_{job_key}"
                    
                    # Skip if already in database
                    if job_exists(job_id):
                        continue
                    
                    # Extract company
                    company_elem = card.find('span', class_='companyName')
                    company = company_elem.get_text(strip=True) if company_elem else 'Unknown'
                    
                    # Extract location
                    location_elem = card.find('div', class_='companyLocation')
                    job_location = location_elem.get_text(strip=True) if location_elem else location
                    
                    # Extract description snippet
                    desc_elem = card.find('div', class_='job-snippet')
                    description = desc_elem.get_text(strip=True) if desc_elem else ''
                    
                    # Build job URL
                    job_url = f"https://www.indeed.com/viewjob?jk={job_key}"
                    
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
                        'source': 'Indeed',
                        'score': job_score
                    }
                    
                    # Save to database
                    if save_job(job_data):
                        new_jobs.append(job_data)
                        print(f"  ✅ Found: {title} at {company} (Score: {job_score})")
                
                except Exception as e:
                    print(f"  ⚠️  Error parsing job card: {str(e)}")
                    continue
            
            # Be respectful - add delay between pages
            time.sleep(2)
        
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Error fetching Indeed page: {str(e)}")
            break
    
    return new_jobs

def scrape_all_indeed_searches():
    """Run all Indeed searches based on your criteria."""
    
    searches = [
        ("Credit Analyst Intern", "Seattle, WA"),
        ("Credit Analyst Intern", "San Francisco, CA"),
        ("Commercial Banking Intern", "Seattle, WA"),
        ("Commercial Banking Intern", "New York, NY"),
        ("Corporate Banking Intern", "Seattle, WA"),
        ("Corporate Banking Intern", "San Francisco, CA"),
        ("Summer Analyst Corporate Banking", "Seattle, WA"),
        ("Summer Analyst Corporate Banking", "New York, NY"),
        ("Summer Analyst Lending", "United States"),
        ("Investment Analyst Credit", "Remote"),
        ("Underwriting Analyst", "Seattle, WA"),
        ("Direct Lending Analyst", "San Francisco, CA"),
        ("Relationship Banking Analyst", "Seattle, WA"),
    ]
    
    all_new_jobs = []
    
    for query, location in searches:
        jobs = scrape_indeed(query, location, max_results=30)
        all_new_jobs.extend(jobs)
        time.sleep(3)  # Delay between different searches
    
    return all_new_jobs

if __name__ == '__main__':
    from utils.database import init_database
    
    # Initialize database
    init_database()
    
    print("\n" + "="*60)
    print("INDEED JOB SCRAPER")
    print("="*60 + "\n")
    
    new_jobs = scrape_all_indeed_searches()
    
    print("\n" + "="*60)
    print(f"SUMMARY: Found {len(new_jobs)} new jobs")
    print("="*60)
