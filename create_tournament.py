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
    name = f"KoB 3-0 No
