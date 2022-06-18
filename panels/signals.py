from django.db.models.signals import post_save
from django.dispatch import receiver

from panels.models import EmployeeDiscountAction


@receiver(post_save, sender=EmployeeDiscountAction)
def check_discount_status(instance, created, **kwargs):
    if not created:
        return

    if instance.state is False:
        instance.discount.status = 'Rejected'
        instance.discount.save()
        return

    if EmployeeDiscountAction.objects.filter(discount=instance.discount).values_list('state').count() >= 2:
        instance.discount.status = 'Active'
        instance.discount.save()
        return
