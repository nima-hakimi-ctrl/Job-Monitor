# Job Monitor - Automated Job Alert System

Automated system that scrapes job boards, scores postings based on your criteria, and emails you high-quality matches every 6 hours.

## Features

- ✅ **Multi-source scraping**: Indeed, LinkedIn, company career pages
- 🎯 **Smart scoring**: Ranks jobs based on relevance to your search criteria
- 📧 **Email alerts**: Beautiful HTML emails with high-scoring matches
- 🗄️ **Deduplication**: Tracks jobs you've already seen
- ⚙️ **Automated**: Runs every 6 hours via GitHub Actions (free)

## Quick Start

### Option 1: Run on GitHub Actions (Recommended - Free & Automated)

1. **Fork this repository** to your GitHub account

2. **Set up GitHub Secrets** (Settings → Secrets and variables → Actions → New repository secret):

   Required secrets:
   ```
   EMAIL_FROM: your_gmail@gmail.com
   EMAIL_PASSWORD: your_gmail_app_password (see below)
   EMAIL_TO: your_email@gmail.com
   KEYWORDS: Credit Analyst,Summer Analyst,Corporate Banking,Investment Analyst
   LOCATIONS: Seattle,Bellevue,San Francisco,Remote
   EXCLUDE_KEYWORDS: Senior,Manager,Director,VP
   MIN_SCORE: 3
   COMPANIES: Wells Fargo,JPMorgan,BMO,KeyBank
   ```

3. **Enable GitHub Actions**:
   - Go to Actions tab
   - Click "I understand my workflows, go ahead and enable them"

4. **First run**:
   - Go to Actions → Job Monitor → Run workflow
   - Monitor the run to verify it works

5. **Automated runs**: Will now run every 6 hours automatically

### Option 2: Run Locally

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd job_monitor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.template .env
   # Edit .env with your settings
   ```

4. **Run manually**:
   ```bash
   python main.py
   ```

5. **Run on schedule** (Linux/Mac):
   ```bash
   # Edit crontab
   crontab -e
   
   # Add this line to run every 6 hours:
   0 */6 * * * cd /path/to/job_monitor && python main.py
   ```

## Gmail Setup (Required for Emails)

1. **Enable 2-Factor Authentication** on your Gmail account

2. **Create App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other" → name it "Job Monitor"
   - Copy the 16-character password
   - Use this as `EMAIL_PASSWORD`

3. **If you get "Less secure app" errors**: Make sure you're using an App Password, not your regular Gmail password

## Configuration

### Customizing Search Criteria

Edit `.env` or GitHub Secrets:

**KEYWORDS**: Job titles and terms to search for
```
KEYWORDS=Credit Analyst,Summer Analyst,Corporate Banking,Investment Analyst,Underwriting,Direct Lending,BDC
```

**LOCATIONS**: Target locations (case-insensitive)
```
LOCATIONS=Seattle,Bellevue,San Francisco,Phoenix,New York,Remote
```

**EXCLUDE_KEYWORDS**: Auto-reject titles containing these
```
EXCLUDE_KEYWORDS=Senior,Manager,Director,VP,Vice President
```

**MIN_SCORE**: Minimum relevance score to trigger email (0-15 scale)
```
MIN_SCORE=3
```

### Scoring System

Jobs are scored 0-15 based on:
- **+5**: Perfect title match (e.g., "Credit Analyst Intern")
- **+3**: Preferred location match
- **+2**: Student-friendly keywords (intern, degree in progress, etc.)
- **+2**: Keywords in title
- **+2**: Target company
- **+1**: Keywords in description

**Example scores**:
- 14-15: Perfect match (definitely apply)
- 8-13: Strong match (review carefully)
- 4-7: Moderate match (worth a look)
- 0-3: Weak match (probably ignore)

## File Structure

```
job_monitor/
├── main.py                 # Main orchestrator
├── requirements.txt        # Python dependencies
├── .env.template          # Configuration template
├── .github/
│   └── workflows/
│       └── monitor.yml    # GitHub Actions workflow
├── scrapers/
│   ├── indeed_scraper.py
│   ├── linkedin_scraper.py
│   └── company_scrapers.py
├── utils/
│   ├── database.py        # SQLite operations
│   ├── scorer.py          # Job scoring logic
│   └── emailer.py         # Email alerts
└── data/
    └── jobs.db            # SQLite database (auto-created)
```

## Troubleshooting

### Email not sending
- Verify you're using a Gmail App Password (not regular password)
- Check spam folder
- Run `python utils/emailer.py` to send test email

### No jobs found
- Scrapers may be rate-limited (Indeed/LinkedIn block automated access)
- Try running at different times
- Check if sites changed their HTML structure

### GitHub Actions failing
- Check Actions tab for error logs
- Verify all secrets are set correctly
- Ensure repository is public (or you have Actions minutes)

## Advanced Customization

### Adding New Job Sources

1. Create new scraper in `scrapers/`
2. Import and call in `main.py`
3. Follow the pattern from existing scrapers

### Changing Alert Frequency

Edit `.github/workflows/monitor.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Change */6 to */12 for every 12 hours
```

### Adding Slack Alerts

Modify `utils/emailer.py` to include Slack webhook support

## Database Management

View your job database:
```bash
sqlite3 data/jobs.db

# Show all tables
.tables

# View recent jobs
SELECT title, company, score, discovered_date FROM jobs ORDER BY discovered_date DESC LIMIT 10;

# Stats
SELECT COUNT(*) as total, AVG(score) as avg_score FROM jobs;
```

## Privacy & Security

- **API keys**: Stored as GitHub Secrets (encrypted)
- **Database**: Contains only public job postings
- **Rate limiting**: Built-in delays to respect site policies
- **No authentication bypass**: Only scrapes public pages

## License

MIT License - Feel free to modify and use

## Support

Issues? Create a GitHub issue or modify the code to fit your needs.

---

**Built for corporate banking recruiting in 2026**
Optimized for: Credit Analyst, Summer Analyst, Corporate Banking, Direct Lending roles
