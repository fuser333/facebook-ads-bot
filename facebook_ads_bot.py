import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# Variables de la aplicación
app_id = '823040352757676'
app_secret = 'db46c9d90dfa967520a0fd7dcd15d5f6'
ACCESS_TOKEN = 'EAALsjQPcp6wBO2My9QMqcfhDwyaf1hMoSUKpGQYIFZARjLBXrLA51ZCyUrEdcnmoZAMKqsTZB5huf8NDaVGYkKy0kR0x6BYjmy6PwurphDri2hPCU4PEjs9Jf5dajysQCriSZAptNwh9RDHu0dLI3SRFN3mZAgfJUwVJ4EtzU0ZC2Pmh43EJwIRcm9m'  # Token de acceso a largo plazo
AD_ACCOUNT_ID = '206988452103586'  # Sin el prefijo 'act_'
API_VERSION = 'v13.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}/'

# Función para renovar el token de acceso
def renew_access_token():
    global ACCESS_TOKEN
    url = f"https://graph.facebook.com/{API_VERSION}/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    ACCESS_TOKEN = response.json().get('access_token')
    print("Token de acceso renovado:", ACCESS_TOKEN)

# Función para enviar correos electrónicos
def send_email(subject, body, to_email):
    from_email = "ingfuser33@gmail.com"
    from_password = "wtilmqzdhyoyynai"  # Usa aquí tu contraseña de aplicación generada
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

# Funciones para obtener campañas, conjuntos de anuncios e insights
def get_campaigns(access_token):
    url = f"{BASE_URL}act_{AD_ACCOUNT_ID}/campaigns"
    params = {
        'access_token': access_token,
        'fields': 'id,name,status',
        'effective_status': json.dumps(['ACTIVE'])
    }
    response = requests.get(url, params=params)
    return response.json()

def get_adsets(campaign_id, access_token):
    url = f"{BASE_URL}{campaign_id}/adsets"
    params = {
        'access_token': access_token,
        'fields': 'id,name,status',
        'effective_status': json.dumps(['ACTIVE'])
    }
    response = requests.get(url, params=params)
    return response.json()

def get_insights(adset_id, access_token):
    url = f"{BASE_URL}{adset_id}/insights"
    params = {
        'access_token': access_token,
        'fields': 'impressions,clicks,spend,cpm,cpc,ctr',
        'time_range': json.dumps({
            'since': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'until': datetime.now().strftime('%Y-%m-%d')
        })
    }
    response = requests.get(url, params=params)
    return response.json()

def update_adset(adset_id, new_budget, access_token):
    url = f"{BASE_URL}{adset_id}"
    payload = {
        'daily_budget': new_budget,
        'access_token': access_token
    }
    response = requests.post(url, data=payload)
    return response.json()

# Función para chequear y actualizar el conjunto de anuncios basado en el rendimiento
def check_and_update_adset(adset_id, adset_name, insights, access_token):
    if 'data' in insights:
        insights_data = insights['data']
        if not insights_data:
            print(f"No hay datos de rendimiento para el conjunto de anuncios {adset_name}.")
        else:
            for insight in insights_data:
                impressions = insight.get('impressions', 'N/A')
                clicks = insight.get('clicks', 'N/A')
                spend = insight.get('spend', 'N/A')
                cpm = insight.get('cpm', 'N/A')
                cpc = insight.get('cpc', 'N/A')
                ctr = insight.get('ctr', 'N/A')

                print(f"Insights para {adset_name}:")
                print(f"  Impresiones: {impressions}")
                print(f"  Clicks: {clicks}")
                print(f"  Gasto: {spend}")
                print(f"  CPM: {cpm}")
                print(f"  CPC: {cpc}")
                print(f"  CTR: {ctr}")

                # Definir umbrales de rendimiento
                target_ctr = 1.0
                target_leads = 10
                if ctr != 'N/A' and float(ctr) < target_ctr:
                    new_budget = 5000  # Aumenta el presupuesto en base a tus necesidades
                    update_response = update_adset(adset_id, new_budget, access_token)
                    print(f"Presupuesto actualizado para {adset_name}: {update_response}")

                # Enviar correo de notificación
                subject = f"Rendimiento del Conjunto de Anuncios: {adset_name}"
                body = (f"Conjunto de Anuncios: {adset_name}\n"
                        f"Impresiones: {impressions}\n"
                        f"Clicks: {clicks}\n"
                        f"Gasto: {spend}\n"
                        f"CPM: {cpm}\n"
                        f"CPC: {cpc}\n"
                        f"CTR: {ctr}\n")

                send_email(subject, body, to_email)
    else:
        print(f"Error al obtener insights para {adset_name}: {insights}")

if __name__ == "__main__":
    to_email = "ingfuser33@gmail.com"

    # Renovar el token de acceso
    renew_access_token()

    # Obtener campañas activas
    print("Obteniendo campañas activas...")
    campaigns = get_campaigns(ACCESS_TOKEN)
    
    if 'data' in campaigns:
        campaign_data = campaigns['data']
        if not campaign_data:
            print("No hay campañas activas.")
        else:
            for campaign in campaign_data:
                campaign_id = campaign['id']
                campaign_name = campaign['name']
                print(f"Campaña activa: {campaign_name} (ID: {campaign_id})")
                
                # Obtener conjuntos de anuncios activos
                print(f"Obteniendo conjuntos de anuncios activos para la campaña {campaign_name}...")
                adsets = get_adsets(campaign_id, ACCESS_TOKEN)
                
                if 'data' in adsets:
                    adset_data = adsets['data']
                    if not adset_data:
                        print(f"No hay conjuntos de anuncios activos para la campaña {campaign_name}.")
                    else:
                        for adset in adset_data:
                            adset_id = adset['id']
                            adset_name = adset['name']
                            print(f"Conjunto de anuncios activo: {adset_name} (ID: {adset_id})")
                            
                            # Obtener insights del conjunto de anuncios
                            print(f"Obteniendo insights para el conjunto de anuncios {adset_name}...")
                            insights = get_insights(adset_id, ACCESS_TOKEN)
                            
                            # Chequear y actualizar conjunto de anuncios basado en el rendimiento
                            check_and_update_adset(adset_id, adset_name, insights, ACCESS_TOKEN)
                else:
                    print(f"Error obteniendo conjuntos de anuncios para la campaña {campaign_name}: {adsets}")
    else:
        print(f"Error obteniendo campañas: {campaigns}")




