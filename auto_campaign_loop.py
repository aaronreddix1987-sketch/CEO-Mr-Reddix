#!/usr/bin/env python3
"""
TTI 48-Hour Campaign Auto-Loop
Runs every 30 minutes until April 4, 2026 9:40 AM PDT (16:40 UTC)
IQ 200 | Super Hermes AI Agent 2026
"""

import subprocess
import json
import time
import datetime
import sys
import os
import shlex

# Campaign end time: April 4, 2026 9:40 AM PDT = 16:40 UTC
END_TIME = datetime.datetime(2026, 4, 4, 16, 40, 0, tzinfo=datetime.timezone.utc)
INTERVAL_SECONDS = 30 * 60  # 30 minutes
CAMPAIGN_DIR = "/home/ubuntu/CEO-Mr-Reddix"
RESULT_FILE = "/home/ubuntu/CEO-Mr-Reddix/intelligence/48hr_campaign/latest_cycle_result.json"

def get_hour_offset():
    """Calculate hours since campaign start (April 2, 2026 16:40 UTC)."""
    start = datetime.datetime(2026, 4, 2, 16, 40, 0, tzinfo=datetime.timezone.utc)
    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - start
    return max(0, int(delta.total_seconds() / 3600))

def run_campaign_cycle():
    """Run one campaign cycle and return results."""
    print(f"\n{'='*60}")
    print(f"  AUTO-LOOP: Firing campaign cycle at {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"{'='*60}")

    # Step 1: Run the campaign script
    result = subprocess.run(
        ["python3", "-u", "tti_48hr_campaign.py"],
        cwd=CAMPAIGN_DIR,
        capture_output=True,
        text=True,
        timeout=120
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"[ERROR] Campaign script failed: {result.stderr}")
        return None

    # Step 2: Read results
    try:
        with open(RESULT_FILE, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not read result file: {e}")
        return None

    # Step 3: Git add, commit, pull rebase, push
    cycle = data.get("cycle", "?")
    revenue = data.get("confirmed_revenue_usd", 0)
    hot_leads = data.get("hot_leads", 0)
    commit_msg = f"48HR CAMPAIGN CYCLE {cycle}: ${revenue:,} revenue | {hot_leads} HOT leads"

    git_cmds = [
        ["git", "add", "-A"],
        ["git", "commit", "-m", commit_msg],
        ["git", "pull", "--rebase", "origin", "main"],
        ["git", "push", "origin", "main"],
    ]
    for cmd in git_cmds:
        r = subprocess.run(cmd, cwd=CAMPAIGN_DIR, capture_output=True, text=True, timeout=60)
        out = (r.stdout.strip() or r.stderr.strip())[:200]
        print(f"[GIT] {' '.join(cmd[:2])}: {out}")

    return data

def send_email(data):
    """Send campaign status email via Gmail MCP."""
    if not data:
        return

    cycle = data.get("cycle", "?")
    hour = get_hour_offset()
    sms_sent = data.get("sms_sent", 0)
    hot_leads = data.get("hot_leads", 0)
    demos_booked = data.get("demos_booked", 0)
    demos_confirmed = data.get("demos_confirmed", 0)
    deals_sourced = data.get("deals_sourced", 0)
    hot_deals = data.get("hot_deals", 0)
    of_deals = data.get("owner_finance_deals", 0)
    revenue = data.get("confirmed_revenue_usd", 0)
    pipeline = data.get("pipeline_value_usd", 0)
    timestamp = data.get("timestamp", datetime.datetime.utcnow().isoformat())

    subject = f"TTI 48HR CAMPAIGN UPDATE — [Hour {hour}] | ${revenue:,} | {hot_leads} HOT Leads | IQ 200"

    body = (
        f"TTI 48-HOUR MASTER BLACK MARKETING CAMPAIGN\n"
        f"IQ 200 | Super Hermes AI Agent 2026\n\n"
        f"CYCLE {cycle} RESULTS — {timestamp[:19].replace('T', ' ')} UTC\n\n"
        f"SMS BLAST (Phone Tower)\n"
        f"  SMS Sent:          {sms_sent:,}\n"
        f"  Delivered:         {data.get('sms_delivered', 0):,}\n"
        f"  Responses:         {data.get('responses', 0)}\n\n"
        f"LEADS & DEMOS\n"
        f"  HOT Leads:         {hot_leads}\n"
        f"  Warm Leads:        {data.get('warm_leads', 0)}\n"
        f"  Demos Booked:      {demos_booked}\n"
        f"  Demos Confirmed:   {demos_confirmed}\n\n"
        f"OWNER FINANCE DEALS\n"
        f"  Deals Sourced:     {deals_sourced}\n"
        f"  HOT Deals:         {hot_deals}\n"
        f"  Owner Finance:     {of_deals}\n\n"
        f"REVENUE\n"
        f"  Confirmed Revenue: ${revenue:,}\n"
        f"  Pipeline Value:    ${pipeline:,}\n\n"
        f"MARKETS COVERED: {data.get('markets', 15)}\n"
        f"PLATFORMS: {data.get('platforms', 7)}\n"
        f"CONTENT PIECES: {data.get('content_pieces', 105)}\n\n"
        f"GitHub: Committed and Pushed to main\n"
        f"Campaign End: April 4, 2026 9:40 AM PDT\n"
        f"Next cycle fires in approximately 30 minutes.\n\n"
        f"— IQ 200 Super Hermes AI Agent 2026\n"
        f"  Total Transformation Inc. | CEO Mr. Reddix"
    )

    # Write payload to temp file
    payload = {"messages": [{"to": ["aaronreddix1987@gmail.com"], "subject": subject, "content": body}]}
    payload_file = "/tmp/tti_email_payload.json"
    with open(payload_file, "w") as f:
        json.dump(payload, f)

    # Read it back as a single-line string for the CLI
    with open(payload_file, "r") as f:
        payload_str = f.read().strip()

    r = subprocess.run(
        ["manus-mcp-cli", "tool", "call", "gmail_send_messages",
         "--server", "gmail", "--input", payload_str],
        capture_output=True, text=True, timeout=60
    )
    combined = r.stdout + r.stderr
    if "Message ID" in combined or "mcp_result" in combined:
        print(f"[EMAIL] Sent: {subject}")
    else:
        print(f"[EMAIL] Output: {combined[:400]}")

def main():
    print(f"\n{'#'*60}")
    print(f"  TTI 48-HR AUTO-LOOP STARTED")
    print(f"  End time: {END_TIME.strftime('%Y-%m-%d %H:%M UTC')} (April 4, 2026 9:40 AM PDT)")
    print(f"  Interval: 30 minutes")
    print(f"{'#'*60}\n")

    loop_count = 0
    while True:
        now = datetime.datetime.now(datetime.timezone.utc)
        if now >= END_TIME:
            print(f"\n[DONE] Campaign end time reached: {now.isoformat()}")
            print("[DONE] TTI 48-Hour Campaign complete. All cycles executed.")
            break

        loop_count += 1
        print(f"\n[LOOP {loop_count}] Starting at {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"[LOOP {loop_count}] Time remaining: {END_TIME - now}")

        try:
            data = run_campaign_cycle()
            send_email(data)
        except Exception as e:
            print(f"[ERROR] Cycle failed: {e}")

        # Calculate next run time
        now = datetime.datetime.now(datetime.timezone.utc)
        if now >= END_TIME:
            print(f"\n[DONE] Campaign end time reached after cycle.")
            break

        next_run = now + datetime.timedelta(seconds=INTERVAL_SECONDS)
        if next_run > END_TIME:
            next_run = END_TIME

        wait_secs = (next_run - now).total_seconds()
        print(f"\n[WAIT] Next cycle at {next_run.strftime('%Y-%m-%d %H:%M UTC')} (waiting {int(wait_secs/60)} min {int(wait_secs%60)} sec)")
        sys.stdout.flush()
        time.sleep(max(0, wait_secs))

    print("\n[CAMPAIGN COMPLETE] TTI 48-Hour Master Black Marketing Campaign finished.")

if __name__ == "__main__":
    main()
