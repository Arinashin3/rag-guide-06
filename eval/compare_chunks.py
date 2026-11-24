import json

import numpy as np

from app.index import embed
from app.llm import ask

QS = ["연차는 다음 해로 이월되나요?", "출장비 정산은 언제까지 해야 하나요?", "병가가 3일을 넘으면 어떻게 하나요?",
      "수습 기간에도 연차가 생기나요?", "서울 출장 숙박비 한도는 얼마인가요?"]
PROMPT = open("prompts/v1.txt", encoding="utf-8").read()
print("질문 | " + " | ".join(f"index_{s}" for s in (200, 500, 1000)))
for q in QS:
    qv = np.array(embed(q), dtype=np.float32)
    row = []
    for s in (200, 500, 1000):
        d = f"index_{s}"
        V = np.load(f"{d}/vectors.npy")
        C = json.load(open(f"{d}/chunks.json", encoding="utf-8"))
        top = np.argsort(-(V @ qv))[:4]
        ctx = "\n\n".join(f"<발췌 id='{C[i]['id']}'>\n{C[i]['text']}\n</발췌>" for i in top)
        r = ask(PROMPT, f"{ctx}\n\n<질문>{q}</질문>", max_tokens=500)
        row.append(f"{r['text'][:60].replace(chr(10), ' ')}… (입력 {r['usage']['inputTokens']}토큰)")
    print(q, "|", " | ".join(row))
