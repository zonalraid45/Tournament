#!/usr/bin/env python3
"""
Broadcast "Hi guys" to your Lichess team.

• Requires an environment variable LICHESS_KEY holding a token with team:write.
• Team slug is hard-coded (testingsboy) but you can change it.
"""

import os, sys, textwrap, requests

# 1️⃣  Read and sanitize the token ------------------------------------------------
token = os.getenv("LICHESS_KEY", "").strip('"').strip("'")  # strip accidental quotes
if not token:
    sys.exit("❌  LICHESS_KEY is missing!")

# 2️⃣  Config you might tweak -----------------------------------------------------
TEAM_ID = "testingsboy"
MESSAGE = "Hi guys"

# 3️⃣  Quick token sanity-check: /api/account should return 200 ------------------
acct = requests.get(
    "https://lichess.org/api/account",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)
print("Account check HTTP:", acct.status_code)
if acct.status_code != 200:
    sys.exit("❌  Token invalid or missing scope/team:write.")

# 4️⃣  Send the team-wide message -------------------------------------------------
url = f"https://lichess.org/team/{TEAM_ID}/pm-all"        # <-- no /api prefix
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/x-www-form-urlencoded",
}
resp = requests.post(url, headers=headers, data={"msg": MESSAGE}, timeout=10)

# 5️⃣  Log the result -------------------------------------------------------------
if resp.status_code in (200, 204):                       # 204 = success, no content
    print("✅  Team message sent successfully.")
else:
    print(textwrap.dedent(f"""
        ❌  Failed to send message.
        HTTP {resp.status_code}
        First 500 bytes of response:
        {resp.text[:500]}
    """))
    resp.raise_for_status()
