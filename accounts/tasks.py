import requests
import json

from celery import shared_task
from decouple import config
from django.db import DatabaseError

from accounts import models

API_KEY = config('CONST_TOKEN')
headers = {'API-KEY': API_KEY}
base_url = config('BASE_URL')


def get_or_create(model, data):
    created = False
    try:
        instance = model.objects.get(**data)
    except model.DoesNotExist:
        try:
            instance = model.objects.create(**data)
            created = True
        except DatabaseError:
            return False, False
    return instance, created


@shared_task(name='sync_traders')
def sync_traders():
    response = requests.get(f'{base_url}/users/traders', headers=headers)
    data = json.loads(response.text)

    for piece in data:
        user_data = piece['user']
        user, created_user = get_or_create(models.User, user_data)

        if user is False:
            continue

        trader_id = piece['id']
        additional_info = piece['additional_info']
        trader, created_trader = get_or_create(models.Trader, {'id': trader_id, 'user': user, **additional_info})

        if trader is False:
            # Delete newly created user. Simulates atomic request
            if created_user:
                user.delete()
    print('Traders Sync is complete!')


@shared_task(name='sync_bank_employees')
def sync_bank_employees():
    response = requests.get(f'{base_url}/users/bank-employees', headers=headers)
    data = json.loads(response.text)

    for piece in data:
        user_data = piece['user']
        user, created_user = get_or_create(models.User, user_data)

        if user is False:
            continue

        employee_id = piece['id']
        employee, created_employee = get_or_create(models.BankEmployee, {'id': employee_id, 'user': user})

        if employee is False:
            if created_user:
                user.delete()
    print('Bank Employees Sync is complete!')


@shared_task(name='sync_terminals')
def sync_terminals():
    response = requests.get(f'{base_url}/pos-terminals', headers=headers)
    data = json.loads(response.text)

    for piece in data:
        user_data = piece['trader']['user']
        user, created_user = get_or_create(models.User, user_data)

        if user is False:
            continue

        trader_id = piece['trader']['id']
        additional_info = piece['trader']['additional_info']
        trader, created_trader = get_or_create(models.Trader, {'id': trader_id, 'user': user, **additional_info})

        if trader is False:
            if created_user:
                user.delete()
            continue

        terminal_id = piece['id']
        terminal, created_terminal = get_or_create(models.POSTerminal, {'id': terminal_id, 'trader': trader})

        if terminal is False:
            if created_user:
                user.delete()
            if created_trader:
                trader.delete()
    print('POS Terminals Sync is complete!')
