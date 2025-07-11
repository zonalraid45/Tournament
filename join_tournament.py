#!/usr/bin/env python3
"""
Join a Lichess arena tournament (not a team-battle).

Env-vars expected:
------------------
TOR – your personal Lichess OAuth token (with *tournament:write* scope)
"""

import os
import sys
import requests

TOKEN = os.environ["TOR"].strip('"')

# ✅ Hardcoded tournament ID
TMT_ID = "MAqOvnzA"  # <-- Replace with your tournament ID if needed

URL = f"https://lichess.org/api/tournament/{TMT_ID}/join"

try:
    resp = requests.post(
        URL,
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=15,
    )
except requests.exceptions.RequestException as e:
    sys.exit(f"❌  Request error: {e}")

print("HTTP", resp.status_code)
print(resp.text)

if resp.status_code == 200:
    print("✅  Successfully joined the tournament.")
elif "already joined" in resp.text.lower():
    print("ℹ️  You have already joined this tournament.")
else:
    sys.exit("❌  Join failed.")
