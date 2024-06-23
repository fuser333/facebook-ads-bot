import requests
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

# Variables
app_id = '823040352757676'
app_secret = 'db46c9d90dfa967520a0fd7dcd15d5f6'
short_lived_token = 'EAALsjQPcp6wBO6UzrACTQZCeCEtbbbkdcoryK5dmY1T6ljW6gEKcWSZCgAjx1ZBqrlnkPBUw3cdkOV3H3fZAHDXOXVkoy0yObH8ZAs8Vue6BNXgstHmuZCOCvBCPxYL8mnvR4tX5jLkuKeYr50tdYqv6muYvmito50DRwRhfEEXnvhiHVW0XHCZCSRORYPdpIe65lSQqh4Kn1T1CYrLCZCNA3VU5Os4ZD'

# URL para obtener el token de acceso a largo plazo
url = 'https://graph.facebook.com/v13.0/oauth/access_token'
params = {
    'grant_type': 'fb_exchange_token',
    'client_id': app_id,
    'client_secret': app_secret,
    'fb_exchange_token': short_lived_token
}

# Solicitud HTTP
response = requests.get(url, params=params)
if response.status_code == 200:
    long_lived_token = response.json().get('access_token')
    print('Token de Acceso a Largo Plazo:', long_lived_token)
else:
    print('Error:', response.json())

