from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListViewSet

router = DefaultRouter()
router.register('lists', ListViewSet, basename='lists')


urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
]