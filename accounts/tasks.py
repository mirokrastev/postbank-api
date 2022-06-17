import requests

from celery import shared_task
from decouple import config

from accounts import serializers


API_KEY = config('CONST_TOKEN')
headers = {'API-KEY': API_KEY}
base_url = 'http://localhost:8081/api/'


@shared_task(name='sync_traders')
def sync_traders():
    response = requests.get(f'{base_url}/users/traders', headers=headers)
    data = response.json()

    serializer = serializers.TraderSerializer(data, many=True)


@shared_task(name='sync_bank_employees')
def sync_bank_employees():
    response = requests.get(f'{base_url}/users/bank-employees', headers=headers)
    data = response.json()


@shared_task(name='sync_terminals')
def sync_terminals():
    response = requests.get(f'{base_url}/pos-terminals', headers=headers)
    data = response.json()
