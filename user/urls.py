from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import CreateUserView, ManageUserView, CustomTokenObtainPairView

urlpatterns = [
	path("register/", CreateUserView.as_view(), name="register"),
	path("me/", ManageUserView.as_view(), name="manage"),
	path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
	path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

app_name = "user"
