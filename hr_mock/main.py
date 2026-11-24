"""모의 휴가 시스템 (실습용, SQLite)"""
import os
import sqlite3

from fastapi import FastAPI
from pydantic import BaseModel

DB = os.environ.get("HR_DB", "/tmp/hr.db")
HOLIDAYS = {"2026-12-25", "2027-01-01"}
app = FastAPI(title="hr-mock")


def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.execute("CREATE TABLE IF NOT EXISTS employees(id TEXT PRIMARY KEY, name TEXT, remaining REAL, used REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS requests(id INTEGER PRIMARY KEY AUTOINCREMENT, emp_id TEXT, date TEXT, "
              "kind TEXT, days REAL, idem_key TEXT UNIQUE)")
    if not c.execute("SELECT 1 FROM employees").fetchone():
        c.executemany("INSERT INTO employees VALUES(?,?,?,?)",
                      [("e001", "홍길동", 7, 8), ("e002", "김대리", 3, 12), ("e003", "이사원", 11, 4)])
        c.commit()
    return c


class Req(BaseModel):
    user_id: str
    date: str
    kind: str
    days: float
    idem_key: str = ""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/balance/{user_id}")
def balance(user_id: str):
    r = conn().execute("SELECT remaining, used FROM employees WHERE id=?", (user_id,)).fetchone()
    return {"remaining": r["remaining"] if r else 0, "used": r["used"] if r else 0, "year": 2026}


@app.get("/holiday/{d}")
def holiday(d: str):
    return {"holiday": d in HOLIDAYS}


@app.post("/requests")
def create(req: Req):
    c = conn()
    if req.idem_key:
        old = c.execute("SELECT id FROM requests WHERE idem_key=?", (req.idem_key,)).fetchone()
        if old:
            rem = c.execute("SELECT remaining FROM employees WHERE id=?", (req.user_id,)).fetchone()["remaining"]
            return {"request_id": f"LV-{old['id']:04d}", "remaining": rem, "duplicate": True}
    cur = c.execute("INSERT INTO requests(emp_id,date,kind,days,idem_key) VALUES(?,?,?,?,?)",
                    (req.user_id, req.date, req.kind, req.days, req.idem_key or None))
    c.execute("UPDATE employees SET remaining = remaining - ?, used = used + ? WHERE id=?",
              (req.days, req.days, req.user_id))
    c.commit()
    rem = c.execute("SELECT remaining FROM employees WHERE id=?", (req.user_id,)).fetchone()["remaining"]
    return {"request_id": f"LV-{cur.lastrowid:04d}", "remaining": rem}
