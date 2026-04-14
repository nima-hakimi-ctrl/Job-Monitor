#!/bin/bash

echo "=========================================================================="
echo "JOB MONITOR - AUTOMATED SETUP SCRIPT"
echo "=========================================================================="
echo ""
echo "This script will help you deploy to GitHub with minimal manual work."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# Check if gh CLI is installed
if command -v gh &> /dev/null; then
    USE_GH_CLI=true
    print_success "GitHub CLI detected - will use it for easier setup"
else
    USE_GH_CLI=false
    print_warning "GitHub CLI not found - will use manual method"
    echo "  Install with: brew install gh (Mac) or see https://cli.github.com"
fi

echo ""
echo "=========================================================================="
echo "STEP 1: COLLECT INFORMATION"
echo "=========================================================================="
echo ""

# GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

# Repository name
read -p "Enter repository name [job-monitor]: " REPO_NAME
REPO_NAME=${REPO_NAME:-job-monitor}

# Gmail
read -p "Enter your Gmail address: " EMAIL_FROM
EMAIL_TO=$EMAIL_FROM

# Gmail App Password
echo ""
echo "Gmail App Password:"
echo "  1. Go to: https://myaccount.google.com/apppasswords"
echo "  2. Enable 2FA if not already enabled"
echo "  3. Create app password named 'Job Monitor'"
echo "  4. Copy the 16-character password"
echo ""
read -sp "Paste Gmail App Password (won't show on screen): " EMAIL_PASSWORD
echo ""

# Keywords (with defaults)
echo ""
echo "Keywords (press Enter to use defaults):"
DEFAULT_KEYWORDS="Credit Analyst,Summer Analyst,Corporate Banking,Commercial Banking,Investment Analyst,Underwriting,Direct Lending,BDC,Lending,Relationship Banking"
read -p "[$DEFAULT_KEYWORDS]: " KEYWORDS
KEYWORDS=${KEYWORDS:-$DEFAULT_KEYWORDS}

# Locations
echo ""
echo "Target locations (press Enter to use defaults):"
DEFAULT_LOCATIONS="Seattle,Bellevue,San Francisco,Phoenix,New York,Remote"
read -p "[$DEFAULT_LOCATIONS]: " LOCATIONS
LOCATIONS=${LOCATIONS:-$DEFAULT_LOCATIONS}

# Companies
echo ""
echo "Target companies (press Enter to use defaults):"
DEFAULT_COMPANIES="Wells Fargo,JPMorgan Chase,BMO,KeyBank,Bank of America,Citizens Bank"
read -p "[$DEFAULT_COMPANIES]: " COMPANIES
COMPANIES=${COMPANIES:-$DEFAULT_COMPANIES}

# Exclude keywords
EXCLUDE_KEYWORDS="Senior,Manager,Director,VP,Vice President"

# Min score
MIN_SCORE="3"

echo ""
print_success "Information collected!"

echo ""
echo "=========================================================================="
echo "STEP 2: GIT INITIALIZATION"
echo "=========================================================================="
echo ""

# Initialize git if not already
if [ ! -d .git ]; then
    git init
    print_success "Git initialized"
else
    print_success "Git already initialized"
fi

# Add all files
git add .
print_success "Files staged"

# Commit
git commit -m "Initial job monitor setup" 2>/dev/null || print_warning "Files already committed"

echo ""
echo "=========================================================================="
echo "STEP 3: GITHUB REPOSITORY CREATION"
echo "=========================================================================="
echo ""

if [ "$USE_GH_CLI" = true ]; then
    echo "Using GitHub CLI to create repository..."
    
    # Check if logged in
    if ! gh auth status &> /dev/null; then
        echo "You need to login to GitHub CLI:"
        gh auth login
    fi
    
    # Create repo
    gh repo create "$GITHUB_USERNAME/$REPO_NAME" --public --source=. --remote=origin --push
    
    if [ $? -eq 0 ]; then
        print_success "Repository created and code pushed!"
    else
        print_error "Failed to create repository via GitHub CLI"
        exit 1
    fi
    
