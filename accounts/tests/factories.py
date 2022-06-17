from rest_framework.authtoken.models import Token

from accounts import models


def create_user(username='testuser',
                email='testemail@example.com',
                password='secretPassword123',
                create_token=True,
                **kwargs):

    user = models.User.objects.create_user(username=username, email=email, password=password, **kwargs)

    if create_token:
        Token.objects.get_or_create(user=user)

    return user
