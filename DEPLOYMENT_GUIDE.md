# Job Monitor - Deployment Guide

Complete step-by-step guide to get your job monitoring system running.

---

## 📋 Prerequisites

- GitHub account (free)
- Gmail account with 2FA enabled
- Python 3.8+ (if running locally)

---

## 🚀 Deployment Option 1: GitHub Actions (Recommended)

**Advantage**: Completely free, runs automatically every 6 hours, no server needed.

### Step 1: Set up Gmail App Password

1. Go to your Gmail account → Security settings
2. Enable **2-Factor Authentication** (required)
3. Go to https://myaccount.google.com/apppasswords
4. Create new app password:
   - App: **Mail**
   - Device: **Other (Custom name)** → "Job Monitor"
5. Copy the 16-character password (looks like: `abcd efgh ijkl mnop`)
6. **Save this password** - you'll need it for GitHub Secrets

### Step 2: Create GitHub Repository

```bash
# On your local machine:
cd /path/to/job_monitor
git init
git add .
git commit -m "Initial job monitor setup"

# Create new repo on GitHub.com (name it "job-monitor")
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/job-monitor.git
git branch -M main
git push -u origin main
```

### Step 3: Configure GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** for each of these:

| Secret Name | Value | Example |
|------------|-------|---------|
| `EMAIL_FROM` | Your Gmail address | `nima.yourname@gmail.com` |
| `EMAIL_PASSWORD` | Gmail App Password (from Step 1) | `abcd efgh ijkl mnop` |
| `EMAIL_TO` | Email to receive alerts | `nima.yourname@gmail.com` |
| `KEYWORDS` | Job keywords (comma-separated) | `Credit Analyst,Summer Analyst,Corporate Banking,Commercial Banking,Investment Analyst,Underwriting,Lending,Relationship Banking` |
| `LOCATIONS` | Target locations | `Seattle,Bellevue,San Francisco,Phoenix,New York,Remote` |
| `EXCLUDE_KEYWORDS` | Auto-reject keywords | `Senior,Manager,Director,VP,Vice President` |
| `MIN_SCORE` | Minimum alert score (3-5 recommended) | `3` |
| `COMPANIES` | Target companies | `Wells Fargo,JPMorgan Chase,BMO,KeyBank,Bank of America,Citizens Bank` |

### Step 4: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. You'll see "Job Monitor" workflow listed

### Step 5: First Run

1. In Actions tab, click **Job Monitor** workflow
2. Click **Run workflow** → **Run workflow** (green button)
3. Watch the workflow run (takes 2-5 minutes)
4. Check your email for alerts!

### Step 6: Verify Automated Runs

- Workflow will now run automatically every 6 hours
- Schedule: 12:00 AM, 6:00 AM, 12:00 PM, 6:00 PM UTC
- You can manually trigger anytime via "Run workflow" button

---

## 💻 Deployment Option 2: Local Machine

**Advantage**: More control, can customize scraping frequency, runs on your schedule.

### Step 1: Clone & Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/job-monitor.git
cd job-monitor

# Install Python dependencies
pip install -r requirements.txt

# Run setup wizard
python setup.py
```

The setup wizard will ask for:
- Gmail address
- Gmail App Password (see GitHub guide above)
- Job keywords
- Locations
- Companies to monitor

### Step 2: Test the System

```bash
# Run quick test
python test.py

# This will:
# - Initialize database
# - Test scoring system
# - Test email configuration
# - Try a sample Indeed search
```

### Step 3: Run Manually

```bash
# Run full monitoring cycle
python main.py

# You should see:
# - Web scraping logs
# - Jobs discovered
# - Email sent (if matches found)
```

### Step 4: Automate (Optional)

**On Mac/Linux** - Use cron:

```bash
# Edit crontab
crontab -e

# Add this line (runs every 6 hours):
0 */6 * * * cd /path/to/job_monitor && /usr/bin/python3 main.py >> /path/to/job_monitor/monitor.log 2>&1
```

**On Windows** - Use Task Scheduler:

1. Open Task Scheduler
2. Create Basic Task → "Job Monitor"
3. Trigger: Daily, repeat every 6 hours
4. Action: Start a program
   - Program: `python.exe`
   - Arguments: `C:\path\to\job_monitor\main.py`
   - Start in: `C:\path\to\job_monitor`

---

## 🔧 Customization Guide

### Adjusting Search Criteria

Edit `.env` file or GitHub Secrets:

```bash
# Add more keywords
KEYWORDS=Credit Analyst,Summer Analyst,Corporate Banking,Commercial Banking,Lending,Relationship Banking,Debt Capital Markets

# Focus on specific locations
LOCATIONS=Seattle,Remote

# Raise minimum score for fewer alerts
MIN_SCORE=5
```

### Changing Alert Frequency

**GitHub Actions**: Edit `.github/workflows/monitor.yml`
```yaml
schedule:
  - cron: '0 */12 * * *'  # Every 12 hours instead of 6
