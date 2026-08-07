import requests
from datetime import datetime


SOFASCORE_URL = "https://www.sofascore.com/api/v1/sport/football/events/live"


def get_live_matches():
    try:
        response = requests.get(
            SOFASCORE_URL,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        events = data.get("events", [])

        matches = []

        for event in events:
            home = event.get("homeTeam", {}).get("name", "Ev Sahibi")
            away = event.get("awayTeam", {}).get("name", "Deplasman")

            home_score = event.get("homeScore", {}).get("current", 0)
            away_score = event.get("awayScore", {}).get("current", 0)

            status = event.get("status", {})
            minute = status.get("gameTime", "")

            matches.append({
                "id": event.get("id"),
                "home": home,
                "away": away,
                "home_score": home_score,
                "away_score": away,
                "minute": minute
            })

        return matches

    except Exception as e:
        print("Sofascore bağlantı hatası:", e)
        return []


if __name__ == "__main__":
    matches = get_live_matches()

    print(f"\nCanlı maç sayısı: {len(matches)}")
    print(f"Güncelleme: {datetime.now()}\n")

    for match in matches:
        print(
            f"{match['minute']} | "
            f"{match['home']} {match['home_score']}-"
            f"{match['away_score']} {match['away']}"
        )
