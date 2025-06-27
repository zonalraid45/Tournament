#!/usr/bin/env python3
"""
Auto-join a Lichess team-battle arena.

Environment variables (NO quotes):
  TOR       – personal token   (scopes: tournament:write, team:write)
  TMT_ID    – 8-character arena / team-battle ID   (default: doF1DMaz)
  TEAM_ID   – team slug                            (default: royalracer-fans)
"""

import os, sys, requests

# ───────── CONSTANTS ─────────
TOKEN   = os.environ["TOR"].strip().strip('"').strip("'")   # trims stray whitespace/quotes
TMT_ID  = os.getenv("TMT_ID",  "doF1DMaz")
TEAM_ID = os.getenv("TEAM_ID", "royalracer-fans")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept":        "application/json",
}

# ───────── DEBUG ─────────
print(f"🔎 Token prefix: {TOKEN[:3]}")
print(f"🔎 Token length: {len(TOKEN)}")

# ───────── HELPERS ─────────
def get_username() -> str:
    r = requests.get("https://lichess.org/api/account", headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()["username"]

def is_member(username: str) -> bool:
    """
    Fast 200/404 membership probe (no JSON parsing).
    200 → already in team, 404 → not in team.
    """
    url = f"https://lichess.org/api/team/{TEAM_ID}/user/{username}"
    r   = requests.get(url, headers=HEADERS, timeout=10)
    return r.status_code == 200

def join_team() -> None:
    """
    Join the team. 200 = open-join success, 202 = request filed for approval.
    """
    url = f"https://lichess.org/api/team/{TEAM_ID}/join"
    r   = requests.post(url, headers=HEADERS, timeout=15)
    print("📩 team-join:", r.status_code, r.text.strip() or "(no body)")
    if r.status_code not in (200, 202):
        sys.exit("❌ could not join the team")

def join_tournament() -> None:
    """
    Join the team-battle tournament.
    """
    url = f"https://lichess.org/api/tournament/{TMT_ID}/join"
    r   = requests.post(url, headers=HEADERS, data={"team": TEAM_ID}, timeout=15)
    print("🏁 tmt-join :", r.status_code, r.text.strip() or "(no body)")
    if r.status_code != 200:
        sys.exit("❌ could not join the tournament")

# ───────── MAIN ─────────
if __name__ == "__main__":
    try:
        user = get_username()
        print(f"🔐 authenticated as {user}")
    except Exception as e:
        sys.exit(f"❌ authentication failed – {e}")

    if is_member(user):
        print(f"✅ already in team '{TEAM_ID}' – skipping team join.")
    else:
        print(f"ℹ️ joining team '{TEAM_ID}' …")
        join_team()

    join_tournament()
