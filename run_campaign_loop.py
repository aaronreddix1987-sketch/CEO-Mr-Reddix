#!/usr/bin/env python3
"""Maintained TTI campaign orchestrator."""
from __future__ import annotations
import datetime, json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path
from zoneinfo import ZoneInfo
BASE_DIR = Path(__file__).resolve().parent
INTELLIGENCE_DIR = BASE_DIR / "intelligence" / "48hr_campaign"
LOGS_DIR = BASE_DIR / "logs"
CAMPAIGN_SCRIPT = BASE_DIR / "tti_48hr_campaign.py"
RESULT_FILE = INTELLIGENCE_DIR / "latest_cycle_result.json"
PDT = ZoneInfo("America/Los_Angeles")
RECIPIENT_EMAIL = os.getenv("TTI_RECIPIENT_EMAIL", "aaronreddix1987@gmail.com")
CYCLE_INTERVAL_SECONDS = int(os.getenv("TTI_CYCLE_INTERVAL_SECONDS", "1800"))
CAMPAIGN_DURATION_HOURS = int(os.getenv("TTI_CAMPAIGN_DURATION_HOURS", "48"))
def parse_dt(name):
    raw = os.getenv(name)
    if not raw:
        return None
    dt = datetime.datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=PDT)
    return dt.astimezone(PDT)
def resolve_window():
    now = datetime.datetime.now(tz=PDT)
    start = parse_dt("TTI_CAMPAIGN_START")
    end = parse_dt("TTI_CAMPAIGN_END")
    if start and end:
        return start, end
    if start and not end:
        return start, start + datetime.timedelta(hours=CAMPAIGN_DURATION_HOURS)
    if end and not start:
        return end - datetime.timedelta(hours=CAMPAIGN_DURATION_HOURS), end
    return now, now + datetime.timedelta(hours=CAMPAIGN_DURATION_HOURS)
CAMPAIGN_START, CAMPAIGN_END = resolve_window()
def log(msg):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    line = f"[{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}] {msg}"
    print(line, flush=True)
    with open(LOGS_DIR / "orchestrator.log", "a") as f:
        f.write(line + "\n")
def hours_elapsed_since_start():
    return max(0.0, (datetime.datetime.now(tz=PDT) - CAMPAIGN_START).total_seconds() / 3600)
def campaign_active():
    return datetime.datetime.now(tz=PDT) < CAMPAIGN_END
def run_campaign_script():
    if not CAMPAIGN_SCRIPT.exists():
        raise FileNotFoundError(f"Missing campaign script: {CAMPAIGN_SCRIPT}")
    log(f"Running {CAMPAIGN_SCRIPT.name} ...")
    result = subprocess.run([sys.executable, str(CAMPAIGN_SCRIPT)], cwd=str(BASE_DIR), capture_output=True, text=True, timeout=180)
    if result.stdout:
        print(result.stdout[-1200:], flush=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "campaign script failed")
    if not RESULT_FILE.exists():
        raise FileNotFoundError(f"Missing result file: {RESULT_FILE}")
    with open(RESULT_FILE) as f:
        return json.load(f)
