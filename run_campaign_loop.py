#!/usr/bin/env python3
"""
TTI 48-Hour Campaign Orchestrator
Runs campaign cycles every 30 minutes until April 4, 2026 9:40 AM PDT
IQ 200 | Super Hermes AI Agent 2026
"""

import subprocess
import json
import time
import datetime
import os
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
CAMPAIGN_DIR = Path("/home/ubuntu/CEO-Mr-Reddix")
INTELLIGENCE_DIR = CAMPAIGN_DIR / "intelligence" / "48hr_campaign"
LOGS_DIR = CAMPAIGN_DIR / "logs"
RECIPIENT_EMAIL = "aaronreddix1987@gmail.com"

# Campaign end time: April 4, 2026 9:40 AM PDT (UTC-7)
PDT = ZoneInfo("America/Los_Angeles")
CAMPAIGN_END = datetime.datetime(2026, 4, 4, 9, 40, 0, tzinfo=PDT)

CYCLE_INTERVAL_SECONDS = 30 * 60  # 30 minutes

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def log(msg: str):
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOGS_DIR / "orchestrator.log", "a") as f:
        f.write(line + "\n")


def hours_elapsed_since_start() -> float:
    start = datetime.datetime(2026, 4, 2, 9, 40, 0, tzinfo=PDT)
    now = datetime.datetime.now(tz=PDT)
    return (now - start).total_seconds() / 3600


def time_remaining_str() -> str:
    now = datetime.datetime.now(tz=PDT)
    remaining = CAMPAIGN_END - now
    if remaining.total_seconds() <= 0:
        return "CAMPAIGN COMPLETE"
    total_secs = int(remaining.total_seconds())
    hours = total_secs // 3600
    minutes = (total_secs % 3600) // 60
    return f"{hours}h {minutes}m remaining"


def run_campaign_script() -> dict:
    """Run the campaign script and return results."""
    log("Running tti_48hr_campaign.py...")
    result = subprocess.run(
        ["python3", "tti_48hr_campaign.py"],
        cwd=str(CAMPAIGN_DIR),
        capture_output=True,
        text=True,
        timeout=120
    )
    if result.returncode != 0:
        log(f"ERROR: Campaign script failed: {result.stderr[:500]}")
        raise RuntimeError(f"Campaign script error: {result.stderr[:200]}")
    log("Campaign script completed successfully")

    # Read latest result
    result_file = INTELLIGENCE_DIR / "latest_cycle_result.json"
    with open(result_file) as f:
        return json.load(f)


def git_commit_and_push(cycle_data: dict):
    """Stage all changes, commit, pull rebase, and push."""
    revenue = cycle_data["confirmed_revenue_usd"]
    hot_leads = cycle_data["hot_leads"]
    cycle_num = cycle_data["cycle"]
    commit_msg = f"48HR CAMPAIGN CYCLE {cycle_num}: ${revenue:,} revenue | {hot_leads} HOT leads"

    log(f"Git: staging all changes...")
    subprocess.run(["git", "add", "-A"], cwd=str(CAMPAIGN_DIR), check=True, capture_output=True)

    log(f"Git: committing with message: {commit_msg}")
    subprocess.run(
        ["git", "commit", "-m", commit_msg],
        cwd=str(CAMPAIGN_DIR), check=True, capture_output=True
    )

    log("Git: pulling with rebase...")
    pull_result = subprocess.run(
        ["git", "pull", "--rebase", "origin", "main"],
        cwd=str(CAMPAIGN_DIR), capture_output=True, text=True
    )
    log(f"Git pull result: {pull_result.stdout.strip()[:100]}")

    log("Git: pushing to origin main...")
    push_result = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=str(CAMPAIGN_DIR), capture_output=True, text=True
    )
    if push_result.returncode != 0:
        log(f"Git push warning: {push_result.stderr[:200]}")
    else:
        log("Git push successful")


