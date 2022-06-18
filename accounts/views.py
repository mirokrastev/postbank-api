from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from accounts import models
from accounts import serializers


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'type': user.type})


class RegisterViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = ()

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'user_id': user.id, 'token': token.key, 'type': user.type}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        self.request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
