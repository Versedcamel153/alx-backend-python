# messaging_app/chats/urls.py
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Register base routes with DefaultRouter
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')  # Optional: allow top-level access

# Register nested routes
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Combine both sets of routes
urlpatterns = router.urls + nested_router.urls