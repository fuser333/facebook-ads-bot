import requests
import smtplib
from email.mime.text import MIMEText
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# Ignorar la advertencia de NotOpenSSLWarning
warnings.simplefilter('ignore', NotOpenSSLWarning)

# Configuración de la aplicación y usuario
LONG_LIVED_ACCESS_TOKEN = 'EAALsjQPcp6wBOZCK9ujv1VCxAWenaFUzPl6GWgGk5qQsZAanGy4mMUSNb1c2DWdOJItlmYnCLgOKZCqgZBZCVp3ZAShQO4XBhZAHT9s9A0vhwqajftg1lmhcFkCQPUj5w6LZBhazOCDi6c3ZBmS30fmLkG2b1MclHax8uNCDHvldCAg6hjZCrtAYyZBjpfH'
AD_ACCOUNT_ID = 'act_206988452103586'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'ingfuser33@gmail.com'
SMTP_PASS = 'wtilmqzdhyoyynai'
RECIPIENT_EMAIL = 'ingfuser33@gmail.com'

def get_campaigns():
    url = f'https://graph.facebook.com/v17.0/{AD_ACCOUNT_ID}/campaigns'
    params = {
        'access_token': LONG_LIVED_ACCESS_TOKEN,
        'effective_status': '["ACTIVE"]'  # Asegurarse de que esto esté correctamente formateado como una cadena JSON
    }
    response = requests.get(url, params=params)
    print(f"Campaigns response: {response.json()}")  # Depuración
    return response.json()

def get_adsets(campaign_id):
    url = f'https://graph.facebook.com/v17.0/{campaign_id}/adsets'
    params = {
        'access_token': LONG_LIVED_ACCESS_TOKEN,
        'fields': 'id,name,status,insights{impressions,clicks,spend,cpm,cpc,ctr,date_start,date_stop},daily_budget'
    }
    response = requests.get(url, params=params)
    print(f"Adsets response for campaign {campaign_id}: {response.json()}")  # Depuración
    return response.json()

def update_budget(adset_id, budget):
    url = f'https://graph.facebook.com/v17.0/{adset_id}'
    params = {
        'access_token': LONG_LIVED_ACCESS_TOKEN,
        'daily_budget': budget
    }
    response = requests.post(url, data=params)
    print(f"Update budget response for adset {adset_id}: {response.json()}")  # Depuración
    return response.json()

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = RECIPIENT_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, RECIPIENT_EMAIL, msg.as_string())

def main():
    campaigns = get_campaigns()
    if 'error' in campaigns:
        send_email("Error obteniendo campañas activas", f"{campaigns['error']['message']} (Code: {campaigns['error']['code']})")
        return

    for campaign in campaigns['data']:
        adsets = get_adsets(campaign['id'])
        if 'error' in adsets:
            send_email(f"Error obteniendo adsets para la campaña {campaign['id']}", f"{adsets['error']['message']} (Code: {adsets['error']['code']})")
            continue

        for adset in adsets['data']:
            if adset['status'] == 'ACTIVE':
                if 'insights' in adset and adset['insights']['data']:
                    insights = adset['insights']['data'][0]
                    impressions = int(insights['impressions'])
                    clicks = int(insights['clicks'])
                    spend = float(insights['spend'])
                    cpm = float(insights['cpm'])
                    cpc = float(insights['cpc'])
                    ctr = float(insights['ctr'])
                    date_start = insights['date_start']
                    date_stop = insights['date_stop']

                    new_budget = 1000  # Ajustar según la lógica de negocio

                    # Verificar si se puede ajustar el presupuesto del conjunto de anuncios
                    if adset.get('daily_budget'):
                        budget_response = update_budget(adset['id'], new_budget)
                        if 'error' in budget_response:
                            if budget_response['error']['code'] == 100 and budget_response['error']['error_subcode'] == 1885621:
                                send_email(f"Error ajustando presupuesto para {adset['id']}", f"No se puede establecer el presupuesto del conjunto de anuncios ya que la campaña tiene un presupuesto configurado. (Code: {budget_response['error']['code']}, Subcode: {budget_response['error']['error_subcode']})")
                            else:
                                send_email(f"Error ajustando presupuesto para {adset['id']}", f"{budget_response['error']['message']} (Code: {budget_response['error']['code']}, Subcode: {budget_response['error'].get('error_subcode', 'N/A')})")
                        else:
                            send_email(f"Presupuesto ajustado para {adset['id']}", f"Nuevo presupuesto: {new_budget} centavos")
                    else:
                        send_email(f"No se puede ajustar presupuesto para {adset['id']}", "La campaña tiene un presupuesto configurado.")

if __name__ == "__main__":
    main()

