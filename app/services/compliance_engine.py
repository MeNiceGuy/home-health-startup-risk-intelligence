import json
from pathlib import Path

DATA_PATH = Path("app/data/virginia_home_health_rules.json")

def get_state_rules(state: str):
    if state.lower() != "virginia":
        return {"error": "Only Virginia is available in this MVP."}

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
