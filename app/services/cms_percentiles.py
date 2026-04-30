import csv, os

CMS_FILE = "data/cms/home_health_agencies.csv"

def to_float(value):
    try:
        return float(str(value).replace("%","").strip())
    except:
        return None

def percentile_rank(value, population, higher_is_better=True):
    value = to_float(value)
    nums = [to_float(x) for x in population]
    nums = [x for x in nums if x is not None]

    if value is None or not nums:
        return None

    if higher_is_better:
        count = sum(1 for x in nums if x <= value)
    else:
        count = sum(1 for x in nums if x >= value)

    return round((count / len(nums)) * 100, 1)

def cms_percentile_benchmarks(agency_profile):
    if not agency_profile or not os.path.exists(CMS_FILE):
        return {}

    with open(CMS_FILE, newline="", encoding="utf-8-sig", errors="ignore") as f:
        rows = list(csv.DictReader(f))

    results = {}

    signals = {
        "star": True,
        "rating": True,
        "quality": True,
        "timely": True,
        "improvement": True,
        "readmission": False,
        "hospitalization": False
    }

    for field, value in agency_profile.items():
        key = str(field).lower()
        matched = False
        higher_is_better = True

        for signal, hib in signals.items():
            if signal in key:
                matched = True
                higher_is_better = hib
                break

        if not matched:
            continue

        population = [row.get(field) for row in rows if row.get(field) not in [None, ""]]

        if len(population) < 10:
            continue

        pct = percentile_rank(value, population, higher_is_better)

        if pct is not None:
            results[field] = {
                "value": value,
                "percentile": pct,
                "sample_size": len(population),
                "higher_is_better": higher_is_better
            }

    return results


