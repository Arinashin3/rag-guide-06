// Lab 3: 민원 분류  (= classify() 1건 · python -m eval.run_classify)
C.tab("민원 분류", (p) => {
  const q = C.el("textarea", { rows: 3 }, "결제가 두 번 됐습니다. 카드 명세서 첨부합니다.");
  const out = C.el("div");
  const one = C.el("button", { text: "1건 분류", onclick: () => C.busy(one, out, async () => {
    out.replaceChildren(C.table([await C.dev("/classify", { text: q.value })]));
  }) });
  const all = C.el("button", { text: "정확도 측정 (20건)", onclick: () => C.busy(all, out, async () => {
    out.replaceChildren(...C.runView(await C.dev("/run", { name: "run_classify" })));
  }) });
  p.append(C.el("h3", { text: "민원 분류 (Lab 3)" }), q, C.el("div", { class: "row" }, one, all), out);
});
