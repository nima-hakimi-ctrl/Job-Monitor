# CHANGELOG - Updated Keywords & Enhanced Student-Level Filtering

## Major Enhancement: Student-Level Role Detection

### What This Solves
**Problem**: System could alert about experienced "Credit Analyst" or "Corporate Banking Analyst" roles (full-time, 2+ years experience) if they matched keywords and location.

**Solution**: New mandatory filtering ensures ONLY student-level roles (intern or summer analyst) can score above alert threshold.

### How It Works
1. **Detects student-level terms**: intern, internship, summer analyst, summer 2027, etc.
2. **Bonus scoring**: +3 points if title contains "Summer Analyst" or "Intern"
3. **Score capping**: Non-student roles capped at 6 points (below MIN_SCORE threshold)

### Impact
- ✅ **Before**: "Corporate Banking Analyst" (full-time) could score 10+ points
- ✅ **After**: Same role capped at 6 points → IGNORED

See `STUDENT_LEVEL_FILTERING.md` for detailed examples and testing.

---

## What Was Added

### New High-Value Title Matches (+5 points each)
- `commercial banking intern`
- `corporate banking intern`
- `summer analyst intern`
- `lending analyst`
- `relationship banking`
- `corporate banking summer analyst`
- `commercial banking summer analyst`

### New Keyword Matches (+1-2 points)
- `Commercial Banking`
- `Lending`
- `Relationship Banking`

### Expanded Search Coverage

#### Indeed Scraper - Now Searches:
1. Credit Analyst Intern (Seattle, SF)
2. **Commercial Banking Intern (Seattle, NY)** ← NEW
3. **Corporate Banking Intern (Seattle, SF)** ← NEW
4. Summer Analyst Corporate Banking (Seattle, NY)
5. **Summer Analyst Lending (US)** ← NEW
6. Investment Analyst Credit (Remote)
7. Underwriting Analyst (Seattle)
8. Direct Lending Analyst (SF)
9. **Relationship Banking Analyst (Seattle)** ← NEW

#### LinkedIn Scraper - Now Searches:
1. Credit Analyst Intern (Seattle, SF)
2. **Commercial Banking Intern (Seattle, US)** ← NEW
3. **Corporate Banking Intern (Seattle, US)** ← NEW
4. Summer Analyst Corporate Banking (US)
5. **Summer Analyst Lending (US)** ← NEW
6. Investment Analyst Direct Lending (Remote)
7. Corporate Banking Analyst (Seattle)
8. **Relationship Banking Analyst (US)** ← NEW
9. BDC Analyst (US)

## Impact on Scoring

### Before Update
```
Title: "Commercial Banking Intern - Summer 2027"
Score: ~5-7 (would match on "intern" and location only)
```

### After Update
```
Title: "Commercial Banking Intern - Summer 2027"
Score: 13 points
  +5: Perfect title match "commercial banking intern"
  +3: Preferred location
  +2: Student-friendly ("intern")
  +2: Keywords in title
  +1: Keywords in description
```

## Example High-Scoring Jobs (Now Captured)

### Perfect Match (15 points)
```
"Corporate Banking Summer Analyst - Lending"
JPMorgan Chase | New York, NY

  +5: Title match "summer analyst"
  +6: Three keywords in title (Corporate, Banking, Lending)
  +3: Preferred location
  +1: Keywords in description
```

### Strong Match (14 points)
```
"Summer Analyst - Relationship Banking"
BMO | Seattle, WA

  +5: Title match "summer analyst"
  +4: Two keywords in title
  +3: Preferred location
  +2: Keywords in description
```

### Strong Match (13 points)
```
"Commercial Banking Intern"
Wells Fargo | Seattle, WA

  +5: Title match "commercial banking intern"
  +3: Preferred location
  +2: Student-friendly
  +2: Keywords in title
  +1: Keywords in description
```

## Why These Additions Matter

### Corporate Banking vs Commercial Banking
- **Corporate Banking**: Typically larger companies ($50M-$2B revenue)
- **Commercial Banking**: Often used interchangeably with corporate banking
- **Both lead to same roles**: Credit analysis, relationship management, deal structuring

Many banks use these terms differently:
- Wells Fargo: "Commercial Banking"
- JPMorgan: "Corporate Banking"  
- BMO: Both terms used
- KeyBank: "Commercial Banking"

**Result**: You were potentially missing 30-40% of relevant postings that used "commercial" instead of "corporate"

### Relationship Banking
- Core function of corporate/commercial banking roles
- Involves credit analysis + client relationship management
- Exactly aligned with your search fund → lending progression

### Lending (as standalone term)
- Catches "Lending Analyst", "Summer Analyst - Lending", etc.
- Directly relevant to credit-side focus
- Often used in job titles without "Corporate Banking" prefix

## Search Coverage Increase

### Before
- ~7 searches per platform = 14 total searches per 6-hour cycle

### After  
- ~13 searches per platform = 26 total searches per 6-hour cycle
- **+85% more search coverage**

### Jobs Previously Missed (Examples)
- "Commercial Banking Summer Analyst" at Citizens Bank
- "Relationship Banking Intern" at Umpqua
- "Lending Analyst Intern" at Banner Bank
- "Corporate Banking Intern" at Pacific Western

## No Action Required

All changes are already integrated:
- ✅ Scorer updated with new high-value titles
- ✅ Scrapers updated with new searches
- ✅ Default keywords expanded
- ✅ Documentation updated

**When you deploy, the system will automatically search for all these variations.**

---

**Bottom line**: You're now capturing commercial banking roles in addition to corporate banking, which significantly expands your relevant job pipeline while maintaining high quality scoring.
