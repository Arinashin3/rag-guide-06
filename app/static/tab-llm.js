// Lab 2: 첫 LLM 호출과 사용량 확인  (= python -c "from app.llm import ask; ...")
C.tab("LLM 호출", (p) => {
  const sys = C.el("input", { type: "text", value: "한 문장으로 답하라" });
  const q = C.el("textarea", { rows: 3 }, "연차휴가란?");
  const max = C.el("input", { type: "number", value: 1024, min: 16, style: "width:90px" });
  const times = C.el("input", { type: "number", value: 1, min: 1, max: 5, style: "width:60px" });
  const out = C.el("div");
  const go = C.el("button", { text: "보내기", onclick: () => C.busy(go, out, async () => {
    const items = [];
    for (let i = 0; i < Number(times.value); i++) {
      const r = await C.dev("/llm", { system: sys.value, user: q.value, max_tokens: Number(max.value) });
      items.push(C.el("pre", { text: r.text }), C.el("div", {
        class: r.stop === "max_tokens" ? "bad" : "muted",
        text: `stop=${r.stop} · 입력 ${r.usage.inputTokens} · 출력 ${r.usage.outputTokens} 토큰 · ${r.ms}ms · 약 $${r.usd}` }));
    }
    out.replaceChildren(...items);
  }) });
  p.append(C.el("h3", { text: "LLM 호출 (Lab 2)" }),
    C.el("div", { text: "system" }), sys, C.el("div", { text: "질문" }), q,
    C.el("div", { class: "row" }, "max_tokens", max, "반복", times, go), out);
});
