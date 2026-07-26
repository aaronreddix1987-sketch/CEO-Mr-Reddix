# TTI Income Engine — Autopilot Playbook
# CEO: Aaron Reddix | Total Transformation Inc.
# Email: aaronreddix1987@gmail.com | Phone: 747-301-8586
# Hub: https://tticommand-w4meojtc.manus.space
# Payment Rail: Chime Pay Anyone → 747-301-8586 (Aaron Reddix)
# Stripe: DISABLED until identity verification (charges_enabled=false)

## EVERY RUN CHECKLIST

### 1. GMAIL INBOX (in:inbox newer_than:1d)
- Search for real human messages
- Reply immediately to every real human message
- Close AI-agency prospects to $297/mo via Chime and (747) 301-8586
- If Groundfloor Finance replies, respond same-run with concrete next steps
- Search for ORDER emails (subject starts with "ORDER —") and Chime transfer alerts from alerts@account.chime.com
- FULFILLMENT: match payment amount to catalog in stripe_ids.md and email download links

### 2. DIGITAL PRODUCT SALES + FULFILLMENT
Catalog (hub: https://tticommand-w4meojtc.manus.space):
- Standard books: $27 / $37 / $47
- Standard bundle: $67
- EXPANDED editions: $47 / $67 / $97
- EXPANDED bundle: $147 (pitch first in PS lines)
- AI Agency: $297/mo

Payment instructions in all emails:
"Pay via Chime Pay Anyone to 747-301-8586 (Aaron Reddix), note the product name, then email proof to aaronreddix1987@gmail.com. No Chime? Reply and I'll send you a claim link to pay with any debit card."

### 3. PARTNERSHIP PIPELINE
Batch 11 (Mesmeric Media, Together Films, Central Recovery Press, Real Recovery Podcast, Faces & Voices of Recovery, Keep Coming Back Podcast):
- If any reply: respond same-run
- Follow up once Jul 31–Aug 3 if silent

Batch 12 (OKARR, RRA San Diego, FARR, Ohio Recovery Housing, MASH, VARR, GARR, Vanderburgh Sober Living, CCAR):
- If any reply: offer live demo call and webinar dates
- Follow up once Jul 30–Aug 2 if silent

### 4. 72-HOUR FOLLOW-UPS
- Check outreach_log.md for sends older than 72 hours with no reply
- Send follow-up (max 2 emails per address ever)

### 5. NEW PROSPECTS (up to 10 per run)
- NARR affiliates, sober living networks, production companies, recovery podcasts/publishers, treatment centers, property managers
- Verify every email on org's official site
- Obey 25 cold emails/day cap
- Check suppression_list.md before sending
- Log every send in outreach_log.md

### 6. LOGGING & SYNC
- Log every send in outreach_log.md
- Sync income_engine *.md to Drive TTI_Ops/ via rclone each run

### 7. NON-EMAIL PIPELINES
AT&T disputes:
- Order 23-272158255486454
- Order 23-771917521581375
- Dispute 23-272639298329650

Human-I-T donation: follow up on device donation status

Grant tickets:
- Cal Wellness REQ-5658
- FHA application
- Grants.gov CAS ticket

### 8. STRIPE RETRY (once per run)
- Call stripe MCP GetAccountsAccount (acct_1TxDpbDLrVG8kvWD)
- If charges_enabled becomes true: restore Stripe buy links on hub (siteData.ts PRODUCTS[].link)
- Announce card checkout is back

REMINDER: Stripe identity verification (DOB + SSN last 4 + bank + ToS) at dashboard.stripe.com takes Aaron ~2 minutes.
Remaining items: DOB (day/month/year), SSN last 4, external bank account (Stride routing 103100195, acct 2481533374660), ToS acceptance.

### 9. OPS REPORT EMAIL
Send to aaronreddix1987@gmail.com at end of every run:
- Replies handled
- Sends executed
- Orders fulfilled via Chime
- Pipeline status
- Single highest-value action for Aaron

## PRODUCT DOWNLOAD LINKS
See /home/ubuntu/ops/products/stripe_ids.md

## OUTREACH LOG
See /home/ubuntu/ops/income_engine/outreach_log.md

## SUPPRESSION LIST
See /home/ubuntu/ops/income_engine/suppression_list.md
