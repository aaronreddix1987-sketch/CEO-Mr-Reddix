# TTI 48-Hour Master Black Marketing Campaign

**IQ 200 | Super Hermes AI Agent 2026**

## Overview

This repository powers the TTI 48-Hour Master Black Marketing Campaign and Owner Finance Cash Hunt. It generates marketing content for 15 markets across 7 platforms, fires Phone Tower SMS blasts, sources owner finance deals, and logs all revenue intelligence.

## Campaign Parameters

- **Start:** April 2, 2026 9:40 AM PDT
- **End:** April 4, 2026 9:40 AM PDT
- **Cycle Interval:** Every 30 minutes
- **Markets:** 15 target markets across the US
- **Platforms:** 7 (Facebook, Instagram, TikTok, YouTube, LinkedIn, Twitter/X, SMS/PhoneTower)

## Structure

```
CEO-Mr-Reddix/
├── tti_48hr_campaign.py          # Single cycle execution
├── run_campaign_loop.py          # 48hr orchestrator loop
├── intelligence/
│   └── 48hr_campaign/            # All cycle logs, deal data, revenue ledger
└── logs/
    └── orchestrator.log          # Loop execution log
```

## Usage

```bash
# Run one cycle manually
cd /home/ubuntu/CEO-Mr-Reddix && python3 tti_48hr_campaign.py

# Run full 48-hour loop
python3 run_campaign_loop.py
```

## Revenue Tracking

All revenue is logged to `intelligence/48hr_campaign/revenue_ledger.jsonl` with cumulative tracking across all cycles.

---
*Powered by TTI Investments | The Total Investment*
