import csv, os

TARGET_FILE = "data/cms_target_leads.csv"
EMAIL_FILE = "data/verified_emails.csv"

def load_verified_emails():
    if not os.path.exists(EMAIL_FILE):
        return {}

    with open(EMAIL_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    return {
        r.get("lead_id",""): r
        for r in rows
        if r.get("email") and str(r.get("verified","")).lower() == "true"
    }

def enrich_targets():
    if not os.path.exists(TARGET_FILE):
        return {"updated": 0, "error": "Run CMS targeting first."}

    verified = load_verified_emails()

    with open(TARGET_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    updated = 0

    for r in rows:
        lead_id = r.get("lead_id","")
        if lead_id in verified:
            r["email"] = verified[lead_id]["email"]
            r["email_source"] = verified[lead_id].get("source","manual")
            r["email_verified"] = "true"
            updated += 1
        else:
            r["email_verified"] = "false"

    fields = list(rows[0].keys()) if rows else []

    with open(TARGET_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    return {"updated": updated}

