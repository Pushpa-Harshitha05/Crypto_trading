from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests

def index(request):
    response = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets", 
        params={"vs_currency": "usd", "ids": "bitcoin,ethereum,cardano"}
    )
    data = response.json()

    if response.status_code != 200:
        return render(request, 'dashboard/error.html', {'error': 'Failed to fetch data from API'})
    
    if response.status_code == 429:
        return render(request, 'dashboard/error.html', {'error': 'Rate limit hit. Please try again later.'})
    
    if not data:
        return render(request, 'dashboard/error.html', {'error': 'No data returned from API'})

    filtered_data = {
        coin["id"]: {
            "current_price": coin["current_price"],
            "market_cap": coin["market_cap"],
            "total_volume": coin["total_volume"],
            "price_change_percentage_24h": coin["price_change_percentage_24h"]
        }
        for coin in data
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "crypto-prices",
        {
            'type': 'send_crypto_data',
            'message': filtered_data
        }          
    )

    return render(request, 'dashboard/homepage.html')
