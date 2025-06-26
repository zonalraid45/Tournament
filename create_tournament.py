import requests, datetime, os, pathlib

# ─────────────── Settings ───────────────
TOKEN   = os.environ["LICHESS_KEY"].strip('"')
TEAM    = "testingsboy"
ROUNDS  = 10
CLOCK   = 60            # 1 + 0 bullet = 60 s total
NUM_TMT = 12
GAP_HRS = 2

headers = {"Authorization": f"Bearer {TOKEN}"}
url     = f"https://lichess.org/api/swiss/new/{TEAM}"

# ---------- NEW: read long description once ----------
DESC_FILE = pathlib.Path(__file__).with_name("description.txt")
try:
    with DESC_FILE.open(encoding="utf-8") as f:
        LONG_DESC = f.read().strip()
except FileNotFoundError:
    raise SystemExit("❌ description.txt not found!")

def create_one(idx: int, start_time: datetime.datetime) -> None:
    name = "KoB Daily bulletz swiss"[:30]

    payload = {
        "name":            name,
        "clock.limit":     CLOCK,
        "clock.increment": 0,
        "startsAt":        start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "nbRounds":        ROUNDS,
        "interval":        15,
        "variant":         "standard",
        "rated":           "true",
        "description":     LONG_DESC,        # ← pulled from file
    }

    r = requests.post(url, headers=headers, data=payload)
    if r.status_code == 200:
        print(f"✅  Tmt #{idx+1} created:", r.json().get('url'))
    else:
        print(f"❌  Tmt #{idx+1} error", r.status_code, r.text)

if __name__ == "__main__":
    first_start = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    for i in range(NUM_TMT):
        start = first_start + datetime.timedelta(hours=i * GAP_HRS)
        create_one(i, start)
