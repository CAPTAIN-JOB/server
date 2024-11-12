import requests
from requests.auth import HTTPBasicAuth
from flask import current_app

def get_access_token():
    consumer_key = current_app.config['CONSUMER_KEY']
    consumer_secret = current_app.config['CONSUMER_SECRET']
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return response.json().get("access_token")

def lipa_na_mpesa_online(amount, phone_number):
    access_token = get_access_token()
    # Use access token to make STK push request
    pass
