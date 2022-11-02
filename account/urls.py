from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from account.views import (
    PmsUserRegisterViewSet,PmsTokenObtainPairView,
    ChangePasswordView, ForgetPasswordView, ResetPasswordView,
    PmsUserProfileViewSet)

router = routers.DefaultRouter()
router.register(r"users", PmsUserRegisterViewSet, basename="User-Register")
router.register(r"profile", PmsUserProfileViewSet, basename="User-Profile")

urlpatterns = [
    path("users/login/", PmsTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/activate-account/<str:uid>/<str:token>/", PmsUserRegisterViewSet.as_view({"post": "activate"})),
    path("users/token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/logout/", TokenBlacklistView.as_view(), name="logout_blacklist_token"),
    path("users/changepassword/<int:pk>/", ChangePasswordView.as_view(), name="change-password" ),
    path("users/forgetpassword/", ForgetPasswordView.as_view(), name="forget-password" ),
    path("users/reset-forgetpassword/<uid>/<token>/", ResetPasswordView.as_view(), name="reset-forget-password" ),
]

urlpatterns = urlpatterns + router.urls
