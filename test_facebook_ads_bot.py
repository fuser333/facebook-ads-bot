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

def test_email():
    subject = "Prueba de correo"
    body = "Este es un correo de prueba."
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            text = msg.as_string()
            server.sendmail(EMAIL_USER, EMAIL_USER, text)
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error enviando correo: {e}")

def test_facebook_api():
    url = f"https://graph.facebook.com/v14.0/act_{AD_ACCOUNT_ID}/campaigns"
    params = {
        'access_token': ACCESS_TOKEN,
        'effective_status': '["ACTIVE"]',
        'fields': 'name,objective,status'
    }
    try:
        response = requests.get(url, params=params, verify=False)
        print("Respuesta de la API de Facebook:", response.json())
    except Exception as e:
        print(f"Error llamando a la API de Facebook: {e}")

if __name__ == "__main__":
    test_email()
    test_facebook_api()
