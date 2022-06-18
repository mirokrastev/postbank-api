from celery import shared_task
from decouple import config
from django.conf import settings
from django.core.mail import send_mail

from accounts.models import Client
from panels.models import Discount


@shared_task(name='send_offers_notif')
def sync_db():
    all_cardholders = Client.objects.filter(notifications_status=True)
    all_accepted_offers = Discount.objects.filter(status='Active', is_processed=False)

    for cardholder in all_cardholders:
        for offer in all_accepted_offers:
            trader = offer.trader.user.username
            discount_percent = offer.discount_percent
            active_until = offer.end_date

            send_mail(
                f'New discount offer from {trader}',
                f'{discount_percent} active until {active_until}',
                settings.EMAIL_HOST_USER,
                [cardholder.user.email,]

            )
