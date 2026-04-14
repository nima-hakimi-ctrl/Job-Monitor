# Job Monitor - Project Summary

## 🎯 What We Built

A fully automated job monitoring system that:
- Scrapes Indeed, LinkedIn, and company career pages every 6 hours
- Scores jobs based on your criteria (keywords, location, company)
- Sends you email alerts with high-quality matches only
- Runs completely free on GitHub Actions (no server needed)
- Tracks jobs you've seen to avoid duplicates

---

## 📁 Project Structure

```
job_monitor/
├── main.py                      # Main orchestrator (runs everything)
├── setup.py                     # Interactive setup wizard
├── test.py                      # Quick system test
├── requirements.txt             # Python dependencies
│
├── .github/workflows/
│   └── monitor.yml              # GitHub Actions config (auto-run every 6 hours)
│
├── scrapers/
│   ├── indeed_scraper.py        # Indeed job board scraper
│   ├── linkedin_scraper.py      # LinkedIn jobs scraper
│   └── company_scrapers.py      # Company career page scrapers
│
├── utils/
│   ├── database.py              # SQLite database operations
│   ├── scorer.py                # Job relevance scoring engine
│   └── emailer.py               # Email alert system
│
├── data/
│   └── jobs.db                  # SQLite database (auto-created)
│
└── docs/
    ├── README.md                # Feature overview
    ├── QUICKSTART.md            # 5-minute setup guide
    └── DEPLOYMENT_GUIDE.md      # Complete deployment docs
```

---

## 🚀 How It Works

### 1. **Scraping Phase** (Every 6 Hours)
```
main.py runs:
  ↓
  ├─→ indeed_scraper.py → searches Indeed for matching jobs
  ├─→ linkedin_scraper.py → searches LinkedIn
  └─→ company_scrapers.py → checks company career pages
       ↓
       All results → database.py (saves to jobs.db)
```

### 2. **Scoring Phase**
```
For each job found:
  ↓
  scorer.py analyzes:
    - Title matches target keywords? (+2-5 points)
    - Location matches targets? (+3 points)
    - Student-friendly terms? (+2 points)
    - Target company? (+2 points)
    - Description has keywords? (+1 per keyword)
  ↓
  Final score: 0-15
```

### 3. **Alert Phase**
```
Get jobs with score >= MIN_SCORE:
  ↓
  emailer.py creates HTML email:
    - Job title, company, location
    - Match score badge
    - Description snippet
    - "Apply Now" link
  ↓
  Send to your email
  ↓
  Mark as alerted (won't send again)
```

---

## 🔧 Key Features

### Smart Scoring System
- **Perfect match** (14-15 points): "Credit Analyst Intern" at Wells Fargo in Seattle
- **Strong match** (8-13 points): "Summer Analyst" at JPMorgan (but in NY, not Seattle)
- **Moderate** (4-7 points): "Investment Analyst" at unknown company
- **Weak** (0-3 points): "Credit Analyst Manager" (excluded keyword)

### Deduplication
- Each job gets unique ID (source + job_number)
- Stored in SQLite database
- Never alerts you twice about same job

### Configurable Everything
```
.env file controls:
- Which keywords to search
- Which locations to prefer
- Which companies to target
- Which terms to auto-reject
- Minimum score to alert
```

### Email Alerts
- **HTML formatted**: Professional, clean design
- **Sortable**: Highest scores first
- **One-click apply**: Direct links to job postings
- **Batch alerts**: Groups multiple jobs in one email

---

## 📊 Scoring Examples

### Example 1: Perfect Match (Score: 14)
```
Title: Credit Analyst Intern - Summer 2027
Company: Wells Fargo
Location: Seattle, WA
Description: "Undergraduate students join Corporate Banking team..."

Breakdown:
  +5: Title exactly matches "Credit Analyst Intern"
  +3: Location is Seattle (preferred)
  +2: Student-friendly ("Intern", "Summer 2027", "Undergraduate")
  +2: "Wells Fargo" is target company
  +2: Keywords in title ("Credit", "Analyst")
  ────
  14 points → EMAIL SENT
```

### Example 2: Good Match (Score: 9)
```
Title: Summer Analyst - Corporate Banking
Company: BMO Financial Group
Location: New York, NY
Description: "Join our credit analysis team..."

Breakdown:
  +2: Keywords in title ("Analyst")
  +3: "New York" is preferred location
  +2: Student-friendly ("Summer")
  +2: "BMO" is target company
  ────
  9 points → EMAIL SENT (if MIN_SCORE ≤ 9)
```

### Example 3: Rejected (Score: 0)
```
Title: Senior Credit Analyst Manager
Company: Unknown Bank
Location: Seattle, WA

Breakdown:
  Contains "Senior" → AUTO-REJECTED
  Contains "Manager" → AUTO-REJECTED
  ────
  0 points → IGNORED
```