def send_status_email(cycle_data: dict):
    """Send status email via Gmail MCP."""
    cycle = cycle_data["cycle"]
    revenue = cycle_data["confirmed_revenue_usd"]
    pipeline = cycle_data["pipeline_value_usd"]
    hot_leads = cycle_data["hot_leads"]
    demos_booked = cycle_data["demos_booked"]
    demos_confirmed = cycle_data["demos_confirmed"]
    sms_sent = cycle_data["sms_sent"]
    deals_sourced = cycle_data["deals_sourced"]
    hot_deals = cycle_data["hot_deals"]
    of_deals = cycle_data["owner_finance_deals"]
    elapsed = hours_elapsed_since_start()
    remaining = time_remaining_str()
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    subject = f"TTI 48HR CAMPAIGN UPDATE — [Hour {elapsed:.1f}] | ${revenue:,} | {hot_leads} HOT Leads | IQ 200"

    body = f"""TTI 48-HOUR MASTER BLACK MARKETING CAMPAIGN
IQ 200 | Super Hermes AI Agent 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CYCLE {cycle} RESULTS — {ts}
Campaign Time: Hour {elapsed:.1f} of 48 | {remaining}

📱 SMS BLAST (Phone Tower)
   • SMS Sent:          {sms_sent:,}
   • Delivered:         {cycle_data['sms_delivered']:,}
   • Responses:         {cycle_data['responses']}

🔥 LEADS & DEMOS
   • HOT Leads:         {hot_leads}
   • Warm Leads:        {cycle_data['warm_leads']}
   • Demos Booked:      {demos_booked}
   • Demos Confirmed:   {demos_confirmed}

🏠 OWNER FINANCE DEALS
   • Total Deals Sourced:    {deals_sourced}
   • HOT Deals:              {hot_deals}
   • Owner Finance Specific: {of_deals}

💰 REVENUE
   • Confirmed This Cycle:   ${revenue:,}
   • Pipeline Value:         ${pipeline:,}

📊 CONTENT ENGINE
   • Markets Covered:   {cycle_data['markets']} markets
   • Platforms Active:  {cycle_data['platforms']} platforms
   • Content Pieces:    {cycle_data['content_pieces']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT CYCLE: In 30 minutes
CAMPAIGN ENDS: April 4, 2026 9:40 AM PDT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TTI Investments | The Total Investment
Powered by IQ 200 Super Hermes AI Agent 2026
"""

    email_payload = json.dumps([{
        "to": RECIPIENT_EMAIL,
        "subject": subject,
        "body": body
    }])

    log(f"Sending status email for cycle {cycle}...")
    result = subprocess.run(
        ["manus-mcp-cli", "tool", "call", "gmail_send_messages",
         "--server", "gmail", "--input", email_payload],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        log(f"Email warning: {result.stderr[:200]}")
    else:
        log(f"Email sent successfully for cycle {cycle}")


def get_cumulative_stats() -> dict:
    """Read the revenue ledger and compute cumulative stats."""
    ledger = INTELLIGENCE_DIR / "revenue_ledger.jsonl"
    if not ledger.exists():
        return {"total_revenue": 0, "total_hot_leads": 0, "total_sms": 0, "cycles": 0}

    total_revenue = 0
    total_hot_leads = 0
    total_sms = 0
    cycles = 0
    with open(ledger) as f:
        for line in f:
            try:
                rec = json.loads(line.strip())
                total_revenue += rec.get("confirmed_revenue_usd", 0)
                total_hot_leads += rec.get("hot_leads", 0)
                total_sms += rec.get("sms_sent", 0)
                cycles += 1
            except Exception:
                pass
    return {
        "total_revenue": total_revenue,
        "total_hot_leads": total_hot_leads,
        "total_sms": total_sms,
        "cycles": cycles
    }


# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────

def main():
    log("=" * 60)
    log("TTI 48-HOUR MASTER BLACK MARKETING CAMPAIGN STARTING")
    log(f"Campaign ends: {CAMPAIGN_END.strftime('%Y-%m-%d %H:%M %Z')}")
    log(f"Cycle interval: {CYCLE_INTERVAL_SECONDS // 60} minutes")
    log("=" * 60)

    cycle_count = 0

    while True:
        now = datetime.datetime.now(tz=PDT)
        if now >= CAMPAIGN_END:
            log("CAMPAIGN END TIME REACHED. Shutting down.")
            # Send final summary email
            stats = get_cumulative_stats()
            final_payload = json.dumps([{
                "to": RECIPIENT_EMAIL,
                "subject": f"TTI 48HR CAMPAIGN COMPLETE | ${stats['total_revenue']:,} TOTAL REVENUE | {stats['total_hot_leads']} HOT LEADS | IQ 200",
                "body": f"""TTI 48-HOUR MASTER BLACK MARKETING CAMPAIGN — FINAL REPORT
IQ 200 | Super Hermes AI Agent 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAMPAIGN COMPLETE — {now.strftime('%Y-%m-%d %H:%M %Z')}

📊 FINAL CUMULATIVE STATS
   • Total Cycles Run:    {stats['cycles']}
   • Total SMS Sent:      {stats['total_sms']:,}
   • Total HOT Leads:     {stats['total_hot_leads']}
   • Total Revenue:       ${stats['total_revenue']:,}

The 48-hour campaign has concluded successfully.
All intelligence logs are committed to GitHub.

TTI Investments | IQ 200 Super Hermes AI Agent 2026
"""
            }])
            subprocess.run(
                ["manus-mcp-cli", "tool", "call", "gmail_send_messages",
                 "--server", "gmail", "--input", final_payload],
                capture_output=True, text=True, timeout=60
            )
            break

        cycle_count += 1
        log(f"\n{'─'*50}")
        log(f"STARTING CYCLE {cycle_count} | {time_remaining_str()}")
        log(f"{'─'*50}")

        try:
            # 1. Run campaign
            cycle_data = run_campaign_script()

            # 2. Git commit and push
            git_commit_and_push(cycle_data)

            # 3. Send email
            send_status_email(cycle_data)

            # 4. Log cumulative stats
            stats = get_cumulative_stats()
            log(f"CUMULATIVE: {stats['cycles']} cycles | ${stats['total_revenue']:,} revenue | {stats['total_hot_leads']} HOT leads")

        except Exception as e:
            log(f"ERROR in cycle {cycle_count}: {e}")

        # Wait for next cycle
        next_run = datetime.datetime.now(tz=PDT) + datetime.timedelta(seconds=CYCLE_INTERVAL_SECONDS)
        if next_run >= CAMPAIGN_END:
            log("Next cycle would exceed campaign end time. Finishing.")
            break

        log(f"Sleeping {CYCLE_INTERVAL_SECONDS // 60} minutes until next cycle at {next_run.strftime('%H:%M %Z')}...")
        time.sleep(CYCLE_INTERVAL_SECONDS)

    log("Campaign orchestrator exiting.")


if __name__ == "__main__":
    main()
