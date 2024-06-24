import requests
import urllib3
import warnings

# Suprimir advertencias de urllib3 sobre OpenSSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

# Datos de autenticación y configuración
ACCESS_TOKEN = 'EAALsjQPcp6wBOZCK9ujv1VCxAWenaFUzPl6GWgGk5qQsZAanGy4mMUSNb1c2DWdOJItlmYnCLgOKZCqgZBZCVp3ZAShQO4XBhZAHT9s9A0vhwqajftg1lmhcFkCQPUj5w6LZBhazOCDi6c3ZBmS30fmLkG2b1MclHax8uNCDHvldCAg6hjZCrtAYyZBjpfH'
AD_ACCOUNT_ID = '206988452103586'

def get_active_campaigns():
    url = f"https://graph.facebook.com/v16.0/act_{AD_ACCOUNT_ID}/campaigns"
    params = {
        'access_token': ACCESS_TOKEN,
        'effective_status': '["ACTIVE"]',
        'fields': 'name,objective,status'
    }
    response = requests.get(url, params=params, verify=False)
    return response.json()

def main():
    campaigns = get_active_campaigns()
    print("Campañas activas:", campaigns)

if __name__ == "__main__":
    main()
