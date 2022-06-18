from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
from creditcards.models import CardExpiryField

from accounts.utils import CustomCardNumberField
from base.models import BaseModel


class User(BaseModel, AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Trader(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    phone_number = PhoneNumberField()

    def __str__(self):
        return f'Trader<{self.user.username}>'


class BankEmployee(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)

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

    def __str__(self):
        return f'Client<{self.user.username}>'
