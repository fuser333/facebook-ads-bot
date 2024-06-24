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
ACCESS_TOKEN = 'EAALsjQPcp6wBOZCK9ujv1VCxAWenaFUzPl6GWgGk5qQsZAanGy4mMUSNb1c2DWdOJItlmYnCLgOKZCqgZBZCVp3ZAShQO4XBhZAHT9s9A0vhwqajftg1lmhcFkCQPUj5w6LZBhazOCDi6c3ZBmS30fmLkG2b1MclHax8uNCDHvldCAg6hjZCrtAYyZBjpfH'
AD_ACCOUNT_ID = '206988452103586'
EMAIL_USER = 'ingfuser33@gmail.com'
EMAIL_PASS = 'wtilmqzdhyoyynai'

def get_active_campaigns():
    url = f"https://graph.facebook.com/v16.0/act_{AD_ACCOUNT_ID}/campaigns"
    params = {
        'access_token': ACCESS_TOKEN,
        'effective_status': '["ACTIVE"]',
        'fields': 'name,objective,status'
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
        print("Correo enviado exitosamente.")

def main():
    campaigns = get_active_campaigns()
    print("Campañas activas:", campaigns)
    send_email("Prueba de campañas activas", str(campaigns))

if __name__ == "__main__":
    main()
