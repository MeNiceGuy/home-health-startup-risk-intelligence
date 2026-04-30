import csv
import os
import urllib.request

DATASETS = {
    "home_health_agencies": {
        "id": "6jpm-sxkc",
        "path": "data/cms/home_health_agencies.csv"
    },
    "home_health_national": {
        "id": "97z8-de96",
        "path": "data/cms/home_health_national.csv"
    }
}

def download_cms_files():
    os.makedirs("data/cms", exist_ok=True)
    results = []

    for name, item in DATASETS.items():
        url = f"https://data.cms.gov/provider-data/api/1/datastore/query/{item['id']}/0/download?format=csv"

        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "text/csv,*/*"
                }
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                data = response.read()

            with open(item["path"], "wb") as f:
                f.write(data)

            results.append({
                "dataset": name,
                "status": "downloaded",
                "path": item["path"],
                "bytes": len(data)
            })

        except Exception as e:
            results.append({
                "dataset": name,
                "status": "failed",
                "error": str(e)
            })

    return results

def load_csv(path, limit=1000):
    if not os.path.exists(path):
        return []

    with open(path, newline="", encoding="utf-8-sig", errors="ignore") as f:
        reader = csv.DictReader(f)
        rows = []

        for i, row in enumerate(reader):
            if i >= limit:
                break
            rows.append(row)

        return rows

def find_agency_by_name_state(agency_name="", state=""):
    rows = load_csv(DATASETS["home_health_agencies"]["path"], limit=100000)

    agency_name = (agency_name or "").lower().strip()
    state = (state or "").upper().strip()

    if not agency_name:
        return []

    search_terms = [t for t in agency_name.replace("-", " ").replace(",", " ").split() if len(t) >= 3]

    scored = []

    for row in rows:
        values = [str(v or "") for v in row.values()]
        row_text = " ".join(values).lower()

        state_match = True
        if state:
            state_match = any(str(v or "").upper().strip() == state for v in row.values())

        if not state_match:
            continue

        score = 0

        # Exact phrase match
        if agency_name in row_text:
            score += 100

        # Individual word matches
        for term in search_terms:
            if term in row_text:
                score += 20

        # Prioritize agency/name/provider columns
        for k, v in row.items():
            key = str(k).lower()
            val = str(v or "").lower()

            if "name" in key or "provider" in key or "agency" in key:
                if agency_name in val:
                    score += 80

                for term in search_terms:
                    if term in val:
                        score += 30

        if score > 0:
            row["_match_score"] = score
            scored.append(row)

    scored = sorted(scored, key=lambda r: r.get("_match_score", 0), reverse=True)

    return scored[:10]

def cms_status():
    status = {}

    for name, item in DATASETS.items():
        status[name] = {
            "exists": os.path.exists(item["path"]),
            "path": item["path"],
            "dataset_id": item["id"]
        }

    return status

def get_cms_benchmarks(state=""):
    rows = load_csv(DATASETS["home_health_national"]["path"], limit=50000)

    denial_rates = []
    ar_days = []

    for r in rows:
        for k, v in r.items():
            try:
                val = float(v)
            except:
                continue

            key = k.lower()

            if "denial" in key:
                denial_rates.append(val)

            if "ar" in key or "receivable" in key:
                ar_days.append(val)

    def avg(lst):
        return round(sum(lst)/len(lst),2) if lst else None

    return {
        "cms_denial_avg": avg(denial_rates),
        "cms_ar_avg": avg(ar_days)
    }

def get_agency_cms_profile(agency_name="", state=""):
    matches = find_agency_by_name_state(agency_name, state)

    if not matches:
        return {
            "matched": False,
            "message": "No CMS agency match found. Audit will use benchmark-based scoring only.",
            "matches": []
        }

    top = matches[0]

    return {
        "matched": True,
        "message": "CMS agency match found.",
        "profile": top,
        "matches": matches[:5]
    }


def percentile_rank(value, population, higher_is_better=True):
    try:
        value = float(value)
        nums = [float(x) for x in population if x is not None]
    except:
        return None

    if not nums:
        return None

    if higher_is_better:
        below_or_equal = sum(1 for x in nums if x <= value)
    else:
        below_or_equal = sum(1 for x in nums if x >= value)

    return round((below_or_equal / len(nums)) * 100, 1)


def get_percentile_rankings(profile):
    rows = load_csv(DATASETS["home_health_agencies"]["path"], limit=100000)

    if not profile or not rows:
        return {}

    rankings = {}

    target_fields = {
        "star": True,
        "rating": True,
        "readmission": False,
        "hospitalization": False,
        "improvement": True,
        "timely": True,
        "quality": True
    }

    for field, value in profile.items():
        key = field.lower()

        matched_signal = None
        higher_is_better = True

        for signal, hib in target_fields.items():
            if signal in key:
                matched_signal = signal
                higher_is_better = hib
                break

        if not matched_signal:
            continue

        try:
            target_value = float(value)
        except:
            continue

        population = []

        for row in rows:
            try:
                population.append(float(row.get(field)))
            except:
                continue

        if len(population) < 10:
            continue

        pct = percentile_rank(target_value, population, higher_is_better)

        if pct is not None:
            rankings[field] = {
                "value": target_value,
                "percentile": pct,
                "higher_is_better": higher_is_better,
                "sample_size": len(population)
            }

    return rankings


def extract_performance_metrics(profile):
    metrics = {}

    if not profile:
        return metrics

    for k, v in profile.items():
        try:
            val = float(v)
        except:
            continue

        key = str(k).lower()

        if "star" in key:
            metrics["star_rating"] = val
        elif "readmission" in key:
            metrics["readmission_rate"] = val
        elif "improvement" in key:
            metrics["improvement_score"] = val
        elif "quality" in key:
            metrics["quality_score"] = val

    return metrics


def percentile_rank(value, population, higher_is_better=True):
    try:
        value = float(value)
        nums = [float(x) for x in population if x is not None]
    except:
        return None

    if not nums:
        return None

    if higher_is_better:
        count = sum(1 for x in nums if x <= value)
    else:
        count = sum(1 for x in nums if x >= value)

    return round((count / len(nums)) * 100, 1)


def get_percentile_rankings(profile):
    rows = load_csv(DATASETS["home_health_agencies"]["path"], limit=100000)

    if not profile or not rows:
        return {}

    rankings = {}

    target_fields = {
        "star": True,
        "rating": True,
        "readmission": False,
        "hospitalization": False,
        "improvement": True,
        "timely": True,
        "quality": True
    }

    for field, value in profile.items():
        key = str(field).lower()

        matched = False
        higher_is_better = True

        for signal, hib in target_fields.items():
            if signal in key:
                matched = True
                higher_is_better = hib
                break

        if not matched:
            continue

        try:
            target_value = float(value)
        except:
            continue

        population = []

        for row in rows:
            try:
                population.append(float(row.get(field)))
            except:
                continue

        if len(population) < 10:
            continue

        pct = percentile_rank(target_value, population, higher_is_better)

        if pct is not None:
            rankings[field] = {
                "value": target_value,
                "percentile": pct,
                "higher_is_better": higher_is_better,
                "sample_size": len(population)
            }

    return rankings


