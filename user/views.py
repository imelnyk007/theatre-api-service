from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.cache import cache
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from user.serializers import UserSerializer
from user.throttling import LoginFailRateThrottle


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    LOGIN_FAILURES_TIME = 180  # seconds
    throttle_classes = [LoginFailRateThrottle, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        email = request.POST["email"]
        cache_key = f"login_fail_{email}"

        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            login_failures = cache.get(cache_key, 0)
            login_failures += 1
            cache.set(cache_key, login_failures, self.LOGIN_FAILURES_TIME)
            raise e

        cache.delete(cache_key)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
