from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, User
from .filter import MessageFilter
from django_filters import rest_framework as filters
from .permissions import IsParticipantOfConversation
from .serializers import (
    ConversationSerializer,
    MessageSerializer, UserSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):  # Only GET methods
    queryset = User.objects.all()
    serializer_class = UserSerializer



class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filterset_fields = ['participants'] 
    
    def create(self, request, *args, **kwargs):
        # Expecting: list of participant user_ids in POST data
        user_ids = request.data.get("participants", [])
        if not user_ids or not isinstance(user_ids, list):
            return Response({"error": "participants must be a list of user_ids"}, status=400)

        # Create conversation
        conversation = Conversation.objects.create()
        participants = User.objects.filter(user_id__in=user_ids)
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_fields = ['conversation']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MessageFilter

    def create(self, request, *args, **kwargs):
        # Expecting: sender_id, conversation_id, message_body
        sender_id = request.data.get("sender_id")
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")

        if not sender_id or not conversation_id or not message_body:
            return Response(
                {"error": "sender_id, conversation_id, and message_body are required"},
                status=400
            )

        try:
            sender = User.objects.get(user_id=sender_id)
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except (User.DoesNotExist, Conversation.DoesNotExist):
            return Response({"error": "Invalid sender_id or conversation_id"}, status=404)

        message = Message.objects.create(
            sender_id=sender,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
