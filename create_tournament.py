#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a full day of Swiss tournaments according to the timetable
supplied by Utsa.  All times are interpreted in Asia/Kolkata (IST)
and sent to the Lichess API in UTC.
"""
import os, datetime as dt, pathlib, requests
from zoneinfo import ZoneInfo   # Python ≥3.9

# ─────────────── Settings ───────────────
TOKEN   = os.environ["LICHESS_KEY"].strip('"')
TEAM    = "testingsgirl"
ROUNDS  = 8
INTERVAL = 30                   # seconds between rounds
IST     = ZoneInfo("Asia/Kolkata")

headers = {"Authorization": f"Bearer {TOKEN}"}
URL     = f"https://lichess.org/api/swiss/new/{TEAM}"

# ---------- read long description once ----------
DESC_FILE = pathlib.Path(__file__).with_name("description.txt")
try:
    LONG_DESC = DESC_FILE.read_text(encoding="utf-8").strip()
except FileNotFoundError:
    raise SystemExit("❌ description.txt not found!")

# ─────────────── Timetable ───────────────
SCHEDULE = [
    #  time ,      title,      min, inc
    ("00:00", "Bullet Bash",    1,  0),
    ("00:30", "Blitz Brawl",    5,  0),
    ("01:00", "Classical Clash",30,  0),
    ("01:30", "Rapid Rumble",  10,  0),
    ("02:00", "Blitz Brawl",    3,  2),
    ("02:30", "Bullet Bash",    2,  1),
    ("03:00", "Rapid Rumble",  15, 10),
    ("03:30", "Blitz Brawl",    5,  2),
    ("04:00", "Classical Clash",30, 20),
    ("04:30", "Bullet Bash",    1,  0),
    ("05:00", "Blitz Brawl",    3,  0),
    ("05:30", "Rapid Rumble",  10,  5),
    ("06:00", "Blitz Brawl",    5,  0),
    ("06:30", "Bullet Bash",    2,  1),
    ("07:00", "Classical Clash",30,  0),
    ("07:30", "Rapid Rumble",  10,  0),
    ("08:00", "Blitz Brawl",    3,  2),
    ("08:30", "Bullet Bash",    1,  0),
    ("09:00", "Rapid Rumble",  15, 10),
    ("09:30", "Blitz Brawl",    5,  2),
    ("10:00", "Classical Clash",30, 20),
    ("10:30", "Bullet Bash",    2,  1),
    ("11:00", "Blitz Brawl",    3,  0),
    ("11:30", "Rapid Rumble",  10,  5),
    ("12:00", "Blitz Brawl",    5,  0),
    ("12:30", "Bullet Bash",    1,  0),
    ("13:00", "Classical Clash",30,  0),
    ("13:30", "Rapid Rumble",  10,  0),
    ("14:00", "Blitz Brawl",    3,  2),
    ("14:30", "Bullet Bash",    2,  1),
    ("15:00", "Rapid Rumble",  15, 10),
    ("15:30", "Blitz Brawl",    5,  2),
    ("16:00", "Classical Clash",30, 20),
    ("16:30", "Bullet Bash",    1,  0),
    ("17:00", "Blitz Brawl",    3,  0),
    ("17:30", "Rapid Rumble",  10,  5),
    ("18:00", "Blitz Brawl",    5,  0),
    ("18:30", "Bullet Bash",    2,  1),
    ("19:00", "Classical Clash",30,  0),
    ("19:30", "Rapid Rumble",  10,  0),
    ("20:00", "Blitz Brawl",    3,  2),
    ("20:30", "Bullet Bash",    1,  0),
    ("21:00", "Rapid Rumble",  15, 10),
    ("21:30", "Blitz Brawl",    5,  2),
    ("22:00", "Classical Clash",30, 20),
    ("22:30", "Bullet Bash",    2,  1),
    ("23:00", "Blitz Brawl",    3,  0),
    ("23:30", "Rapid Rumble",  10,  5),
]

# ─────────────── Helper ───────────────
def next_occurrence(time_str: str) -> dt.datetime:
    """Return the next datetime (≥ now + 5 min) for HH:MM in IST."""
    hh, mm = map(int, time_str.split(":"))
    today   = dt.date.today()
    now_ist = dt.datetime.now(IST)
    cand    = dt.datetime.combine(today, dt.time(hh, mm), tzinfo=IST)
    if cand < now_ist + dt.timedelta(minutes=5):
        cand += dt.timedelta(days=1)
    return cand.astimezone(dt.timezone.utc)   # convert to UTC

def create_tmt(idx: int, name: str, minutes: int, inc: int, start_utc: dt.datetime) -> None:
    payload = {
        "name":            f"{name} {minutes}+{inc}"[:30],
        "clock.limit":     minutes * 60,
        "clock.increment": inc,
        "startsAt":        start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "nbRounds":        ROUNDS,
        "interval":        INTERVAL,
        "variant":         "standard",
        "rated":           "true",
        "description":     LONG_DESC,
    }
    r = requests.post(URL, headers=headers, data=payload, timeout=15)
    if r.status_code == 200:
        print(f"✅  {payload['name']:<25} →", r.json().get("url"))
    else:
        print(f"❌  {payload['name']:<25} ({r.status_code}) {r.text[:120]}")

# ─────────────── Main ───────────────
if __name__ == "__main__":
    for idx, (t, title, mins, inc) in enumerate(SCHEDULE):
        start = next_occurrence(t)
        create_tmt(idx, title, mins, inc, start)
