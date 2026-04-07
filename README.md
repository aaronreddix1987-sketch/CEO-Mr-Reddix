# TTI 48-Hour Master Black Marketing Campaign

**IQ 200 | Super Hermes AI Agent 2026**

## Overview

This repository powers the TTI 48-Hour Master Black Marketing Campaign and Owner Finance Cash Hunt. It generates marketing content across target markets, logs revenue intelligence, and can run a timed campaign loop that commits cycle output and sends status updates.

## What Was Fixed

- Removed hardcoded `/home/ubuntu/...` path assumptions
- Replaced stale April 2026 hardcoded loop windows with environment-driven scheduling
- Removed `git push --force` from the main orchestrator
- Consolidated duplicate loop scripts so they call one maintained runner
- Kept Gmail status emails optional instead of crashing when the external CLI is unavailable

## Structure

```text
CEO-Mr-Reddix/
├── tti_48hr_campaign.py      # Single cycle execution
├── run_campaign_loop.py      # Maintained campaign orchestrator
├── auto_campaign_loop.py     # Thin wrapper -> run_campaign_loop.main()
├── auto_48hr_loop.py         # Thin wrapper -> run_campaign_loop.main()
├── campaign_orchestrator.py  # Thin wrapper -> run_campaign_loop.main()
├── intelligence/
│   └── 48hr_campaign/        # Cycle logs, deal data, revenue ledger
└── logs/
    └── orchestrator.log      # Loop execution log
```

## Configuration

Environment variables:

- `TTI_CAMPAIGN_START`: ISO timestamp for campaign start
- `TTI_CAMPAIGN_END`: ISO timestamp for campaign end
- `TTI_CAMPAIGN_DURATION_HOURS`: defaults to `48` if no explicit end is set
- `TTI_CYCLE_INTERVAL_SECONDS`: defaults to `1800`
- `TTI_RECIPIENT_EMAIL`: status email recipient

If no start or end values are provided, the maintained runner starts immediately and uses a 48-hour window.

## Usage

```bash
python3 tti_48hr_campaign.py
python3 run_campaign_loop.py
```

## Runtime Configuration

- Paths resolve relative to the repo root
- `TTI_CAMPAIGN_START` / `TTI_CAMPAIGN_END` support ISO timestamps
- `TTI_CAMPAIGN_DURATION_HOURS` defaults to `48`
- `TTI_CYCLE_INTERVAL_SECONDS` defaults to `1800`
- `TTI_RECIPIENT_EMAIL` controls status email delivery

## Revenue Tracking

All revenue is logged to `intelligence/48hr_campaign/revenue_ledger.jsonl` with cumulative tracking across all cycles.
