from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_display', read_only=True)  # ✅ Using serializers.CharField with display

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.UUIDField()
    conversation_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender_id',
            'conversation_id',
            'message_body',
            'sent_at'
        ]

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  # ✅ Custom nested messages logic

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'created_at'
        ]

    def get_messages(self, obj):
        from .models import Message
        messages = Message.objects.filter(conversation=obj).order_by('sent_at')
        return MessageSerializer(messages, many=True).data
