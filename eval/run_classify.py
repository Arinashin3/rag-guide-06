import json

from app.classify import classify

rows = [json.loads(l) for l in open("eval/complaints.jsonl", encoding="utf-8")]
ok, report = 0, []
for r in rows:
    out = classify(r["text"])
    hit = out["decision"] == r["label"]
    ok += hit
    report.append((r["id"], r["label"], out["decision"], out["confidence"], "O" if hit else "X"))
print(f"정확도 {ok}/{len(rows)} = {ok/len(rows):.0%}")
for row in report:
    print(*row, sep="\t")
