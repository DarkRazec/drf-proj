from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from materials.urls import router
from users.apps import UsersConfig
from users.views import UserViewSet, PaymentViewSet

app_name = UsersConfig.name

router.register(r'users', UserViewSet, basename='users')
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
                  path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + router.urls
