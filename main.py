#!/usr/bin/env python3
"""
Job Monitor - Main Orchestrator

This script coordinates all scrapers, scores jobs, and sends email alerts.
Designed to run every 6 hours via GitHub Actions or local cron.
"""

import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import init_database, get_unalerted_jobs, mark_as_alerted, get_stats
from utils.emailer import send_email_alert
from scrapers.indeed_scraper import scrape_all_indeed_searches
from scrapers.linkedin_scraper import scrape_all_linkedin_searches

def main():
    """Main execution flow."""
    
    print("\n" + "="*70)
    print(f"JOB MONITOR - Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    # Initialize database
    init_database()
    
    # Get starting stats
    start_stats = get_stats()
    print(f"📊 Database stats: {start_stats['total_jobs']} total jobs, {start_stats['pending']} unalerted\n")
    
    # Run all scrapers
    all_new_jobs = []
    
    print("🔍 PHASE 1: Web Scraping")
    print("-" * 70)
    
    try:
        print("\n[1/2] Indeed...")
        indeed_jobs = scrape_all_indeed_searches()
        all_new_jobs.extend(indeed_jobs)
        print(f"     Found {len(indeed_jobs)} new jobs on Indeed")
    except Exception as e:
        print(f"     ❌ Indeed scraper failed: {str(e)}")
    
    try:
        print("\n[2/2] LinkedIn...")
        linkedin_jobs = scrape_all_linkedin_searches()
        all_new_jobs.extend(linkedin_jobs)
        print(f"     Found {len(linkedin_jobs)} new jobs on LinkedIn")
    except Exception as e:
        print(f"     ❌ LinkedIn scraper failed: {str(e)}")
    
    print("\n" + "-" * 70)
    print(f"✅ Scraping complete: {len(all_new_jobs)} new jobs discovered")
    
    # Get high-scoring jobs that need alerts
    print("\n📧 PHASE 2: Email Alerts")
    print("-" * 70)
    
    min_score = int(os.getenv('MIN_SCORE', '3'))
    unalerted_jobs = get_unalerted_jobs(min_score=min_score)
    
    if unalerted_jobs:
        print(f"Found {len(unalerted_jobs)} jobs with score >= {min_score}")
        print("\nSending email alert...")
        
        if send_email_alert(unalerted_jobs):
            # Mark jobs as alerted
            for job in unalerted_jobs:
                mark_as_alerted(job['job_id'])
            print(f"✅ Alert sent and {len(unalerted_jobs)} jobs marked as alerted")
        else:
            print("❌ Failed to send email alert")
    else:
        print(f"No jobs found with score >= {min_score}")
    
    # Final stats
    print("\n" + "="*70)
    end_stats = get_stats()
    print(f"📊 Final stats: {end_stats['total_jobs']} total jobs, {end_stats['alerted']} alerted")
    print(f"Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
