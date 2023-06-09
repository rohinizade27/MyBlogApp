from django.urls import path
from .views import RegisterView, GetTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', GetTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
