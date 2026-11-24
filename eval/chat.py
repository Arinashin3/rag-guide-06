import argparse
import uuid

import requests

ap = argparse.ArgumentParser()
ap.add_argument("text")
ap.add_argument("--base-url", default="http://localhost:8000")
ap.add_argument("--answer", help="확인 질문에 자동으로 답할 값 (예 또는 아니오)")
ap.add_argument("--session", default=str(uuid.uuid4())[:8])
a = ap.parse_args()
u = a.base_url.rstrip("/") + "/chat"
r = requests.post(u, json={"session_id": a.session, "text": a.text}, timeout=90).json()
print(f"[{r['type']}] {r['text']}")
if r["type"] == "confirm":
    ans = a.answer or input("사용자 > ")
    r = requests.post(u, json={"session_id": a.session, "confirm": ans.strip() in ("예", "y", "yes", "네")},
                      timeout=90).json()
    print(f"[{r['type']}] {r['text']}")
