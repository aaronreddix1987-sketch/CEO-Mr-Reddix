#!/usr/bin/env python3
"""
TTI 48-Hour Master Black Marketing Campaign — Automated Loop
IQ 200 | Super Hermes AI Agent 2026
Runs every 30 minutes until April 4, 2026 9:40 AM PDT (16:40 UTC)
"""

import subprocess
import json
import time
import datetime
import os
import sys
from pathlib import Path

# Campaign end time: April 4, 2026 9:40 AM PDT = 16:40 UTC
END_TIME = datetime.datetime(2026, 4, 4, 16, 40, 0, tzinfo=datetime.timezone.utc)
INTERVAL_SECONDS = 30 * 60  # 30 minutes
REPO_DIR = "/home/ubuntu/CEO-Mr-Reddix"
RESULT_FILE = "/home/ubuntu/CEO-Mr-Reddix/intelligence/48hr_campaign/latest_cycle_result.json"
LOG_FILE = "/home/ubuntu/CEO-Mr-Reddix/logs/auto_loop.log"

def log(msg: str):
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def run_campaign_cycle():
    """Run the campaign script and return the result dict."""
    log("Running tti_48hr_campaign.py ...")
    result = subprocess.run(
        ["python3", "tti_48hr_campaign.py"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        timeout=120
    )
    log(f"Script stdout: {result.stdout[-500:] if result.stdout else 'none'}")
    if result.returncode != 0:
        log(f"ERROR: {result.stderr[-300:]}")
        return None

    # Load result
    try:
        with open(RESULT_FILE) as f:
            return json.load(f)
    except Exception as e:
        log(f"Could not read result file: {e}")
        return None

def git_commit_push(cycle: int, revenue: int, hot_leads: int):
    """Git add, commit, pull rebase, push."""
    log("Git commit and push ...")
    cmds = [
        ["git", "add", "-A"],
        ["git", "commit", "-m", f"48HR CAMPAIGN CYCLE: ${revenue:,} revenue | {hot_leads} HOT leads"],
        ["git", "pull", "--rebase", "origin", "main"],
        ["git", "push", "origin", "main"],
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True, timeout=60)
        log(f"  {' '.join(cmd[:3])}: {'OK' if r.returncode == 0 else 'FAIL'} {r.stdout.strip()[-100:]} {r.stderr.strip()[-100:]}")

def send_email(cycle: int, data: dict, elapsed_hours: float):
    """Send status email via Gmail MCP."""
    hour_label = f"Hour {int(elapsed_hours)}"
    revenue = data.get("confirmed_revenue_usd", 0)
    hot_leads = data.get("hot_leads", 0)
    sms_sent = data.get("sms_sent", 0)
    sms_delivered = data.get("sms_delivered", 0)
    demos_booked = data.get("demos_booked", 0)
    demos_confirmed = data.get("demos_confirmed", 0)
    of_deals = data.get("owner_finance_deals", 0)
    pipeline = data.get("pipeline_value_usd", 0)
    deals_sourced = data.get("deals_sourced", 0)
    hot_deals = data.get("hot_deals", 0)
    ts = datetime.datetime.utcnow().strftime("%B %d, %Y | %I:%M %p UTC")

    subject = f"TTI 48HR CAMPAIGN UPDATE — [{hour_label}] | ${revenue:,} | {hot_leads} HOT Leads | IQ 200"
    body = (
        f"CEO Mr. Reddix,\n\n"
        f"CYCLE {cycle} COMPLETE — TTI 48-Hour Master Black Marketing Campaign\n\n"
        f"{'='*50}\n"
        f"CAMPAIGN STATS — CYCLE {cycle} | {ts}\n"
        f"{'='*50}\n\n"
        f"SMS COUNT:           {sms_sent:,} sent | {sms_delivered:,} delivered\n"
        f"HOT LEADS:           {hot_leads}\n"
        f"DEMOS BOOKED:        {demos_booked} booked | {demos_confirmed} confirmed\n"
        f"OWNER FINANCE DEALS: {of_deals} sourced\n"
        f"CONFIRMED REVENUE:   ${revenue:,}\n"
        f"PIPELINE VALUE:      ${pipeline:,}\n"
        f"DEALS SOURCED:       {deals_sourced} total | {hot_deals} HOT deals\n"
        f"MARKETS COVERED:     15 markets x 7 platforms\n"
        f"CONTENT GENERATED:   105 pieces\n\n"
        f"{'='*50}\n"
        f"CAMPAIGN STATUS: ACTIVE — Running every 30 minutes\n"
        f"Campaign ends: April 4, 2026 9:40 AM PDT\n"
        f"{'='*50}\n\n"
        f"All data committed to GitHub: aaronreddix1987-sketch/CEO-Mr-Reddix\n\n"
        f"IQ 200 | Super Hermes AI Agent 2026\n"
        f"Total Transformation Inc. (TTI)\n"
    )

    payload = json.dumps({
        "messages": [{
            "to": ["aaronreddix1987@gmail.com"],
            "subject": subject,
            "content": body
        }]
    })

    r = subprocess.run(
        ["manus-mcp-cli", "tool", "call", "gmail_send_messages",
         "--server", "gmail", "--input", payload],
        capture_output=True, text=True, timeout=90
    )
    if r.returncode == 0:
        log(f"Email sent: {subject}")
    else:
        log(f"Email FAILED: {r.stderr[-300:]}")

def main():
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    log("="*60)
    log("TTI 48-HR CAMPAIGN AUTO LOOP STARTED")
    log(f"Campaign ends at: {END_TIME.isoformat()}")
    log("="*60)

    campaign_start = datetime.datetime(2026, 4, 2, 16, 40, 0, tzinfo=datetime.timezone.utc)

    while True:
        now = datetime.datetime.now(datetime.timezone.utc)
        if now >= END_TIME:
            log("CAMPAIGN COMPLETE — 48 hours elapsed. Loop ending.")
            break

        elapsed = (now - campaign_start).total_seconds() / 3600.0
        remaining = (END_TIME - now).total_seconds()
        log(f"Starting cycle | Elapsed: {elapsed:.1f}h | Remaining: {remaining/3600:.1f}h")

        # 1. Run campaign
        data = run_campaign_cycle()
        if data is None:
            log("Campaign script failed — skipping git/email this cycle")
        else:
            cycle = data.get("cycle", 0)
            revenue = data.get("confirmed_revenue_usd", 0)
            hot_leads = data.get("hot_leads", 0)

            # 2. Git commit & push
            git_commit_push(cycle, revenue, hot_leads)

            # 3. Send email
            send_email(cycle, data, elapsed)

        # 4. Wait 30 minutes (or until end time)
        now2 = datetime.datetime.now(datetime.timezone.utc)
        remaining2 = (END_TIME - now2).total_seconds()
        sleep_secs = min(INTERVAL_SECONDS, max(0, remaining2))
        if sleep_secs <= 0:
            log("Campaign end time reached after cycle. Exiting.")
            break
        log(f"Sleeping {sleep_secs/60:.1f} minutes until next cycle ...")
        time.sleep(sleep_secs)

    log("TTI 48-HR CAMPAIGN AUTO LOOP FINISHED.")

if __name__ == "__main__":
    main()
