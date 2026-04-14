#!/usr/bin/env python3
"""
Quick test script - Runs a single search to verify everything works
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import init_database, get_stats
from utils.scorer import score_job, format_score_report

def test_system():
    """Run a quick test of the system."""
    
    print("\n" + "="*70)
    print("JOB MONITOR - QUICK TEST")
    print("="*70 + "\n")
    
    # Initialize database
    print("1️⃣ Initializing database...")
    init_database()
    stats = get_stats()
    print(f"   ✅ Database ready: {stats['total_jobs']} jobs stored\n")
    
    # Test scorer
    print("2️⃣ Testing scoring system...")
    test_job = {
        'title': 'Credit Analyst Intern - Summer 2027',
        'company': 'Wells Fargo',
        'location': 'Seattle, WA',
        'description': 'Looking for undergraduate students to join our Corporate Banking team. Will assist with credit underwriting and financial analysis of middle-market companies.'
    }
    
    print(format_score_report(test_job))
    
    # Test email configuration
    print("\n3️⃣ Checking email configuration...")
    from dotenv import load_dotenv
    load_dotenv()
    
    email_from = os.getenv('EMAIL_FROM')
    email_to = os.getenv('EMAIL_TO')
    
    if email_from and email_to:
        print(f"   ✅ Email configured: {email_from} → {email_to}")
        
        send_test = input("\n   Send test email? (y/n): ").strip().lower()
        if send_test == 'y':
            from utils.emailer import send_test_email
            if send_test_email():
                print("   ✅ Test email sent!")
            else:
                print("   ❌ Test email failed")
    else:
        print("   ⚠️  Email not configured. Run setup.py first.")
    
    # Quick scrape test
    print("\n4️⃣ Testing Indeed scraper (1 search)...")
    
    try:
        from scrapers.indeed_scraper import scrape_indeed
        
        jobs = scrape_indeed("Credit Analyst Intern", "Seattle, WA", max_results=10)
        
        if jobs:
            print(f"   ✅ Found {len(jobs)} new jobs")
            print("\n   Top results:")
            for job in jobs[:3]:
                print(f"      • {job['title']} at {job['company']} (Score: {job['score']})")
        else:
            print("   ℹ️  No new jobs found (may be rate-limited or all seen before)")
    
    except Exception as e:
        print(f"   ⚠️  Scraper test: {str(e)}")
        print("      (This is normal in restricted network environments)")
    
    print("\n" + "="*70)
    print("Test complete! If everything passed, you're ready to run:")
    print("  python main.py")
    print("="*70 + "\n")

if __name__ == '__main__':
    test_system()
