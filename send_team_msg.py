#!/usr/bin/env python3
"""
Broadcast “Hi guys” to the Lichess team `testingsgirl`.
Requires a secret LICHESS_KEY holding a token with team:write scope.
"""

import os, sys, textwrap, requests

token = os.getenv("LICHESS_KEY", "").strip('"').strip("'")
if not token:
    sys.exit("❌  LICHESS_KEY is missing!")

TEAM_ID = "testingsgirl"
MESSAGE = "Hi guys"

# ── sanity-check the token ────────────────────────────────────────────
acct = requests.get(
    "https://lichess.org/api/account",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)
print("Account check HTTP:", acct.status_code)
if acct.status_code != 200:
    sys.exit("❌  Token invalid or lacks team:write")

# ── send the team-wide PM ─────────────────────────────────────────────
url = f"https://lichess.org/team/{TEAM_ID}/pm-all"          # ← no /api/
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/x-www-form-urlencoded",
}

resp = requests.post(url, headers=headers, data={"message": MESSAGE}, timeout=10)

# ── report result ─────────────────────────────────────────────────────
if resp.status_code in (200, 204):
    print("✅  Team message sent successfully.")
else:
    print(textwrap.dedent(f"""
        ❌  Failed to send message.
        HTTP {resp.status_code}
        First 500 bytes:
        {resp.text[:500]}
    """))
    resp.raise_for_status()
