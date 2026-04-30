import csv, os

CMS_FILE = "data/cms/home_health_agencies.csv"
EXPORT_FILE = "data/cms/target_agencies.csv"

def score_agency(row):
    score = 0
    signals = []

    for k, v in row.items():
        key = str(k).lower()
        val = str(v).strip()

        try:
            num = float(val)
        except:
            continue

        if "star" in key and num <= 3:
            score += 30
            signals.append("Low CMS star rating")

        if "timely" in key and num < 90:
            score += 20
            signals.append("Timely care performance gap")

        if "quality" in key and num < 3:
            score += 20
            signals.append("Quality performance concern")

    return score, list(set(signals))

def build_target_list(limit=100):
    if not os.path.exists(CMS_FILE):
        return []

    targets = []

    with open(CMS_FILE, newline="", encoding="utf-8-sig", errors="ignore") as f:
        rows = csv.DictReader(f)

        for row in rows:
            score, signals = score_agency(row)

            if score > 0:
                row["_lead_score"] = score
                row["_signals"] = "; ".join(signals)
                targets.append(row)

    targets = sorted(targets, key=lambda x: int(x["_lead_score"]), reverse=True)[:limit]

    os.makedirs("data/cms", exist_ok=True)

    if targets:
        with open(EXPORT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=targets[0].keys())
            writer.writeheader()
            writer.writerows(targets)

    return targets


