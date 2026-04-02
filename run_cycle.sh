#!/bin/bash
# TTI Campaign Cycle Runner - runs one cycle, commits, and prepares email payload
set -e
cd /home/ubuntu/CEO-Mr-Reddix

# Run campaign
python3 tti_48hr_campaign.py

# Git operations
git add -A
REVENUE=$(python3 -c "import json; d=json.load(open('intelligence/48hr_campaign/latest_cycle_result.json')); print(f\"{d['confirmed_revenue_usd']:,}\")")
HOT=$(python3 -c "import json; d=json.load(open('intelligence/48hr_campaign/latest_cycle_result.json')); print(d['hot_leads'])")
git commit -m "48HR CAMPAIGN CYCLE: \$$REVENUE revenue | $HOT HOT leads" || echo "Nothing to commit"
git pull --rebase origin main
git push origin main

echo "CYCLE COMPLETE: Revenue=\$$REVENUE | HOT Leads=$HOT"
