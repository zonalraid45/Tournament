#!/usr/bin/env python3
"""
send_team_msg.py
----------------
Broadcasts “Hi guys” to the Lichess team `testingsboy`.

Prerequisites
-------------
1. Create a personal API token on Lichess with **team:write** scope.
2. Add that token to your GitHub repo secrets:
      Name  : LICHESS_KEY
      Value : lip_xxxxxxxxxxxxxxxxx    ← (no quotes)
3. Ensure the token’s account is a leader/admin of the team.

This script is called by your GitHub Actions workflow at 19:17 IST.
"""

import os, sys, textwrap, requests

# ──────────────────────────────────────────────────────────────────────
# 1. Read token from environment and remove stray quote characters
# ──────────────────────────────────────────────────────────────────────
token = os.getenv("LICHESS_KEY", "").strip('"').strip("'")
if not token:
    sys.exit("❌  LICHESS_KEY environment variable is missing!")

# ──────────────────────────────────────────────────────────────────────
# 2. Configuration
# ──────────────────────────────────────────────────────────────────────
TEAM_ID = "testingsboy"
MESSAGE = "Hi guys"

# ──────────────────────────────────────────────────────────────────────
# 3. Quick sanity-check: confirm token really works
# ──────────────────────────────────────────────────────────────────────
acct = requests.get(
    "https://lichess.org/api/account",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)
print("Account check HTTP:", acct.status_code)
if acct.status_code != 200:
    sys.exit("❌  Token invalid or lacks team:write scope")

# ──────────────────────────────────────────────────────────────────────
# 4. Send the team-wide message (official API endpoint)
# ──────────────────────────────────────────────────────────────────────
url = f"https://lichess.org/api/team/{TEAM_ID}/pm-all"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/x-www-form-urlencoded",
}

resp = requests.post(url, headers=headers, data={"msg": MESSAGE}, timeout=10)

# ──────────────────────────────────────────────────────────────────────
# 5. Report result
# ──────────────────────────────────────────────────────────────────────
if resp.status_code in (200, 204):
    print("✅  Team message sent successfully.")
else:
    print(textwrap.dedent(f"""
        ❌  Failed to send message.
        HTTP {resp.status_code}
        First 500 bytes of response:
        {resp.text[:500]}
    """))
    resp.raise_for_status()
