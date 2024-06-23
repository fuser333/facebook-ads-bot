import requests
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# Ignorar la advertencia de NotOpenSSLWarning
warnings.simplefilter('ignore', NotOpenSSLWarning)

LONG_LIVED_ACCESS_TOKEN = 'EAALsjQPcp6wBOZCK9ujv1VCxAWenaFUzPl6GWgGk5qQsZAanGy4mMUSNb1c2DWdOJItlmYnCLgOKZCqgZBZCVp3ZAShQO4XBhZAHT9s9A0vhwqajftg1lmhcFkCQPUj5w6LZBhazOCDi6c3ZBmS30fmLkG2b1MclHax8uNCDHvldCAg6hjZCrtAYyZBjpfH'
CAMPAIGN_ID = '120206639723420724'  # Reemplazar con el ID de una campaña activa

def get_adsets(campaign_id):
    url = f'https://graph.facebook.com/v17.0/{campaign_id}/adsets'
    params = {
        'access_token': LONG_LIVED_ACCESS_TOKEN,
        'fields': 'id,name,status,insights{impressions,clicks,spend,cpm,cpc,ctr,date_start,date_stop},daily_budget'
    }
    response = requests.get(url, params=params)
    print(f"Adsets response for campaign {campaign_id}: {response.json()}")  # Depuración
    return response.json()

def main():
    adsets = get_adsets(CAMPAIGN_ID)
    if 'error' in adsets:
        print(f"Error obteniendo adsets para la campaña {CAMPAIGN_ID}: {adsets['error']['message']} (Code: {adsets['error']['code']})")
    else:
        print("Conjuntos de anuncios obtenidos correctamente.")

if __name__ == "__main__":
    main()
