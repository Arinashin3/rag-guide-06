import argparse
import json
import random
import statistics
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import requests

ap = argparse.ArgumentParser()
ap.add_argument("--base-url", required=True)
ap.add_argument("--n", type=int, default=100)
a = ap.parse_args()
qs = [json.loads(l)["q"] for l in open("eval/questions.jsonl", encoding="utf-8")]
random.seed(1)


def one(_):
    q = random.choice(qs)
    try:
        r = requests.post(a.base_url.rstrip("/") + "/ask", json={"q": q}, timeout=90)
        body = r.json() if r.status_code == 200 else {}
        return (r.headers.get("X-Prompt-Version", "?"), r.status_code, r.elapsed.total_seconds() * 1000,
                body.get("usage", {}).get("outputTokens", 0), "찾을 수 없습니다" in body.get("answer", ""))
    except Exception:
        return ("?", 599, 0, 0, False)


with ThreadPoolExecutor(4) as ex:
    rows = list(ex.map(one, range(a.n)))
g = defaultdict(list)
for r in rows:
    g[r[0]].append(r)
print(f"{'버전':8} {'요청':>4} {'평균지연':>8} {'p95':>7} {'평균출력토큰':>10} {'거절률':>6} {'5xx':>4}")
for v, rs in sorted(g.items()):
    lat = sorted(x[2] for x in rs)
    print(f"{v:8} {len(rs):>4} {statistics.mean(lat)/1000:>7.1f}s {lat[max(int(len(lat)*.95)-1, 0)]/1000:>6.1f}s "
          f"{statistics.mean(x[3] for x in rs):>10.0f} {sum(x[4] for x in rs)/len(rs):>6.0%} {sum(x[1] >= 500 for x in rs):>4}")
