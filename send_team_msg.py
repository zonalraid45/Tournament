#!/usr/bin/env python3
"""
Sends a team-wide message on Lichess.
"""

import os, requests, sys, textwrap

# Get token from GitHub secrets (via environment variable)
token = os.getenv("LICHESS_KEY", "").strip('"').strip("'")

# Team ID (hardcoded or passed in future)
team_id = "testingsboy"

# Your message here
msg = "Hi guys"

if not token:
    sys.exit("❌  LICHESS_KEY is missing!")

url = f"https://lichess.org/api/team/{team_id}/pm-all"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/x-www-form-urlencoded"
}

resp = requests.post(url, headers=headers, data={"msg": msg}, timeout=10)

if resp.status_code in (200, 204):
    print("✅  Team message sent successfully.")
else:
    print(textwrap.dedent(f"""
        ❌  Failed to send message. HTTP {resp.status_code}
        Response:
        {resp.text[:500]}
    """))
    resp.raise_for_status()
