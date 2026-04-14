# Deployment Checklist

Quick reference for deploying your job monitoring system.

---

## ✅ Pre-Deployment

- [ ] Gmail account with 2FA enabled
- [ ] GitHub account created
- [ ] Downloaded job_monitor folder

---

## 📧 Step 1: Gmail App Password (2 min)

1. Go to: https://myaccount.google.com/apppasswords
2. Create password: Mail → Other → "Job Monitor"
3. **Copy the 16-character password**
4. Save it somewhere (you'll need it for GitHub Secrets)

---

## 🚀 Step 2: GitHub Setup (3 min)

```bash
cd job_monitor
git init
git add .
git commit -m "Initial setup"

# Create new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/job-monitor.git
git branch -M main
git push -u origin main
```

---

## 🔐 Step 3: Add GitHub Secrets (2 min)

Go to: Repository → Settings → Secrets and variables → Actions

Add these 8 secrets:

| Secret Name | Value | Your Value |
|------------|-------|------------|
| EMAIL_FROM | your.email@gmail.com | _________________ |
| EMAIL_PASSWORD | 16-char app password | _________________ |
| EMAIL_TO | your.email@gmail.com | _________________ |
| KEYWORDS | Credit Analyst,Summer Analyst,Corporate Banking,Commercial Banking,Lending,Relationship Banking | ✅ Use default |
| LOCATIONS | Seattle,Bellevue,San Francisco,New York,Remote | ✅ Use default or customize |
| EXCLUDE_KEYWORDS | Senior,Manager,Director,VP | ✅ Use default |
| MIN_SCORE | 3 | ✅ Use default (adjust later if needed) |
| COMPANIES | Wells Fargo,JPMorgan,BMO,KeyBank,Bank of America | ✅ Use default or customize |

---

## ▶️ Step 4: First Run (1 min)

1. Go to **Actions** tab
2. Click "I understand my workflows, go ahead and enable them"
3. Click **Job Monitor** workflow
4. Click **Run workflow** → **Run workflow** (green button)
5. Watch it run (takes 3-5 minutes)
6. **Check your email!**

---

## 🎯 Success Criteria

Within 6 hours of deployment, you should have:

- [ ] Email received with job matches (if any found)
- [ ] Jobs in email are student-level roles (intern or summer analyst)
- [ ] Jobs match your keywords (credit, banking, lending, etc.)
- [ ] Jobs are in your target locations
- [ ] No alerts about experienced/senior roles

---

## 🔧 Post-Deployment Tuning

### If Getting Too Many Alerts (>10/week)
→ Increase MIN_SCORE to 5 or 8

### If Getting Too Few Alerts (<2/week)
→ Lower MIN_SCORE to 3 or add more KEYWORDS

### If Getting Wrong Type of Jobs
→ Check EXCLUDE_KEYWORDS, add more if needed

---

## 📅 Ongoing Maintenance

### Weekly
- [ ] Check emails, apply to good matches
- [ ] Note which sources find best jobs (Indeed vs LinkedIn)

### Monthly
- [ ] Review MIN_SCORE setting
- [ ] Update COMPANIES list if networking expands
- [ ] Check GitHub Actions logs for errors

### Quarterly
- [ ] Clean old jobs from database (optional)
- [ ] Rotate Gmail App Password (security best practice)

---

## 🐛 Troubleshooting

### No email received?
1. Check spam/promotions folder
2. Verify GitHub Actions ran successfully (Actions tab)
3. Verify all 8 secrets are set correctly
4. Run test: `python utils/emailer.py` locally

### GitHub Actions failing?
1. Check Actions tab for error logs
2. Verify secrets have no typos
3. Ensure repository is public (or has Actions minutes)

### Empty emails (no jobs)?
1. Normal for first few runs (might not find new jobs)
2. Jobs may be filtered by MIN_SCORE
3. Check database: `sqlite3 data/jobs.db "SELECT COUNT(*) FROM jobs;"`

---

## 📊 What to Expect

### First 24 Hours
- System runs 4 times (every 6 hours)
- Likely 1-2 emails with 3-8 jobs total
- All will be student-level roles

### First Week
- 10-30 jobs found
- 5-15 email alerts (depending on MIN_SCORE)
- Mix of new postings and existing listings

### Ongoing (After Week 2)
- 1-5 new jobs per day
- 2-8 email alerts per week
- Only truly new postings (duplicates filtered)

---

## ✨ You're All Set!

**System will now automatically:**
- ✅ Search Indeed + LinkedIn every 6 hours
- ✅ Score jobs based on relevance
- ✅ Email you high-quality student-level matches
- ✅ Track jobs to avoid duplicate alerts
- ✅ Run completely free on GitHub Actions

**Focus on applying, not searching. Good luck with recruiting! 🚀**
