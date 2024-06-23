import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib3
import warnings

# Suprimir advertencias de urllib3 sobre OpenSSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

# Datos de autenticación y configuración
ACCESS_TOKEN = 'EAALsjQPcp6wBOz4mUj3RP1mZBXye6wNqeVJOLiN8b2n0zacbLFElAewdRKVT1td5rvLl4xG9wpJysALmDhPSDMibQ9fYrj7fjkRvkPexSsoCm0ZCBHx7m85J1xLW74L3SJ9CcZBzlQ5odU4yRkmDoFMJPHY3IEzOvDkah8fXRtdpwpM90SCKXYz'
AD_ACCOUNT_ID = '206988452103586'
EMAIL_USER = 'ingfuser33@gmail.com'
EMAIL_PASS = 'wtilmqzdhyoyynai'

def get_active_campaigns():
    url = f"https://graph.facebook.com/v14.0/act_{AD_ACCOUNT_ID}/campaigns"
    params = {
        'access_token': ACCESS_TOKEN,
        'effective_status': ['ACTIVE'],
        'fields': 'name,objective,status'
    }
    response = requests.get(url, params=params)
    return response.json()

def get_adset_insights(adset_id):
    url = f"https://graph.facebook.com/v14.0/{adset_id}/insights"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'impressions,clicks,spend,cpm,cpc,ctr'
    }
    response = requests.get(url, params=params)
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

def adjust_budget(adset_id, new_budget):
    url = f"https://graph.facebook.com/v14.0/{adset_id}"
    params = {
        'access_token': ACCESS_TOKEN,
        'daily_budget': new_budget
    }
    response = requests.post(url, data=params)
    return response.json()

def main():
    campaigns = get_active_campaigns()
    if 'data' in campaigns:
        for campaign in campaigns['data']:
            campaign_id = campaign['id']
            campaign_name = campaign['name']
            
            adsets_url = f"https://graph.facebook.com/v14.0/{campaign_id}/adsets"
            adsets_params = {
                'access_token': ACCESS_TOKEN,
                'fields': 'name'
            }
            adsets_response = requests.get(adsets_url, params=adsets_params)
            adsets = adsets_response.json()
            
            if 'data' in adsets:
                for adset in adsets['data']:
                    adset_id = adset['id']
                    adset_name = adset['name']
                    insights = get_adset_insights(adset_id)
                    
                    if 'data' in insights and len(insights['data']) > 0:
                        insight = insights['data'][0]
                        impressions = int(insight['impressions'])
                        clicks = int(insight['clicks'])
                        spend = float(insight['spend'])
                        cpm = float(insight['cpm'])
                        cpc = float(insight['cpc'])
                        ctr = float(insight['ctr'])
                        
                        # Analizar y ajustar presupuesto
                        if ctr > 5.0 and cpc < 0.05:
                            new_budget = 2 * spend
                        else:
                            new_budget = 0.5 * spend
                        
                        adjust_budget(adset_id, new_budget)
                        
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
                        """
                        send_email(email_subject, email_body)

if __name__ == "__main__":
    main()