```

**Local cron**: Edit crontab
```bash
0 0,12 * * *  # Runs at midnight and noon only
```

### Adding Custom Searches

Edit `scrapers/indeed_scraper.py` → `scrape_all_indeed_searches()`:

```python
searches = [
    ("Credit Analyst Intern", "Seattle, WA"),
    ("Corporate Banking Summer Analyst", "New York, NY"),
    # Add your custom searches:
    ("BDC Investment Analyst", "Remote"),
    ("Direct Lending Associate", "San Francisco, CA"),
]
```

### Modifying Score Weights

Edit `utils/scorer.py`:

```python
# Make location more important
if preferred_loc in location.lower():
    score += 5  # Changed from 3
    
# Prioritize intern roles more
for indicator in STUDENT_INDICATORS:
    if indicator in full_text:
        score += 3  # Changed from 2
```

---

## 🐛 Troubleshooting

### Issue: No email received

**Check:**
1. Gmail App Password is correct (not regular password)
2. 2FA is enabled on Gmail
3. Check spam/promotions folder
4. Run `python utils/emailer.py` to test email directly

**Fix:**
```bash
# Test email system
python -c "from utils.emailer import send_test_email; send_test_email()"
```

### Issue: No jobs found

**Possible causes:**
1. Scrapers are rate-limited (Indeed/LinkedIn block bots)
2. All jobs already seen (check database)
3. Search criteria too narrow

**Fix:**
```bash
# Check what's in database
sqlite3 data/jobs.db "SELECT COUNT(*) FROM jobs;"

# Clear database to re-scan all jobs
rm data/jobs.db
python main.py
```

### Issue: GitHub Actions failing

**Check:**
1. All secrets are set correctly (no typos)
2. Repository is public (or you have Actions minutes)
3. Workflow file syntax is correct

**Fix:**
```bash
# View detailed logs
# Go to Actions tab → failed run → expand steps
```

### Issue: Scrapers not working

**Cause**: Indeed/LinkedIn block automated access

**Solution**: 
- They may block IPs or require JavaScript
- Scrapers work best from residential IPs
- Consider using LinkedIn/Indeed native alerts as backup
- Focus on company career pages (less blocking)

---

## 📊 Monitoring & Maintenance

### View Database Stats

```bash
# Enter SQLite shell
sqlite3 data/jobs.db

# Show all jobs
SELECT title, company, score, discovered_date FROM jobs ORDER BY score DESC LIMIT 20;

# Count by source
SELECT source, COUNT(*) FROM jobs GROUP BY source;

# Average score
SELECT AVG(score) as avg_score, COUNT(*) as total FROM jobs;

# Exit
.quit
```

### Clean Old Jobs

```bash
# Delete jobs older than 90 days
sqlite3 data/jobs.db "DELETE FROM jobs WHERE discovered_date < date('now', '-90 days');"
```

### Backup Database

```bash
# Backup
cp data/jobs.db data/jobs_backup_$(date +%Y%m%d).db

# Restore
cp data/jobs_backup_20260412.db data/jobs.db
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Already in .gitignore
2. **Use App Passwords** - Never use your main Gmail password
3. **Keep secrets secure** - GitHub Secrets are encrypted
4. **Rotate passwords** - Change App Password every 6 months
5. **Limit access** - Only give repository access to yourself

---

## 📈 Optimization Tips

### Reduce False Positives

```bash
# Increase minimum score
MIN_SCORE=5

# Add more exclude keywords
EXCLUDE_KEYWORDS=Senior,Manager,Director,VP,Lead,Principal,Staff
```

### Get More Results

```bash
# Add broader keywords
KEYWORDS=Analyst,Associate,Banking,Finance,Credit

# Expand locations
LOCATIONS=Seattle,Bellevue,Tacoma,Redmond,Remote,United States
```

### Focus on Quality

```bash
# Target specific companies only
COMPANIES=Wells Fargo,JPMorgan Chase,Goldman Sachs

# Narrow keywords
KEYWORDS=Credit Analyst Intern,Summer Analyst Corporate Banking
```

---

## 🆘 Getting Help

1. **Check logs**: 
   - GitHub Actions: Actions tab → Workflow run → Expand steps
   - Local: `tail -f monitor.log`

2. **Test individual components**:
   ```bash
   python test.py                    # Full system test
   python utils/emailer.py          # Email only
   python scrapers/indeed_scraper.py # Indeed only
   python utils/scorer.py           # Scoring only
   ```

3. **Enable debug mode**:
   - Add `print()` statements in scrapers
   - Check `data/jobs.db` to see what was saved

---

## ✅ Success Checklist

- [ ] Gmail App Password created
- [ ] GitHub repository created
- [ ] All 8 secrets configured in GitHub
- [ ] GitHub Actions enabled
- [ ] First manual workflow run completed
- [ ] Test email received
- [ ] Automated runs scheduled (every 6 hours)
- [ ] Database tracking jobs correctly
- [ ] Receiving relevant job alerts

---

**You're all set! 🎉**

The system will now automatically monitor job boards and email you matches every 6 hours.

**Next steps:**
- Monitor your first few email alerts
- Adjust MIN_SCORE if getting too many/few alerts
- Customize keywords based on what you're seeing
- Add more job boards as scrapers (optional)
