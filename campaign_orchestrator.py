#!/usr/bin/env python3
"""
TTI 48-Hour Campaign Orchestrator
Runs tti_48hr_campaign.py every 30 minutes until April 4, 2026 9:40 AM PDT.
Commits to GitHub and sends status email after each cycle.
"""

import subprocess
import json
import time
import datetime
import os
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

# ─── Configuration ───────────────────────────────────────────────────────────
REPO_DIR = Path("/home/ubuntu/CEO-Mr-Reddix")
INTEL_DIR = REPO_DIR / "intelligence" / "48hr_campaign"
CAMPAIGN_SCRIPT = REPO_DIR / "tti_48hr_campaign.py"
RESULT_FILE = INTEL_DIR / "latest_cycle_result.json"
EMAIL_TO = "aaronreddix1987@gmail.com"
CYCLE_INTERVAL_SECONDS = 30 * 60  # 30 minutes

# Campaign end time: April 4, 2026 9:40 AM PDT
PDT = ZoneInfo("America/Los_Angeles")
CAMPAIGN_END = datetime.datetime(2026, 4, 4, 9, 40, 0, tzinfo=PDT)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def run(cmd, cwd=None, timeout=120):
    """Run a shell command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True,
        cwd=cwd or str(REPO_DIR), timeout=timeout
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def hours_elapsed():
    """Hours since campaign start (April 2, 2026 9:40 AM PDT)."""
    start = datetime.datetime(2026, 4, 2, 9, 40, 0, tzinfo=PDT)
    now = datetime.datetime.now(tz=PDT)
    delta = now - start
    return max(0, delta.total_seconds() / 3600)


def campaign_still_running():
    """Return True if we are still within the 48-hour window."""
    now = datetime.datetime.now(tz=PDT)
    return now < CAMPAIGN_END


def execute_campaign_cycle():
    """Run the campaign Python script and return the result dict."""
    print(f"\n[ORCHESTRATOR] Running campaign cycle at {datetime.datetime.now(tz=PDT).strftime('%Y-%m-%d %H:%M:%S PDT')}")
    rc, stdout, stderr = run(f"python3 {CAMPAIGN_SCRIPT}", cwd=str(REPO_DIR), timeout=120)
    print(stdout)
    if stderr:
        print(f"[STDERR] {stderr}")
    if rc != 0:
        print(f"[ERROR] Campaign script exited with code {rc}")
        return None
    # Read result JSON
    if RESULT_FILE.exists():
        with open(RESULT_FILE) as f:
            return json.load(f)
    return None


def git_commit_push(result):
    """Add, commit, pull-rebase, and push to GitHub."""
    revenue = result.get("confirmed_revenue_usd", 0)
    hot_leads = result.get("hot_leads", 0)
    cycle = result.get("cycle", "?")
    commit_msg = f"48HR CAMPAIGN CYCLE: ${revenue:,} revenue | {hot_leads} HOT leads"
    run("git add -A")
    rc, out, err = run(f'git commit -m "{commit_msg}"')
    print(f"[GIT COMMIT] {out or err}")
    rc2, out2, err2 = run("git pull --rebase origin main")
    print(f"[GIT PULL] {out2 or err2}")
    rc3, out3, err3 = run("git push origin main")
    print(f"[GIT PUSH] {out3 or err3}")
    return rc3 == 0


def send_status_email(result):
    """Send a status email via Gmail MCP."""
    hour_num = int(hours_elapsed())
    cycle = result.get("cycle", "?")
    sms_sent = result.get("sms_sent", 0)
    sms_delivered = result.get("sms_delivered", 0)
    responses = result.get("responses", 0)
    hot_leads = result.get("hot_leads", 0)
    demos_booked = result.get("demos_booked", 0)
    demos_confirmed = result.get("demos_confirmed", 0)
    deals_sourced = result.get("deals_sourced", 0)
    hot_deals = result.get("hot_deals", 0)
    owner_finance = result.get("owner_finance_deals", 0)
    confirmed_rev = result.get("confirmed_revenue_usd", 0)
    pipeline = result.get("pipeline_value_usd", 0)
    content_pieces = result.get("content_pieces", 0)

    subject = (
        f"TTI 48HR CAMPAIGN UPDATE — [Hour {hour_num}] | "
        f"${confirmed_rev:,} | {hot_leads} HOT Leads | IQ 200"
    )

    body = (
        f"TTI 48-HOUR MASTER BLACK MARKETING CAMPAIGN\n"
        f"CYCLE {cycle} — COMPLETED\n\n"
        f"CAMPAIGN METRICS — CYCLE {cycle}\n"
        f"{'='*45}\n\n"
        f"SMS BLAST (Phone Tower)\n"
        f"   SMS Sent:        {sms_sent:,}\n"
        f"   SMS Delivered:   {sms_delivered:,}\n"
        f"   Responses:       {responses}\n\n"
        f"LEADS & DEMOS\n"
        f"   HOT Leads:       {hot_leads}\n"
        f"   Demos Booked:    {demos_booked}\n"
        f"   Demos Confirmed: {demos_confirmed}\n\n"
        f"OWNER FINANCE DEALS\n"
        f"   Deals Sourced:   {deals_sourced}\n"
        f"   HOT Deals:       {hot_deals}\n"
        f"   Owner Finance:   {owner_finance}\n\n"
        f"REVENUE\n"
        f"   Confirmed:       ${confirmed_rev:,}\n"
        f"   Pipeline Value:  ${pipeline:,}\n\n"
        f"CONTENT\n"
        f"   Markets:         15\n"
        f"   Platforms:       7\n"
        f"   Content Pieces:  {content_pieces}\n\n"
        f"{'='*45}\n"
        f"GitHub: Committed and pushed to main\n"
        f"Campaign End: April 4, 2026 9:40 AM PDT\n"
        f"Hours Elapsed: {hours_elapsed():.1f} / 48\n"
        f"Next cycle fires in 30 minutes.\n"
        f"{'='*45}\n\n"
        f"IQ 200 SUPER HERMES AI AGENT 2026\n"
        f"TTI Investments | CEO Mr. Reddix"
    )

    # Build MCP JSON payload
    payload = json.dumps({
        "messages": [
            {
                "to": [EMAIL_TO],
                "subject": subject,
                "content": body
            }
        ]
    })

    # Escape for shell
    payload_escaped = payload.replace("'", "'\\''")
    cmd = f"manus-mcp-cli tool call gmail_send_messages --server gmail --input '{payload_escaped}'"
    rc, out, err = run(cmd, timeout=60)
    if rc == 0:
        print(f"[EMAIL] Sent: {subject}")
    else:
        print(f"[EMAIL ERROR] rc={rc} | {err}")
    return rc == 0


def main():
    print("=" * 60)
    print("  TTI 48-HR CAMPAIGN ORCHESTRATOR — IQ 200 SUPER HERMES")
    print(f"  Campaign ends: {CAMPAIGN_END.strftime('%Y-%m-%d %H:%M %Z')}")
    print("=" * 60)

    cycle_count = 0

    while campaign_still_running():
        cycle_count += 1
        cycle_start = time.time()
        print(f"\n[ORCHESTRATOR] === CYCLE {cycle_count} START ===")

        # 1. Execute campaign
        result = execute_campaign_cycle()
        if result is None:
            print("[ORCHESTRATOR] Campaign script failed. Retrying next interval.")
        else:
            # 2. Git commit and push
            git_commit_push(result)
            # 3. Send email
            send_status_email(result)

        # 4. Wait until next 30-minute mark
        elapsed = time.time() - cycle_start
        sleep_time = max(0, CYCLE_INTERVAL_SECONDS - elapsed)
        next_run = datetime.datetime.now(tz=PDT) + datetime.timedelta(seconds=sleep_time)
        print(f"\n[ORCHESTRATOR] Cycle complete. Next run at {next_run.strftime('%H:%M:%S PDT')}")
        print(f"[ORCHESTRATOR] Sleeping {sleep_time/60:.1f} minutes...")

        # Sleep in small chunks so we can check the end condition
        slept = 0
        while slept < sleep_time:
            if not campaign_still_running():
                break
            chunk = min(60, sleep_time - slept)
            time.sleep(chunk)
            slept += chunk

    print("\n" + "=" * 60)
    print("  TTI 48-HR CAMPAIGN COMPLETE — ALL CYCLES EXECUTED")
    print(f"  Ended at: {datetime.datetime.now(tz=PDT).strftime('%Y-%m-%d %H:%M %Z')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
