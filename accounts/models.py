from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
from creditcards.models import CardExpiryField

from accounts.utils import CustomCardNumberField
from base.models import BaseModel


class User(BaseModel, AbstractUser):
    email = models.EmailField(unique=True)

    phone_number = PhoneNumberField()
    card_number = CustomCardNumberField()
    valid_thru = CardExpiryField()

    REQUIRED_FIELDS = ['email', 'phone_number', 'card_number', 'valid_thru']

    def __str__(self):
        return self.username
