from rest_framework.routers import DefaultRouter
from . views import UserViewSet, ProfileViewSet, CustomerViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('profile', ProfileViewSet, basename='profile')
router.register('customer', CustomerViewSet, basename='customer')

urlpatterns = router.urls