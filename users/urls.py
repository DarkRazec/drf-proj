from materials.urls import router
from users.apps import UsersConfig
from users.views import UserViewSet

app_name = UsersConfig.name

router.register(r'users', UserViewSet, basename='users')

urlpatterns = router.urls
