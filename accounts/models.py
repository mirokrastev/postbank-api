from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
from creditcards.models import CardExpiryField

from accounts.utils import CustomCardNumberField
from base.models import BaseModel


class User(BaseModel, AbstractUser):
    USER_TYPES = (
        ('TRADER', 'Trader'),
        ('BANK_EMPLOYEE', 'Bank Employee'),
        ('CLIENT', 'Client')
    )
    email = models.EmailField(unique=True)
    type = models.CharField(choices=USER_TYPES, max_length=50, blank=True, null=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Trader(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    phone_number = PhoneNumberField()
    notifications_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.user:
            self.user.type = 'TRADER'
            self.user.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Trader<{self.user.username}>'


class BankEmployee(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        if self.user:
            self.user.type = 'BANK_EMPLOYEE'
            self.user.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Bank Employee<{self.user.username}>'


class POSTerminal(BaseModel):
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE, related_name='pos_terminals')

    def __str__(self):
        return f'{self.id} - {self.trader.user.username}'


class Client(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)

    phone_number = PhoneNumberField()
    card_number = CustomCardNumberField()
    valid_thru = CardExpiryField()
    notifications_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.user:
            self.user.type = 'CLIENT'
            self.user.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Client<{self.user.username}>'
