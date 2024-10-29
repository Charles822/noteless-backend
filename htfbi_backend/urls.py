"""
URL configuration for htfbi_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework_nested import routers
from lists.views import ListViewSet
from notes.views import NoteViewSet
from users.views import UserViewSet, MyTokenObtainPairView
from interactions.views import CommentViewSet, VoteViewSet
from rest_framework_simplejwt.views import TokenRefreshView

# Main router for lists
lists_router = routers.DefaultRouter()
lists_router.register('lists', ListViewSet, basename='lists')

# Main router for users
users_router = routers.DefaultRouter()
users_router.register('users', UserViewSet, basename='users')

# Nested router for notes
notes_router = routers.NestedDefaultRouter(lists_router, 'lists', lookup='list')
notes_router.register('notes', NoteViewSet, basename='list-notes')

# Nested List router for users 
user_lists_router = routers.NestedDefaultRouter(users_router, 'users', lookup='user')
user_lists_router.register('lists', ListViewSet, basename='user-lists')

# Nested router for comments under notes
comments_router = routers.NestedDefaultRouter(notes_router, 'notes', lookup='note')
comments_router.register('comments', CommentViewSet, basename='note-comments')

# Nested router for votes under notes
votes_router = routers.NestedDefaultRouter(notes_router, 'notes', lookup='note')
votes_router.register('votes', VoteViewSet, basename='note-votes')



urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/stripe/', include('payments.urls')),
    path('admin/', admin.site.urls),
    path('ai_agent/', include('ai_agent.urls')),
    path('contents/', include('contents.urls')),
    path('interactions/', include('interactions.urls')),
    path('lists/', include('lists.urls')),
    path('notes/', include('notes.urls')),
    path('users/', include('users.urls')),
    # Nested URLs
    path('lists/', include(notes_router.urls)),
    path('lists/', include(comments_router.urls)),
    path('lists/', include(votes_router.urls)),
    path('users/', include(user_lists_router.urls)),
    

] + debug_toolbar_urls()