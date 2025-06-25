import requests, datetime, os

TOKEN  = os.environ["LICHESS_KEY"].strip('"')    # GitHub secret (quotes OK)
TEAM   = "kingdomofblitzplayers"                 # team slug
ROUNDS = 10                                      # Swiss rounds
CLOCK  = 180                                     # 3 min base time

headers = {"Authorization": f"Bearer {TOKEN}"}

def create_swiss():
    # start 5 min from now so players can join
    now        = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    starts_at  = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    name       = f"KoB 3+0 Swiss {now:%m%d %H:%M}"[:30]  # ✅ shortened name

    data = {
        "name":           name,
        "clock.limit":    CLOCK,
        "clock.increment": 0,
        "startsAt":       starts_at,
        "nbRounds":       ROUNDS,
        "interval":       15,
        "variant":        "standard",
        "rated":          "true",
        "description":    "Auto-made by GitHub Actions 💥"
    }

    url = f"https://lichess.org/api/swiss/new/{TEAM}"
    r   = requests.post(url, headers=headers, data=data)

    if r.status_code == 200:
        print("✅  Tournament created:", r.json().get("url"))
    else:
        print("❌  Error", r.status_code, r.text)

if __name__ == "__main__":
    create_swiss()
