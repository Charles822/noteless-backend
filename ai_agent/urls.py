from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('agents', views.AgentRoleViewSet)
router.register('agent_responses', views.AgentResponseViewSet)


urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
]