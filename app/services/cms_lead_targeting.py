import csv, os, re
from datetime import datetime

CMS_FILE = "data/cms/home_health_agencies.csv"
EXPORT_FILE = "data/cms_target_leads.csv"
QUEUE_FILE = "data/outreach_queue.csv"

def to_float(v):
    try:
        return float(str(v).replace("%","").strip())
    except:
        return None

def get_any(row, keywords):
    for k, v in row.items():
        key = str(k).lower()
        if any(word in key for word in keywords):
            return v
    return ""

def score_agency(row):
    score = 0
    reasons = []

    star = to_float(get_any(row, ["star", "rating"]))
    if star is not None and star <= 3:
        score += 30
        reasons.append("Low CMS star/rating signal")

    readmit = to_float(get_any(row, ["readmission", "hospitalization"]))
    if readmit is not None and readmit >= 15:
        score += 25
        reasons.append("Elevated readmission/hospitalization signal")

    timely = to_float(get_any(row, ["timely", "started care"]))
    if timely is not None and timely < 85:
        score += 20
        reasons.append("Timely care performance gap")

    quality = to_float(get_any(row, ["quality", "improvement"]))
    if quality is not None and quality < 80:
        score += 15
        reasons.append("Quality improvement gap")

    if score >= 70:
        tier = "High Probability"
    elif score >= 40:
        tier = "Moderate Probability"
    else:
        tier = "Low Probability"

    return score, tier, "; ".join(reasons)

def clean_slug(text):
    return re.sub(r"[^a-zA-Z0-9]+", "", str(text).lower())[:40]

def build_targets(limit=250, state_filter=""):
    if not os.path.exists(CMS_FILE):
        return {"created": 0, "error": f"Missing {CMS_FILE}"}

    os.makedirs("data", exist_ok=True)

    with open(CMS_FILE, newline="", encoding="utf-8-sig", errors="ignore") as f:
        rows = list(csv.DictReader(f))

    leads = []

    for row in rows:
        agency = get_any(row, ["provider name", "agency name", "name"]) or row.get("Provider Name") or "Unknown Agency"
        state = get_any(row, ["state"]) or row.get("State") or ""

        if state_filter and str(state).upper() != state_filter.upper():
            continue

        score, tier, reasons = score_agency(row)

        if score < 40:
            continue

        lead_id = clean_slug(f"{agency}-{state}")
        preview_url = f"http://127.0.0.1:8000/mini-audit?agency={agency.replace(' ','%20')}&state={state}&lead_id={lead_id}"

        leads.append({
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "lead_id": lead_id,
            "email": "",
            "agency": agency,
            "state": state,
            "score": score,
            "tier": tier,
            "reasons": reasons,
            "preview_url": preview_url,
            "status": "targeted"
        })

    leads = sorted(leads, key=lambda x: x["score"], reverse=True)[:limit]

    with open(EXPORT_FILE, "w", newline="", encoding="utf-8") as f:
        fields = ["created_at","lead_id","email","agency","state","score","tier","reasons","preview_url","status"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(leads)

    return {"created": len(leads), "file": EXPORT_FILE}

def add_targets_to_outreach_queue():
    if not os.path.exists(EXPORT_FILE):
        return {"added": 0, "error": "Run targeting first."}

    with open(EXPORT_FILE, newline="", encoding="utf-8") as f:
        targets = list(csv.DictReader(f))

    existing = []
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, newline="", encoding="utf-8") as f:
            existing = list(csv.DictReader(f))

    existing_ids = {r.get("lead_id") for r in existing}
    added = 0

    fields = ["created_at","lead_id","email","agency","state","preview_url","status","sent_at","error"]

    with open(QUEUE_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)

        if not existing:
            w.writeheader()

        for t in targets:
            if t.get("lead_id") in existing_ids:
                continue

            w.writerow({
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "lead_id": t.get("lead_id"),
                "email": t.get("email"),
                "agency": t.get("agency"),
                "state": t.get("state"),
                "preview_url": t.get("preview_url"),
                "status": "pending",
                "sent_at": "",
                "error": ""
            })
            added += 1

    return {"added": added}

