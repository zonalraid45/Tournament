#!/usr/bin/env python3
"""
Join a Lichess arena tournament (not a team-battle).

Env-vars expected
-----------------
TOR     – your personal Lichess OAuth token (with *tournament:write* scope)
TMT_ID  – the 8-character tournament ID, e.g. "MAqOvnzA"
"""

import os
import sys
import requests

TOKEN   = os.environ["TOR"].strip('"')
TMT_ID  = os.getenv("TMT_ID", "MAqOvnzA")

URL = f"https://lichess.org/api/tournament/{TMT_ID}/join"

resp = requests.post(
    URL,
    headers={"Authorization": f"Bearer {TOKEN}"},
    timeout=15,
)

print("HTTP", resp.status_code)
print(resp.text)

if resp.status_code != 200:
    sys.exit("❌  join failed")
