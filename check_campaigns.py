import requests
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# Ignorar la advertencia de NotOpenSSLWarning
warnings.simplefilter('ignore', NotOpenSSLWarning)

LONG_LIVED_ACCESS_TOKEN = 'EAALsjQPcp6wBOZCK9ujv1VCxAWenaFUzPl6GWgGk5qQsZAanGy4mMUSNb1c2DWdOJItlmYnCLgOKZCqgZBZCVp3ZAShQO4XBhZAHT9s9A0vhwqajftg1lmhcFkCQPUj5w6LZBhazOCDi6c3ZBmS30fmLkG2b1MclHax8uNCDHvldCAg6hjZCrtAYyZBjpfH'
AD_ACCOUNT_ID = 'act_206988452103586'

def get_campaigns():
    url = f'https://graph.facebook.com/v17.0/{AD_ACCOUNT_ID}/campaigns'
    params = {
        'access_token': LONG_LIVED_ACCESS_TOKEN,
        'effective_status': '["ACTIVE"]'  # Asegurarse de que esto esté correctamente formateado como una cadena JSON
    }
    response = requests.get(url, params=params)
    print(f"Campaigns response: {response.json()}")  # Depuración
    return response.json()

def main():
    campaigns = get_campaigns()
    if 'error' in campaigns:
        print(f"Error obteniendo campañas activas: {campaigns['error']['message']} (Code: {campaigns['error']['code']})")
    else:
        print("Campañas activas obtenidas correctamente.")

if __name__ == "__main__":
    main()
