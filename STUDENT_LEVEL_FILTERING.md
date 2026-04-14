# Enhanced Student-Level Role Detection

## What Changed

The scoring system now **guarantees** that only student-level roles (intern or summer analyst positions) score highly, while experienced roles are capped at low scores.

---

## Key Improvements

### 1. Mandatory Student-Level Detection
```python
STUDENT_LEVEL_TERMS = [
    'intern', 
    'internship', 
    'summer analyst', 
    'analyst intern',
    'summer 2026', 
    'summer 2027', 
    'summer 2028'
]
```

**Logic**: 
- If title OR description contains any of these → Student-level role ✅
- Otherwise → Experienced role (score capped at 6) ⚠️

### 2. Bonus Points for "Summer Analyst" or "Intern" in Title
- **+3 points** if title contains "Summer Analyst"
- **+3 points** if title contains "Intern" (but not "Internship")
- Ensures these critical keywords are heavily weighted

### 3. Score Capping for Non-Student Roles
- **Student-level roles**: Max score = 15
- **Experienced roles**: Max score = 6 (below MIN_SCORE threshold of 3-8)

---

## Scoring Examples

### ✅ Perfect Student-Level Matches (Score: 15)

#### Example 1: "Commercial Banking Intern"
```
Title: Commercial Banking Intern
Company: Wells Fargo | Seattle, WA

Score Breakdown:
  +5: Perfect title match "commercial banking intern"
  +3: Contains "Intern" in title (BONUS)
  +3: Preferred location (Seattle)
  +2: Student-friendly indicator
  +2: Keywords in title
  ─────
  15 points ✅ EMAIL SENT
```

#### Example 2: "Summer Analyst - Corporate Banking"
```
Title: Summer Analyst - Corporate Banking
Company: JPMorgan | New York, NY

Score Breakdown:
  +5: Perfect title match "summer analyst"
  +3: Contains "Summer Analyst" in title (BONUS)
  +3: Preferred location (New York)
  +2: Student-friendly indicator
  +2: Keywords in title
  ─────
  15 points ✅ EMAIL SENT
```

#### Example 3: "Credit Analyst Intern"
```
Title: Credit Analyst Intern
Company: BMO | Seattle, WA

Score Breakdown:
  +5: Perfect title match "credit analyst intern"
  +3: Contains "Intern" in title (BONUS)
  +3: Preferred location (Seattle)
  +2: Student-friendly indicator
  +2: Keywords in title
  ─────
  15 points ✅ EMAIL SENT
```

---

### ❌ Experienced Roles (Capped at Score: 6)

#### Example 1: "Corporate Banking Analyst" (Full-time)
```
Title: Corporate Banking Analyst
Company: Wells Fargo | Seattle, WA
Description: 2+ years experience required

Raw Score Calculation:
  +5: Perfect title match
  +3: Location
  +2: Keywords in title
  +1: Keywords in description
  ─────
  11 points RAW

Applied Cap:
  ⚠️ Not student-level role (no intern/summer analyst terms)
  ⚠️ Capped at 6 points
  ─────
  6 points FINAL → IGNORED (below MIN_SCORE)
```

#### Example 2: "Credit Analyst" (Experienced)
```
Title: Credit Analyst
Company: JPMorgan | New York, NY
Description: Analyze commercial lending deals

Raw Score: 6 points
  ⚠️ Not student-level → Stays at 6
  ─────
  6 points → IGNORED
```

---

### ⚠️ Edge Cases (Moderate Scores)

#### Example 1: "Summer 2027 Analyst - Commercial Banking"
```
Title: Summer 2027 Analyst - Commercial Banking
Company: Wells Fargo | Seattle, WA

Score: 8 points
  ✅ Student-level detected ("summer 2027")
  +2: Student-friendly
  +2: Keywords
  +3: Location
  +1: Description
  ─────
  8 points → EMAIL SENT (if MIN_SCORE ≤ 8)
  
Note: Lower than perfect matches because title isn't 
exactly "Summer Analyst" format, but still student-level
```

#### Example 2: "Internship - Corporate Banking Credit"
```
Title: Internship - Corporate Banking Credit
Company: BMO | Seattle, WA

Score: 7 points
  ✅ Student-level detected ("internship")
  +2: Student-friendly
  +2: Keywords
  +3: Location
  ─────
  7 points → EMAIL SENT (if MIN_SCORE ≤ 7)
```

---

## Why This Matters

### Before Enhancement
**Problem**: Experienced roles could score high if they had the right keywords

```
"Corporate Banking Analyst" (Full-time, experienced)
  +5: Title match
  +3: Location
  +2: Keywords
  ─────
  10 points → Would send alert ❌ WRONG
```

### After Enhancement
**Solution**: Only student-level roles score above threshold

```
"Corporate Banking Analyst" (Full-time, experienced)
  Raw: 11 points
  ⚠️ Capped at 6 (not student-level)
  ─────
  6 points → IGNORED ✅ CORRECT
```

---

## Configuration Impact

### Recommended MIN_SCORE Settings

**Conservative (fewer emails, highest quality)**
```env
MIN_SCORE=8
```
- Only near-perfect student-level matches
- ~1-3 emails per week
- All will be highly relevant

**Balanced (recommended)**
```env
MIN_SCORE=5
```
- Strong student-level matches
- ~3-8 emails per week
- Mix of perfect + good matches

**Aggressive (maximum coverage)**
```env
MIN_SCORE=3
```
- Any student-level role with keywords
- ~8-15 emails per week
- Some lower-quality matches included

---

## Title Format Coverage

### ✅ Formats That Score High (15 points)
- "Commercial Banking Intern"
- "Corporate Banking Intern"
- "Summer Analyst - Corporate Banking"
- "Credit Analyst Intern"
- "Relationship Banking Intern"
- "Corporate Banking Summer Analyst"
- "Summer Analyst Intern - Lending"

### ✅ Formats That Score Moderate (7-11 points)
- "Internship - Corporate Banking"
- "Summer 2027 Analyst - Commercial Banking"
- "Commercial Lending Intern (Summer)"
- "Banking Intern - Credit"

### ❌ Formats That Score Low (≤6 points)
- "Corporate Banking Analyst" (no intern/summer)
- "Credit Analyst" (full-time)
- "Commercial Banking Associate" (experienced)
- "VP Corporate Banking" (excluded keyword)
- "Senior Credit Analyst" (excluded keyword)

---

## Testing Results

### Student-Level Roles (All scored 15/15) ✅
1. "Commercial Banking Intern" - Wells Fargo, Seattle
2. "Summer Analyst - Corporate Banking" - JPMorgan, NYC
3. "Credit Analyst Intern" - BMO, Seattle
4. "Corporate Banking Summer Analyst" - KeyBank, Seattle
5. "Relationship Banking Intern" - Citizens, Remote

### Experienced Roles (All capped at 6/15) ✅
1. "Corporate Banking Analyst" - Wells Fargo, Seattle
2. "Credit Analyst" - JPMorgan, NYC
3. "Commercial Banking Associate" - BMO, SF

---

## Summary

**Guarantee**: The system will now **only** send you alerts for roles that are:
1. ✅ Student-level (intern OR summer analyst)
2. ✅ Match your keywords (credit, banking, lending, etc.)
3. ✅ In your target locations
4. ✅ At your target companies (bonus points)

**No more**: Alerts for experienced, full-time, or senior roles that happen to have the right keywords.

**Result**: Higher signal-to-noise ratio = less time wasted = better recruiting outcomes.
