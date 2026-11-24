import json
import sys

from app import agent
from app.tools import today_kst

if __name__ == "__main__":
    text = sys.argv[1]
    show = "--show-messages" in sys.argv
    res = agent.run([{"role": "user", "content": [{"text": text}]}], "e001", today_kst())
    if show:
        for i, m in enumerate(res["messages"], 1):
            for b in m["content"]:
                kind = next(iter(b))
                print(f"{i} | {m['role']:9} | {kind}: {json.dumps(b[kind], ensure_ascii=False)[:110]}")
    print(f"결과({res['type']}):", res.get("text") or res.get("tool"))
