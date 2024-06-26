import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib3
import warnings
import logging

# Configurar el logging para guardar la salida en un archivo
logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Suprimir advertencias de urllib3 sobre OpenSSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

# Datos de autenticación y configuración
ACCESS_TOKEN = 'EAALsjQPcp6wBOZCK9ujv1VCxAWenaFUzPl6GWgGk5qQsZAanGy4mMUSNb1c2DWdOJItlmYnCLgOKZCqgZBZCVp3ZAShQO4XBhZAHT9s9A0vhwqajftg1lmhcFkCQPUj5w6LZBhazOCDi6c3ZBmS30fmLkG2b1MclHax8uNCDHvldCAg6hjZCrtAYyZBjpfH'
AD_ACCOUNT_ID = '206988452103586'
EMAIL_USER = 'ingfuser33@gmail.com'
EMAIL_PASS = 'wtilmqzdhyoyynai'
MAX_BUDGET = 10  # en dólares (equivalente a $10)
MONTHLY_BUDGET = 1500  # en dólares (equivalente a $1500)
DAILY_BUDGET = MONTHLY_BUDGET // 30  # Presupuesto diario basado en el presupuesto mensual

def get_active_campaigns():
    url = f"https://graph.facebook.com/v14.0/act_{AD_ACCOUNT_ID}/campaigns"
    params = {
        'access_token': ACCESS_TOKEN,
        'effective_status[0]': 'ACTIVE',  # Aquí nos aseguramos de que sea un array
        'fields': 'name,objective,status'
    }
    response = requests.get(url, params=params, verify=False)
    return response.json()

def get_adset_insights(adset_id):
    url = f"https://graph.facebook.com/v14.0/{adset_id}/insights"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'impressions,clicks,spend,cpm,cpc,ctr'
    }
    response = requests.get(url, params=params, verify=False)
    return response.json()

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, EMAIL_USER, text)

def adjust_budget(entity_id, new_budget, entity_type='adset'):
    url = f"https://graph.facebook.com/v14.0/{entity_id}"
    params = {
        'access_token': ACCESS_TOKEN,
        'daily_budget': new_budget * 100  # Convertir a centavos
    }
    response = requests.post(url, data=params, verify=False)
    return response.json()

def main():
    campaigns = get_active_campaigns()
    logging.info("Campañas obtenidas: %s", campaigns)
    if 'data' in campaigns:
        for campaign in campaigns['data']:
            campaign_id = campaign['id']
            campaign_name = campaign['name']
            
            adsets_url = f"https://graph.facebook.com/v14.0/{campaign_id}/adsets"
            adsets_params = {
                'access_token': ACCESS_TOKEN,
                'fields': 'name,status'
            }
            adsets_response = requests.get(adsets_url, params=adsets_params, verify=False)
            adsets = adsets_response.json()
            logging.info("Conjuntos de anuncios obtenidos: %s", adsets)
            
            if 'data' in adsets:
                for adset in adsets['data']:
                    adset_id = adset['id']
                    adset_name = adset['name']
                    adset_status = adset['status']
                    
                    if adset_status == 'ACTIVE':
                        insights = get_adset_insights(adset_id)
                        logging.info("Insights obtenidos: %s", insights)
                        
                        if 'data' in insights and len(insights['data']) > 0:
                            insight = insights['data'][0]
                            impressions = int(insight['impressions'])
                            clicks = int(insight['clicks'])
                            spend = float(insight['spend'])
                            cpm = float(insight['cpm'])
                            cpc = float(insight['cpc'])
                            ctr = float(insight['ctr'])
                            
                            # Analizar y ajustar presupuesto
                            if adset_name == 'Terrenos Clientes Potenciales':
                                new_budget = int((MONTHLY_BUDGET * 0.70) // 30)  # 70% del presupuesto mensual dividido en 30 días
                            else:
                                if ctr > 5.0 and cpc < 0.05:
                                    new_budget = MAX_BUDGET  # Aumentar el presupuesto al máximo permitido
                                else:
                                    new_budget = int(MAX_BUDGET * 0.5)  # Reducir el presupuesto a la mitad
                            
                            # Ajustar presupuesto del conjunto de anuncios
                            adjust_budget_response = adjust_budget(adset_id, new_budget)
                            logging.info("Respuesta al ajustar presupuesto: %s", adjust_budget_response)
                            if 'error' not in adjust_budget_response:
                                budget_status = f"Presupuesto ajustado correctamente para el conjunto de anuncios {adset_name}: {new_budget} dólares"
                            else:
                                budget_status = f"Error ajustando presupuesto para {adset_name}: {adjust_budget_response['error']['message']}"
                                if adjust_budget_response['error']['code'] == 100 and adjust_budget_response['error']['error_subcode'] == 1885621:
                                    # Intentar ajustar el presupuesto de la campaña
                                    campaign_budget_response = adjust_budget(campaign_id, DAILY_BUDGET, entity_type='campaign')
                                    logging.info("Respuesta al ajustar presupuesto de la campaña: %s", campaign_budget_response)
                                    if 'error' not in campaign_budget_response:
                                        budget_status = f"Presupuesto ajustado correctamente para la campaña {campaign_name}: {DAILY_BUDGET} dólares"
                                    else:
                                        budget_status = f"Error ajustando presupuesto para la campaña {campaign_name}: {campaign_budget_response['error']['message']}"
                            
                            email_subject = f"Insights para {adset_name} en {campaign_name}"
                            email_body = f"""
                            Campaña: {campaign_name}
                            Conjunto de anuncios: {adset_name}
                            Impresiones: {impressions}
                            Clicks: {clicks}
                            Gasto: {spend}
                            CPM: {cpm}
                            CPC: {cpc}
                            CTR: {ctr}
                            Nuevo presupuesto: {new_budget}
                            Estado del ajuste: {budget_status}
                            """
                            send_email(email_subject, email_body)
                            logging.info("Correo enviado con el siguiente cuerpo: %s", email_body)

if __name__ == "__main__":
    main()