def run_git(*args, check=False):
    result = subprocess.run(["git", *args], cwd=str(BASE_DIR), capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed")
    return result
def git_commit_and_push(cycle_data):
    revenue = cycle_data.get("confirmed_revenue_usd", 0)
    hot_leads = cycle_data.get("hot_leads", 0)
    cycle_num = cycle_data.get("cycle", "?")
    commit_msg = f"48HR CAMPAIGN CYCLE {cycle_num}: ${revenue:,} revenue | {hot_leads} HOT leads"
    run_git("add", "-A", check=True)
    status = run_git("status", "--porcelain")
    if not status.stdout.strip():
        log("Git: nothing new to commit")
        return
    run_git("commit", "-m", commit_msg, check=True)
    pull = run_git("pull", "--rebase", "origin", "main")
    if pull.returncode != 0:
        log(f"Git pull warning: {(pull.stderr or pull.stdout).strip()[:300]}")
    push = run_git("push", "origin", "main")
    if push.returncode != 0:
        log(f"Git push warning: {(push.stderr or push.stdout).strip()[:300]}")
    else:
        log("Git push successful")
def send_status_email(cycle_data):
    cli = shutil.which("manus-mcp-cli")
    if not cli:
        log("Email skipped: manus-mcp-cli not installed")
        return
    cycle = cycle_data.get("cycle", "?")
    revenue = cycle_data.get("confirmed_revenue_usd", 0)
    pipeline = cycle_data.get("pipeline_value_usd", 0)
    hot_leads = cycle_data.get("hot_leads", 0)
    demos_booked = cycle_data.get("demos_booked", 0)
    demos_confirmed = cycle_data.get("demos_confirmed", 0)
    sms_sent = cycle_data.get("sms_sent", 0)
    deals_sourced = cycle_data.get("deals_sourced", 0)
    hot_deals = cycle_data.get("hot_deals", 0)
    owner_finance = cycle_data.get("owner_finance_deals", 0)
    elapsed = hours_elapsed_since_start()
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    subject = f"TTI CAMPAIGN UPDATE | Hour {elapsed:.1f} | ${revenue:,} | {hot_leads} HOT Leads"
    body = (f"TTI CAMPAIGN UPDATE\n\nCycle: {cycle}\nTimestamp: {ts}\nHours elapsed: {elapsed:.1f}\nCampaign end: {CAMPAIGN_END.strftime('%Y-%m-%d %H:%M %Z')}\n\nSMS sent: {sms_sent:,}\nHOT leads: {hot_leads}\nDemos booked: {demos_booked}\nDemos confirmed: {demos_confirmed}\nDeals sourced: {deals_sourced}\nHOT deals: {hot_deals}\nOwner finance deals: {owner_finance}\nConfirmed revenue: ${revenue:,}\nPipeline value: ${pipeline:,}\n")
    payload = {"messages": [{"to": [RECIPIENT_EMAIL], "subject": subject, "content": body}]}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        tmp_path = f.name
    try:
        result = subprocess.run([cli, "tool", "call", "gmail_send_messages", "--server", "gmail", "--input", Path(tmp_path).read_text()], capture_output=True, text=True, timeout=90)
        if result.returncode != 0:
            log(f"Email warning: {(result.stderr or result.stdout).strip()[:300]}")
        else:
            log(f"Email sent for cycle {cycle}")
    finally:
        Path(tmp_path).unlink(missing_ok=True)
def send_final_summary():
    ledger = INTELLIGENCE_DIR / "revenue_ledger.jsonl"
    total_revenue = total_hot_leads = total_sms = cycles = 0
    if ledger.exists():
        with open(ledger) as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                cycles += 1
                total_revenue += rec.get("confirmed_revenue_usd", 0)
                total_hot_leads += rec.get("hot_leads", 0)
                total_sms += rec.get("sms_sent", 0)
    log(f"Campaign complete | cycles={cycles} | sms={total_sms:,} | hot_leads={total_hot_leads} | revenue=${total_revenue:,}")
def main():
    log("=" * 60)
    log("TTI CAMPAIGN ORCHESTRATOR STARTING")
    log(f"Base dir: {BASE_DIR}")
    log(f"Campaign window: {CAMPAIGN_START.strftime('%Y-%m-%d %H:%M %Z')} -> {CAMPAIGN_END.strftime('%Y-%m-%d %H:%M %Z')}")
    log(f"Cycle interval: {CYCLE_INTERVAL_SECONDS} seconds")
    log("=" * 60)
    if datetime.datetime.now(tz=PDT) >= CAMPAIGN_END:
        log("Campaign end is in the past. Exiting without running.")
        return
    while campaign_active():
        cycle_start = time.time()
        try:
            cycle_data = run_campaign_script()
            git_commit_and_push(cycle_data)
            send_status_email(cycle_data)
        except Exception as exc:
            log(f"Cycle error: {exc}")
        if not campaign_active():
            break
        elapsed = time.time() - cycle_start
        sleep_for = max(0, CYCLE_INTERVAL_SECONDS - elapsed)
        log(f"Sleeping {sleep_for/60:.1f} minutes until next cycle")
        time.sleep(sleep_for)
    send_final_summary()
    log("TTI CAMPAIGN ORCHESTRATOR FINISHED")
if __name__ == "__main__":
    main()