---

## 🎯 Your Configuration

Based on your background, here's the recommended setup:

```env
KEYWORDS=Credit Analyst,Summer Analyst,Corporate Banking,Commercial Banking,Investment Analyst,Underwriting,Direct Lending,BDC,Lending,Relationship Banking

LOCATIONS=Seattle,Bellevue,San Francisco,New York,Phoenix,Remote

EXCLUDE_KEYWORDS=Senior,Manager,Director,VP,Vice President,Lead,Principal,Staff

MIN_SCORE=3

COMPANIES=Wells Fargo,JPMorgan Chase,BMO,KeyBank,Bank of America,Citizens Bank,Umpqua Bank,Banner Bank,Western Alliance,MUFG
```

This targets:
- ✅ Credit-focused analyst roles
- ✅ Corporate banking summer programs
- ✅ Your target locations (Seattle primary, SF/NY secondary)
- ✅ Your networking companies
- ❌ Senior/management roles

---

## 🔄 Workflow Timeline

```
Hour 0  (12:00 AM UTC / 4:00 PM PST): Run #1
Hour 6  (6:00 AM UTC / 10:00 PM PST):  Run #2
Hour 12 (12:00 PM UTC / 4:00 AM PST):  Run #3
Hour 18 (6:00 PM UTC / 10:00 AM PST):  Run #4
→ Repeat daily
```

Each run:
1. Scrapes all sources (2-3 minutes)
2. Scores new jobs (seconds)
3. Sends email if matches found (seconds)
4. Total: ~5 minutes per run

---

## 📈 Expected Results

### Week 1
- Expect 5-20 jobs in database
- 2-8 email alerts (depending on MIN_SCORE)
- Most will be from Indeed (fastest to scrape)

### Week 2-4
- Database grows to 50-200 jobs
- Fewer alerts (many jobs already seen)
- You'll start recognizing patterns in what scores high

### Ongoing
- New jobs: 1-5 per day
- Alerts: 0-3 per week (good ones only)
- Best use: Catches jobs you'd miss manually

---

## 🛠️ Maintenance

### Weekly
- Check emails, apply to good matches
- Adjust MIN_SCORE if too many/few alerts

### Monthly
- Review scoring in `.env` - add/remove keywords
- Check database size: `sqlite3 data/jobs.db "SELECT COUNT(*) FROM jobs;"`

### Quarterly
- Clear old jobs: `sqlite3 data/jobs.db "DELETE FROM jobs WHERE discovered_date < date('now', '-90 days');"`
- Rotate Gmail App Password (security best practice)

---

## 🎓 Technical Notes

### Why SQLite?
- No server needed
- Perfect for <100K records
- GitHub Actions can commit it back to repo
- You can inspect it locally

### Why GitHub Actions?
- Completely free (2,000 minutes/month free tier)
- No server maintenance
- Runs reliably
- Easy to pause/resume

### Why Email over Slack/SMS?
- No API keys needed (just Gmail)
- Works everywhere
- You already check email
- Can add Slack later if wanted

### Scraper Limitations
- Indeed/LinkedIn may block bots → use sparingly
- Company sites change structure → may break
- Rate limits → built-in delays
- Some sites require JavaScript → need Selenium

---

## 🚦 Next Steps

### Immediate (First Hour)
1. Deploy to GitHub Actions (see QUICKSTART.md)
2. Wait for first run
3. Check email for alerts
4. Apply to good matches!

### Short Term (First Week)
1. Monitor which sources find best jobs
2. Adjust MIN_SCORE based on volume
3. Refine keywords if needed
4. Add companies you're networking with

### Long Term (Ongoing)
1. Track application outcomes
2. Correlate with job score
3. Use data to improve scoring
4. Share with friends recruiting

---

## 📞 Support

### If it breaks:
1. Check DEPLOYMENT_GUIDE.md troubleshooting section
2. Run `python test.py` to diagnose
3. Check GitHub Actions logs
4. Verify Gmail App Password still works

### To customize:
1. Edit `.env` for simple changes (keywords, locations)
2. Edit `utils/scorer.py` for scoring weights
3. Edit scrapers for new sources
4. Fork and modify freely!

---

## ✅ Success Metrics

You'll know it's working when:
- [ ] Email arrives within 6 hours of deployment
- [ ] Jobs in email are actually relevant
- [ ] You apply to at least 1 job per week from alerts
- [ ] You discover jobs you wouldn't have found manually
- [ ] System saves you 30+ minutes/week vs manual checking

---

**Built specifically for your corporate banking recruiting in 2026.**

Target roles: Credit Analyst, Summer Analyst, Corporate Banking
Target companies: Wells Fargo, JPMorgan, BMO, KeyBank, Citizens
Target locations: Seattle (primary), SF, NY, Phoenix

**Good luck with recruiting! 🚀**
