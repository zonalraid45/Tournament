import requests, datetime, os

TOKEN = os.environ["LICHESS_KEY"].strip('"')
TEAM = "kingdomofblitzplayers"
ROUNDS = 10

headers = {"Authorization": f"Bearer {TOKEN}"}

def create_swiss():
    now = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    starts_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    name = f"KoB Blitz Swiss {now.strftime('%Y-%m-%d %H:%M')} UTC"

    data = {
        "name": name,
        "teamId": TEAM,
        "clock.limit": 180,
        "clock.increment": 0,
        "startsAt": starts_at,
        "nbRounds": ROUNDS,
        "interval": 15,
        "variant": "standard",
        "rated": "true",
        "description": "Auto-made by GitHub Actions 💥",
    }

    r = requests.post("https://lichess.org/api/swiss", headers=headers, data=data)

    if r.status_code == 200:
        print("✅  Tournament created:", r.json().get("url"))
    else:
        print("❌  Error", r.status_code, r.text)

if __name__ == "__main__":
    create_swiss()
