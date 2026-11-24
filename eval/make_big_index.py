import argparse
import json
import os

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--n", type=int, default=50000)
ap.add_argument("--out", default="index_big")
a = ap.parse_args()
rng = np.random.default_rng(0)
v = rng.standard_normal((a.n, 1024), dtype=np.float32)
v /= np.linalg.norm(v, axis=1, keepdims=True)
os.makedirs(a.out, exist_ok=True)
np.save(f"{a.out}/vectors.npy", v)
json.dump([{"id": f"dummy.md#{i}", "text": "dummy"} for i in range(a.n)],
          open(f"{a.out}/chunks.json", "w", encoding="utf-8"), ensure_ascii=False)
print(f"{a.out}/vectors.npy {v.nbytes / 1e6:.0f}MB")
