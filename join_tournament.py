#!/usr/bin/env python3
"""
Join a Lichess arena (team-battle) tournament.

Env-vars expected
-----------------
TOR          – your personal Lichess OAuth token (with *tournament:write* scope)
TMT_ID       – the 8-character tournament ID, e.g. "doF1DMaz"
TEAM_ID      – the team slug, e.g. "royalracer-fans"
"""

import os
import sys
import requests

TOKEN   = os.environ["TOR"].strip('"')
TMT_ID  = os.getenv("TMT_ID", "doF1DMaz")
TEAM_ID = os.getenv("TEAM_ID", "royalracer-fans")

URL = f"https://lichess.org/api/tournament/{TMT_ID}/join"   # arena & team-battle endpoint

resp = requests.post(
    URL,
    headers={"Authorization": f"Bearer {TOKEN}"},
    data={"team": TEAM_ID},          # required for team battles
    timeout=15,
)

print("HTTP", resp.status_code)
print(resp.text)

if resp.status_code != 200:
    sys.exit("❌  join failed")
