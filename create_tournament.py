import requests, datetime, os, pathlib

# ─────────────── Settings ───────────────
TOKEN   = os.environ["LICHESS_KEY"].strip('"')
TEAM    = "testingsboy"

# 8 time-controls (secs), each 2 h apart
CONTROLS = [
    ( 30, 0,  "½+0"),    # 0.5 min
    ( 60, 0,  "1+0"),
    ( 60, 1,  "1+1"),
    (120, 0,  "2+0"),
    ( 45, 0,  "¾+0"),    # 0.75 min
    (120, 1,  "2+1"),
    ( 90, 0,  "1½+0"),   # 1.5 min
    ( 45, 1,  "¾+1"),    # 0.75 min + 1 s
]

ROUNDS       = 10            # Swiss rounds
ROUND_GAP    = 15            # minutes between rounds
GAP_HRS      = 2             # gap between tournaments

CONST_NAME   = "Daily Bullet Swiss toor"  # ← ASCII-only title

headers = {"Authorization": f"Bearer {TOKEN}"}
url     = f"https://lichess.org/api/swiss/new/{TEAM}"

# ---------- read long description once ----------
DESC_PATH = pathlib.Path(__file__).with_name("description.txt")
try:
    LONG_DESC = DESC_PATH.read_text(encoding="utf-8").strip()
except FileNotFoundError:
    raise SystemExit("❌  description.txt not found!")

def create_one(start_time: datetime.datetime,
               limit: int, inc: int, label: str) -> None:
    """Create a single Swiss tournament on Lichess."""
    payload = {
        "name":            CONST_NAME,
        "clock.limit":     limit,
        "clock.increment": inc,
        "startsAt":        start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "nbRounds":        ROUNDS,
        "interval":        ROUND_GAP,
        "variant":         "standard",
        "rated":           "true",
        "description":     LONG_DESC,
    }

    r = requests.post(url, headers=headers, data=payload)
    if r.status_code == 200:
        print(f"✅  {label} created:", r.json().get("url"))
    else:
        print(f"❌  {label} error", r.status_code, r.text)

if __name__ == "__main__":
    first_start = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

    for i, (limit, inc, label) in enumerate(CONTROLS):
        start = first_start + datetime.timedelta(hours=i * GAP_HRS)
        create_one(start, limit, inc, label)
