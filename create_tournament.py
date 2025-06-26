import requests, datetime, os

# ─────────────── Settings ───────────────
TOKEN   = os.environ["LICHESS_KEY"].strip('"')     # GitHub secret
TEAM    = "testingsboy"                  # team slug
ROUNDS  = 10                                       # Swiss rounds
CLOCK   = 60                                      # 3 + 0 blitz
NUM_TMT = 12                                        # how many to create
GAP_HRS = 2                                        # gap between starts

headers = {"Authorization": f"Bearer {TOKEN}"}
url     = f"https://lichess.org/api/swiss/new/{TEAM}"

def create_one(idx: int, start_time: datetime.datetime) -> None:
    # Build a compact ≤30-char name with only valid characters
    name = f"KoB Daily bulletz swiss"[:30]

    payload = {
        "name":            name,
        "clock.limit":     CLOCK,
        "clock.increment": 0,
        "startsAt":        start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "nbRounds":        ROUNDS,
        "interval":        15,
        "variant":         "standard",
        "rated":           "true",
        "description":     "Auto-made by GitHub Actions"
    }

    r = requests.post(url, headers=headers, data=payload)

    if r.status_code == 200:
        print(f"✅  Tmt #{idx+1} created:", r.json().get("url"))
    else:
        print(f"❌  Tmt #{idx+1} error", r.status_code, r.text)

if __name__ == "__main__":
    first_start = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    for i in range(NUM_TMT):
        start = first_start + datetime.timedelta(hours=i * GAP_HRS)
        create_one(i, start)
