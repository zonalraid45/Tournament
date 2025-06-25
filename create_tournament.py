import requests, datetime, os

# ─────────────── Settings ───────────────
TOKEN   = os.environ["LICHESS_KEY"].strip('"')     # GitHub secret
TEAM    = "kingdomofblitzplayers"                  # team slug
ROUNDS  = 10                                       # Swiss rounds
CLOCK   = 180                                      # 3 + 0 blitz
NUM_TMT = 4                                        # how many to create
GAP_HRS = 2                                        # gap between starts

headers = {"Authorization": f"Bearer {TOKEN}"}
url     = f"https://lichess.org/api/swiss/new/{TEAM}"

def create_one(idx: int, start_time: datetime.datetime) -> None:
    # Build a compact ≤30-char name with only valid characters
    name = f"KoB 3-0 No{idx+1} {start_time:%m%d %H%M}"[:30]

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

    r = requests.post(url,
