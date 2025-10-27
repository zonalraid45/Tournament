#!/usr/bin/env python3
"""
Continuously wait until 5:30 PM IST, October 27,
then broadcast the message from t.txt to the Lichess team `testingsgirl`.

Requires:
- Environment variable LICHESS_KEY with team:write scope
- File t.txt containing the message text
"""

import os, sys, time, textwrap, requests
from datetime import datetime
import pytz

TEAM_ID = "jkl"
MSG_FILE = "t.txt"

# ── setup timezone ────────────────────────────────────────────────────
IST = pytz.timezone("Asia/Kolkata")

def get_time():
    """Return current IST time"""
    return datetime.now(IST)

def log(msg):
    print(f"[{get_time().strftime('%I:%M %p, %d %b %Y')}] {msg}", flush=True)

# ── check token ───────────────────────────────────────────────────────
token = os.getenv("LICHESS_KEY", "").strip('"').strip("'")
if not token:
    sys.exit("❌  LICHESS_KEY is missing!")

# ── read message ──────────────────────────────────────────────────────
if not os.path.exists(MSG_FILE):
    sys.exit(f"❌  {MSG_FILE} not found! Please create it with your message.")
with open(MSG_FILE, "r", encoding="utf-8") as f:
    MESSAGE = f.read().strip()
if not MESSAGE:
    sys.exit("❌  Message file is empty!")

# ── wait until 5:30 PM, October 27 ────────────────────────────────────
TARGET_DAY, TARGET_MONTH, TARGET_HOUR, TARGET_MINUTE = 27, 10, 17, 30

while True:
    now = get_time()
    if (
        now.day == TARGET_DAY and
        now.month == TARGET_MONTH and
        now.hour == TARGET_HOUR and
        now.minute == TARGET_MINUTE
    ):
        log("🎯 It's 5:30 PM IST — sending team message now!")
        break
    else:
        log("Waiting... current IST time not yet 5:30 PM, Oct 27.")
        time.sleep(60)

# ── sanity-check token ────────────────────────────────────────────────
acct = requests.get(
    "htt