else
    echo "Manual GitHub setup required:"
    echo ""
    echo "1. Go to: https://github.com/new"
    echo "2. Repository name: $REPO_NAME"
    echo "3. Keep it PUBLIC"
    echo "4. DON'T initialize with README"
    echo "5. Click 'Create repository'"
    echo ""
    read -p "Press Enter once you've created the repository..."
    
    # Add remote
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git" 2>/dev/null || \
    git remote set-url origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    
    echo ""
    echo "Pushing to GitHub..."
    echo "You'll need to authenticate with:"
    echo "  Username: $GITHUB_USERNAME"
    echo "  Password: Your GitHub Personal Access Token (NOT your password)"
    echo ""
    echo "If you don't have a token:"
    echo "  1. Go to: https://github.com/settings/tokens"
    echo "  2. Generate new token (classic)"
    echo "  3. Select 'repo' scope only"
    echo "  4. Copy the token (starts with ghp_)"
    echo ""
    
    git branch -M main
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        print_success "Code pushed to GitHub!"
    else
        print_error "Failed to push. Check your credentials."
        exit 1
    fi
fi

echo ""
echo "=========================================================================="
echo "STEP 4: CONFIGURE GITHUB SECRETS"
echo "=========================================================================="
echo ""

if [ "$USE_GH_CLI" = true ]; then
    echo "Setting GitHub secrets via CLI..."
    
    gh secret set EMAIL_FROM --body "$EMAIL_FROM" --repo "$GITHUB_USERNAME/$REPO_NAME"
    gh secret set EMAIL_PASSWORD --body "$EMAIL_PASSWORD" --repo "$GITHUB_USERNAME/$REPO_NAME"
    gh secret set EMAIL_TO --body "$EMAIL_TO" --repo "$GITHUB_USERNAME/$REPO_NAME"
    gh secret set KEYWORDS --body "$KEYWORDS" --repo "$GITHUB_USERNAME/$REPO_NAME"
    gh secret set LOCATIONS --body "$LOCATIONS" --repo "$GITHUB_USERNAME/$REPO_NAME"
    gh secret set EXCLUDE_KEYWORDS --body "$EXCLUDE_KEYWORDS" --repo "$GITHUB_USERNAME/$REPO_NAME"
    gh secret set MIN_SCORE --body "$MIN_SCORE" --repo "$GITHUB_USERNAME/$REPO_NAME"
    gh secret set COMPANIES --body "$COMPANIES" --repo "$GITHUB_USERNAME/$REPO_NAME"
    
    print_success "All 8 secrets configured!"
    
else
    echo "GitHub secrets must be added manually."
    echo ""
    echo "Go to: https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/secrets/actions"
    echo ""
    echo "Add these 8 secrets (click 'New repository secret' for each):"
    echo ""
    echo "1. EMAIL_FROM"
    echo "   Value: $EMAIL_FROM"
    echo ""
    echo "2. EMAIL_PASSWORD"
    echo "   Value: [your app password - shown above]"
    echo ""
    echo "3. EMAIL_TO"
    echo "   Value: $EMAIL_TO"
    echo ""
    echo "4. KEYWORDS"
    echo "   Value: $KEYWORDS"
    echo ""
    echo "5. LOCATIONS"
    echo "   Value: $LOCATIONS"
    echo ""
    echo "6. EXCLUDE_KEYWORDS"
    echo "   Value: $EXCLUDE_KEYWORDS"
    echo ""
    echo "7. MIN_SCORE"
    echo "   Value: $MIN_SCORE"
    echo ""
    echo "8. COMPANIES"
    echo "   Value: $COMPANIES"
    echo ""
    read -p "Press Enter once you've added all 8 secrets..."
fi

echo ""
echo "=========================================================================="
echo "STEP 5: ENABLE GITHUB ACTIONS"
echo "=========================================================================="
echo ""

echo "Enable GitHub Actions:"
echo "1. Go to: https://github.com/$GITHUB_USERNAME/$REPO_NAME/actions"
echo "2. Click 'I understand my workflows, go ahead and enable them'"
echo "3. Click on 'Job Monitor' workflow"
echo "4. Click 'Run workflow' → 'Run workflow'"
echo ""
read -p "Press Enter once you've triggered the first run..."

echo ""
echo "=========================================================================="
print_success "SETUP COMPLETE!"
echo "=========================================================================="
echo ""
echo "Your job monitor is now deployed!"
echo ""
echo "What happens next:"
echo "  ✅ System runs every 6 hours automatically"
echo "  ✅ Searches Indeed + LinkedIn for matching jobs"
echo "  ✅ Emails you when high-quality matches are found"
echo "  ✅ Tracks jobs to avoid duplicate alerts"
echo ""
echo "Check your email in the next 6 hours for job alerts!"
echo ""
echo "Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "Actions: https://github.com/$GITHUB_USERNAME/$REPO_NAME/actions"
echo ""
print_success "Happy job hunting! 🚀"
echo ""
