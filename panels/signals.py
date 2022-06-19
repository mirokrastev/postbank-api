from smtplib import SMTPRecipientsRefused, SMTPException

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail


from panels.models import EmployeeDiscountAction


def send_discount_email(email_title, email_content, user):
    try:
        send_mail(
            email_title,
            email_content,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
    except (SMTPException, SMTPRecipientsRefused):
        print('error')
        return


@receiver(post_save, sender=EmployeeDiscountAction)
def check_discount_status(instance, created, **kwargs):
    if not created:
        return

    trader = instance.discount.trader
    user = trader.user

    if EmployeeDiscountAction.objects.filter(discount=instance.discount, state=False).count() > 1:
        return

    if instance.state is False:
        instance.discount.status = 'Rejected'
        instance.discount.save()
        if trader.notifications_status:
            send_discount_email('Your discount offer was rejected',
                                'Bank employee(s) has rejected your discount.',
                                user)
        return

    if EmployeeDiscountAction.objects.filter(discount=instance.discount, state=True).count() == 2:
        instance.discount.status = 'Active'
        instance.discount.save()
        if trader.notifications_status:
            send_discount_email('Your discount offer was accepted',
                                'Bank employees has accepted your discount.',
                                user)
        return
