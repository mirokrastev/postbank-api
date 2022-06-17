from creditcards.utils import get_digits
from django.core.validators import MinLengthValidator

from creditcards.models import CardNumberField
from creditcards.validators import CCNumberValidator


class CustomCCNumberValidator(CCNumberValidator):
    def __call__(self, value):
        """
        Do not validate with Luhn's algorithm
        """
        digits = get_digits(value)
        return digits


# todo check if MaxLength is necessary
class CustomCardNumberField(CardNumberField):
    default_validators = [
        MinLengthValidator(13),
        CustomCCNumberValidator(),
    ]
