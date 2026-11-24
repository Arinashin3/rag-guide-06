import json
import logging
import os
import time

import boto3

MODEL = os.environ.get("LLM_MODEL", "global.anthropic.claude-sonnet-5-5")
client = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "ap-northeast-2"))
log = logging.getLogger("llm")


def ask(system: str, user: str, max_tokens: int = 1024) -> dict:
    t0 = time.time()
    resp = client.converse(
        modelId=MODEL,
        system=[{"text": system}],
        messages=[{"role": "user", "content": [{"text": user}]}],
        inferenceConfig={"maxTokens": max_tokens},
    )
    text = "".join(b["text"] for b in resp["output"]["message"]["content"] if "text" in b)
    return {"text": text, "usage": resp["usage"], "stop": resp["stopReason"],
            "ms": int((time.time() - t0) * 1000)}


def ask_logged(system, user, **kw):
    r = ask(system, user, **kw)
    log.info(json.dumps({
        "prompt_version": os.environ.get("PROMPT_VERSION", "v1"),
        "in": r["usage"]["inputTokens"], "out": r["usage"]["outputTokens"],
        "stop": r["stop"], "ms": r["ms"],
    }))
    if r["stop"] == "max_tokens":
        log.warning("응답이 maxTokens에서 잘렸습니다")
    return r
