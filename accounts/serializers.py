from datetime import datetime

from creditcards.utils import get_digits, expiry_date
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from accounts import models
from accounts import utils


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'email', 'type')


class CardNumberField(serializers.CharField):
    def to_representation(self, value):
        raw_digits = get_digits(value)
        digits_array = [raw_digits[0:4], raw_digits[4:8], raw_digits[8:12], raw_digits[12:16]]
        return "-".join(digits_array)

    def to_internal_value(self, data):
        validated_digits = utils.CustomCCNumberValidator()(data)
        return validated_digits


class ValidThruField(serializers.DateField):
    field_format = '%m/%y'

    def to_representation(self, value):
        return value.strftime(self.field_format)

    def to_internal_value(self, value):
        try:
            parsed_value = datetime.strptime(value, self.field_format)
            date = expiry_date(parsed_value.year, parsed_value.month)
        except ValueError:
            raise serializers.ValidationError('Invalid date format.')

        if date < datetime.now().date():
            raise serializers.ValidationError('Invalid date.')
        return value


class TraderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    phone_number = PhoneNumberField()

    class Meta:
        model = models.Trader
        fields = ('id', 'user', 'phone_number')


class BankEmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.BankEmployee
        fields = ('id', 'user')


class TerminalSerializer(serializers.ModelSerializer):
    trader = TraderSerializer()

    class Meta:
        model = models.POSTerminal
        fields = ('id', 'trader')


class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False, style={'input_type': 'password'})

    phone_number = PhoneNumberField(source='client.phone_number')
    card_number = CardNumberField(min_length=13, max_length=16, source='client.card_number')
    valid_thru = ValidThruField(source='client.valid_thru')
    notifications_status = serializers.BooleanField(source='client.notifications_status')

    def validate_password(self, value):
        if not validate_password(value):
            return value

    def create(self, validated_data):
        user_data = {'email': validated_data.pop('email'),
                     'username': validated_data.pop('username'),
                     'password': validated_data.pop('password')}
        user = models.User.objects.create_user(**user_data)
        models.Client.objects.create(user=user, **validated_data['client'])
        return user

    class Meta:
        model = models.User
        fields = ('id', 'username', 'password', 'type', 'email', 'phone_number',
                  'card_number', 'valid_thru', 'notifications_status')
