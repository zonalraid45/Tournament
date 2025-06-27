#!/usr/bin/env python3
"""
Auto-join a Lichess team-battle arena.

Environment variables (no quotes in the values!)
------------------------------------------------
TOR       – personal access token with scopes  tournament:write  and  team:write
TMT_ID    – 8-character arena / team-battle ID       (default: doF1DMaz)
TEAM_ID   – team slug                                (default: royalracer-fans)
"""

import os, sys, json, requests

# ──────────────── CONSTANTS ────────────────
TOKEN   = os.environ["TOR"].strip().strip('"').strip("'")  # removes whitespace + accidental quotes
TMT_ID  = os.getenv("TMT_ID",  "doF1DMaz")
TEAM_ID = os.getenv("TEAM_ID", "royalracer-fans")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept":        "application/json",
}

# ──────────────── DEBUG CHECKS ────────────────
print(f"🔎 Token prefix: {TOKEN[:3]}")
print(f"🔎 Token length: {len(TOKEN)}")

# ──────────────── HELPERS ────────────────
def get_username() -> str:
    """Resolve the account behind the token."""
    r = requests.get("https://lichess.org/api/account", headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()["username"]

def is_member(username: str) -> bool:
    """
    Return True if the account already belongs to TEAM_ID.
    Uses the lightweight ND-JSON stream /api/team/of/{username}.
    """
    url = f"https://lichess.org/api/team/of/{username}"
    r   = requests.get(url,
                       headers={**HEADERS, "Accept": "application/x-ndjson"},
                       stream=True, timeout=15)
    r.raise_for_status()
    for raw in r.iter_lines():
        if raw and json.loads(raw).get("id") == TEAM_ID:
            return True
    return False

def join_team() -> None:
    """
    POST /team/{TEAM_ID}/join – works for open teams (200) or
    files a join request when approval is required (202).
    """
    url = f"https://lichess.org/team/{TEAM_ID}/join"
    r   = requests.post(url, headers=HEADERS, timeout=15)
    print("📩  team-join response:", r.status_code, r.text.strip() or "(no body)")
    if r.status_code not in (200, 202):
        sys.exit("❌  could not join the team")

def join_tournament() -> None:
    """
    POST /api/tournament/{TMT_ID}/join with the team slug for a battle.
    """
    url = f"https://lichess.org/api/tournament/{TMT_ID}/join"
    r   = requests.post(url, headers=HEADERS, data={"team": TEAM_ID}, timeout=15)
    print("🏁  tournament-join response:", r.status_code, r.text.strip() or "(no body)")
    if r.status_code != 200:
        sys.exit("❌  could not join the tournament")

# ──────────────── MAIN FLOW ────────────────
if __name__ == "__main__":
    try:
        user = get_username()
        print(f"🔐  authenticated as {user}")
    except Exception as e:
        sys.exit(f"❌  Failed to authenticate – {e}")

    if is_member(user):
        print(f"✅  already in team '{TEAM_ID}' – skipping team join.")
    else:
        print(f"ℹ️  not in team '{TEAM_ID}' – trying to join the team first…")
        join_team()

    join_tournament()
