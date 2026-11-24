import os
from datetime import date

import requests

HR_URL = os.environ.get("HR_URL", "http://localhost:9000")


def balance(user_id: str) -> dict:
    r = requests.get(f"{HR_URL}/balance/{user_id}", timeout=5)
    r.raise_for_status()
    return r.json()


def is_holiday(d: date) -> bool:
    r = requests.get(f"{HR_URL}/holiday/{d.isoformat()}", timeout=5)
    r.raise_for_status()
    return r.json()["holiday"]


def create_request(user_id: str, d: date, kind: str, days: float, idem_key: str) -> dict:
    r = requests.post(f"{HR_URL}/requests", timeout=5,
                      json={"user_id": user_id, "date": d.isoformat(), "kind": kind,
                            "days": days, "idem_key": idem_key})
    r.raise_for_status()
    return r.json()
