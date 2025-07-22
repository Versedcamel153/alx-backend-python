# messaging_app/chats/urls.py
from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = NestedDefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

# Nested route for messages under conversations
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = router.urls + conversations_router.urls