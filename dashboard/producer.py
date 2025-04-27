import subprocess
import time
import requests
import json

last_data = None

while True:
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": "usd",
                "ids": "bitcoin,ethereum,cardano"
            }
        )

        if response.status_code == 429:
            print("Rate limit hit. Sleeping for 60 seconds...")
            time.sleep(60)
            continue

        elif response.status_code != 200:
            print(f"Unexpected status code {response.status_code}. Retrying in 30 seconds.")
            time.sleep(30)
            continue

        data = response.json()

        # Filter and send relevant data
        filtered_data = {
            coin["id"]: {
                "current_price": coin["current_price"],
                "market_cap": coin["market_cap"],
                "total_volume": coin["total_volume"],
                "price_change_percentage_24h": coin["price_change_percentage_24h"],
                "price_change_percentage_7d": coin.get("price_change_percentage_7d_in_currency", "N/A")
            }
            for coin in data
        }

        data_str = json.dumps(filtered_data, indent=4)
        subprocess.run(f'echo \'{data_str}\' | fluvio produce crypto-prices', shell=True)
        last_data = filtered_data

        time.sleep(20)

    except Exception as e:
        print(f"Error occurred: {e}. Retrying...")
        time.sleep(30)
