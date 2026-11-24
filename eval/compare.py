import json
import sys

a, b = sys.argv[1], sys.argv[2]
ra = json.load(open(f"eval/results/{a}.json", encoding="utf-8"))
rb = json.load(open(f"eval/results/{b}.json", encoding="utf-8"))
for kind in ("questions", "attacks"):
    A = {r["id"]: r["pass"] for r in ra[kind]}
    B = {r["id"]: r["pass"] for r in rb[kind]}
    for k in A:
        if k in B and A[k] != B[k]:
            print(f"{k:5} {'O' if A[k] else 'X'} → {'O' if B[k] else 'X'}")
pa = sum(r["pass"] for r in ra["questions"])
pb = sum(r["pass"] for r in rb["questions"])
print(f"통과 {a}: {pa}/30  {b}: {pb}/30")
