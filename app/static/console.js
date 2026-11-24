// 실습 콘솔 공통 기능. 탭 파일은 C.tab(제목, 만드는함수) 로 자신을 등록합니다.
const C = {
  // 화면 요소 만들기. 글자는 항상 textContent 로 넣습니다 (innerHTML 금지: 모델 답변 속 태그가 실행되지 않게)
  el(tag, attrs = {}, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "text") e.textContent = v;
      else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v);
    }
    e.append(...kids);                    // 문자열은 글자로 들어갑니다
    return e;
  },

  tab(title, build) {
    const pane = C.el("section");
    const btn = C.el("button", { text: title, onclick: () => C.open(btn, pane) });
    document.getElementById("tabs").append(btn);
    document.getElementById("panes").append(pane);
    build(pane);
    if (!document.querySelector("nav button.on")) C.open(btn, pane);
  },

  open(btn, pane) {
    document.querySelectorAll("nav button, section").forEach((x) => x.classList.remove("on"));
    btn.classList.add("on");
    pane.classList.add("on");
  },

  // 콘솔 서버(내 PC)의 /dev API 호출
  async dev(path, body) {
    const opt = body === undefined ? {} : {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
    const r = await fetch("/dev" + path, opt);
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(typeof data.detail === "string" ? data.detail : "오류 " + r.status + " " + JSON.stringify(data.detail || ""));
    return data;
  },

  // 대상 API 호출 (상단의 주소 · X-Canary 사용). 콘솔 서버가 대신 보내고 상태 코드 · 버전 헤더를 돌려줍니다
  api(path, body) {
    return C.dev("/remote", {
      base_url: document.getElementById("base").value.trim(), path, body,
      canary: document.getElementById("canary").checked });
  },

  // 버튼 실행 중 표시와 오류 처리
  async busy(btn, out, fn) {
    btn.disabled = true;
    out.replaceChildren(C.el("div", { class: "muted", text: "실행 중…" }));
    try { await fn(); } catch (e) { out.replaceChildren(C.el("div", { class: "bad", text: "⚠ " + e.message })); }
    finally { btn.disabled = false; }
  },

  json(x) { return typeof x === "string" ? x : JSON.stringify(x, null, 2); },

  // /dev/run 결과(명령 · 종료 코드 · 출력) 보기
  runView(r) {
    return [C.el("div", { class: r.code === 0 ? "ok" : "bad", text: `$ ${r.cmd}  → 종료 코드 ${r.code} (${r.sec}초)` }),
            C.el("pre", { text: r.out })];
  },

  // 객체 배열 → 표 (true 는 초록, false 는 빨강)
  table(rows) {
    if (!Array.isArray(rows) || !rows.length || typeof rows[0] !== "object") return C.el("pre", { text: C.json(rows) });
    const cols = Object.keys(rows[0]);
    const t = C.el("table", {}, C.el("tr", {}, ...cols.map((c) => C.el("th", { text: c }))));
    for (const row of rows) {
      t.append(C.el("tr", {}, ...cols.map((c) => {
        const v = row[c];
        return C.el("td", { text: typeof v === "object" ? JSON.stringify(v) : String(v),
                            class: v === true ? "ok" : v === false ? "bad" : "" });
      })));
    }
    return t;
  },
};

C.dev("/ping")
  .then((p) => { document.getElementById("env").textContent = `콘솔 서버: AWS_PROFILE=${p.profile} · ${p.region}`; })
  .catch(() => { document.getElementById("env").textContent = "콘솔 서버 연결 안 됨"; });
