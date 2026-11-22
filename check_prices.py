import os
import json
import requests

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

with open("spiele.json", "r", encoding="utf-8") as f:
    spiele = json.load(f)

if os.path.exists("verlauf.json"):
    with open("verlauf.json", "r", encoding="utf-8") as f:
        verlauf = json.load(f)
else:
    verlauf = []

neue_deals_gefunden = False

for spiel, max_preis in spiele.items():
    url = "https://www.cheapshark/" + f".com/api/1.0/deals?title={spiel}&exact=0&upperPrice={max_preis}"
    response = requests.get(url)

    if response.status_code == 200:
        for deal in response.json():
            deal_id = deal['dealID']
            if spiel.lower() in deal['title'].lower() and deal_id not in verlauf:
                preis = float(deal['salePrice'])
                link = "https://www.cheapshark/" + f".com/redirect?dealID={deal_id}"
                status = "KOSTENLOS! 🎉" if preis == 0 else f"für ca. {preis}$ (~{max_preis}€)!"

                nachricht = {
                    "content": f"@everyone 🚨 Preisalarm: {deal['title']} ist aktuell {status}\nHier sichern: {link}"
                }
                requests.post(WEBHOOK_URL, json=nachricht)

                verlauf.append(deal_id)
                neue_deals_gefunden = True

if neue_deals_gefunden:
    with open("verlauf.json", "w", encoding="utf-8") as f:
        json.dump(verlauf, f, indent=2)
