from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows only participants of a conversation to interact with its messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "PUT", "PATCH", "DELETE", "POST"]:
            return request.user in obj.conversation.participants.all()
        return False
