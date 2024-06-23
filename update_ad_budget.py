import requests
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# Ignorar la advertencia de NotOpenSSLWarning
warnings.simplefilter('ignore', NotOpenSSLWarning)

LONG_LIVED_ACCESS_TOKEN = 'EAALsjQPcp6wBOZCK9ujv1VCxAWenaFUzPl6GWgGk5qQsZAanGy4mMUSNb1c2DWdOJItlmYnCLgOKZCqgZBZCVp3ZAShQO4XBhZAHT9s9A0vhwqajftg1lmhcFkCQPUj5w6LZBhazOCDi6c3ZBmS30fmLkG2b1MclHax8uNCDHvldCAg6hjZCrtAYyZBjpfH'
AD_ACCOUNT_ID = 'act_206988452103586'
DAILY_BUDGET_CENTS = 1000  # 10 dollars in cents

def get_campaigns():
    url = f'https://graph.facebook.com/v17.0/{AD_ACCOUNT_ID}/campaigns'
    params = {
        'access_token': LONG_LIVED_ACCESS_TOKEN,
        'effective_status': '["ACTIVE"]'
    }
    response = requests.get(url, params=params)
    return response.json()

def get_adsets(campaign_id):
    url = f'https://graph.facebook.com/v17.0/{campaign_id}/adsets'
    params = {
        'access_token': LONG_LIVED_ACCESS_TOKEN,
        'fields': 'id,name,status,insights{impressions,clicks,spend,cpm,cpc,ctr,date_start,date_stop},daily_budget'
    }
    response = requests.get(url, params=params)
    return response.json()

def get_ads(adset_id):
    url = f'https://graph.facebook.com/v17.0/{adset_id}/ads'
    params = {
        'access_token': LONG_LIVED_ACCESS_TOKEN,
        'fields': 'id,name,status'
    }
    response = requests.get(url, params=params)
    return response.json()

def update_ad_budget(ad_id, budget):
    url = f'https://graph.facebook.com/v17.0/{ad_id}'
    params = {
        'access_token': LONG_LIVED_ACCESS_TOKEN,
        'daily_budget': budget
    }
    response = requests.post(url, data=params)
    return response.json()

def main():
    campaigns = get_campaigns()
    if 'error' in campaigns:
        print(f"Error obteniendo campañas activas: {campaigns['error']['message']} (Code: {campaigns['error']['code']})")
        return
    
    for campaign in campaigns['data']:
        adsets = get_adsets(campaign['id'])
        if 'error' in adsets:
            print(f"Error obteniendo adsets para la campaña {campaign['id']}: {adsets['error']['message']} (Code: {adsets['error']['code']})")
            continue
        
        for adset in adsets['data']:
            if adset['status'] == 'ACTIVE':
                ads = get_ads(adset['id'])
                if 'error' in ads:
                    print(f"Error obteniendo ads para el adset {adset['id']}: {ads['error']['message']} (Code: {ads['error']['code']})")
                    continue
                
                for ad in ads['data']:
                    if ad['status'] == 'ACTIVE':
                        budget_response = update_ad_budget(ad['id'], DAILY_BUDGET_CENTS)
                        if 'error' in budget_response:
                            print(f"Error ajustando presupuesto para el anuncio {ad['id']}: {budget_response['error']['message']} (Code: {budget_response['error']['code']})")
                        else:
                            print(f"Presupuesto ajustado correctamente para el anuncio {ad['id']}: {DAILY_BUDGET_CENTS} centavos")

if __name__ == "__main__":
    main()

