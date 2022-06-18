from datetime import date, timedelta
from smtplib import SMTPRecipientsRefused
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

from accounts.models import Client
from panels.models import Discount


@shared_task(name='send_offers_notif')
def send_offers_notif():
    print('sending notifications')
    all_cardholders = Client.objects.filter(notifications_status=True)
    all_accepted_offers = Discount.objects.filter(status='Active', is_processed=False)

    if not all_accepted_offers:
        return

    for cardholder in all_cardholders:
        msgs = []

        for offer in all_accepted_offers:
            trader = offer.trader.user.username
            discount_percent = offer.discount_percent
            active_until = offer.end_date

            msgs.append(f'{discount_percent}% discount from {trader} active until {active_until}')

        msg_joined = '\n'.join(msgs)

        try:
            send_mail(
                'New discount offers from postbank traders',
                msg_joined,
                settings.EMAIL_HOST_USER,
                [cardholder.user.email,]
            )
        except SMTPRecipientsRefused:
            break

    for i in all_accepted_offers:
        i.is_processed = True
        i.save()


@shared_task(name='mark_expired_offers')
def mark_expired_offers():
    print('marking expired offers')
    current_date = date.today() - timedelta(days=1)
    Discount.objects.filter(Q(end_date__lte=current_date) & ~Q(status='Expired')).update(status='Expired')
