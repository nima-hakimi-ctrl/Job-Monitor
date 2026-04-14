# Job Monitor - Quick Start (5 Minutes)

Get automated job alerts in 5 minutes.

---

## 🎯 Goal

Receive emails with relevant job postings every 6 hours, automatically.

---

## ⚡ Setup (GitHub Actions - Free & Automated)

### 1. Gmail App Password (2 min)

1. Go to: https://myaccount.google.com/apppasswords
2. (Enable 2FA first if not enabled)
3. Create password: Mail → Other → "Job Monitor"
4. **Copy the 16-character password**

### 2. GitHub Setup (2 min)

```bash
# Clone this repo
git clone <this-repo-url>
cd job-monitor

# Push to your GitHub account
git remote set-url origin https://github.com/YOUR_USERNAME/job-monitor.git
git push
```

### 3. Add Secrets (1 min)

Go to: Repository → Settings → Secrets → Actions → New secret

Add these **8 secrets**:

```
EMAIL_FROM = your.email@gmail.com
EMAIL_PASSWORD = your 16-char app password
EMAIL_TO = your.email@gmail.com
KEYWORDS = Credit Analyst,Summer Analyst,Corporate Banking,Commercial Banking,Lending,Relationship Banking
LOCATIONS = Seattle,San Francisco,New York,Remote
EXCLUDE_KEYWORDS = Senior,Manager,Director,VP
MIN_SCORE = 3
COMPANIES = Wells Fargo,JPMorgan,BMO,KeyBank
```

### 4. Enable & Run

1. Go to **Actions** tab
2. Enable workflows
3. Click **Job Monitor** → **Run workflow**
4. **Check your email!**

---

## ✅ Done!

- System runs every 6 hours automatically
- You'll receive emails with job matches
- No server needed (runs on GitHub)
- Completely free

---

## 🔧 Customize Later

Edit secrets to change:
- `MIN_SCORE` (3-8): Higher = fewer, better matches
- `KEYWORDS`: Add more job titles you want
- `LOCATIONS`: Add/remove cities

---

## 📖 Full Docs

- **README.md**: Feature overview
- **DEPLOYMENT_GUIDE.md**: Detailed setup & troubleshooting
- **Run locally**: `python setup.py`

---

**That's it! You're monitoring jobs automatically. 🎉**
