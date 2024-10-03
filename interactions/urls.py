from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, VoteViewSet

router = DefaultRouter()
router.register('comments', CommentViewSet, basename='comments')
router.register('votes', VoteViewSet, basename='votes')

urlpatterns = router.urls