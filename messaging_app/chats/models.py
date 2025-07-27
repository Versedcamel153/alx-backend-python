from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

class User(AbstractUser):
    class Role(models.TextChoices):
        GUEST = 'guest', _('Guest')
        HOST = 'host', _('Host')
        ADMIN = 'admin', _('Admin')

    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=15, null=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'  # Or 'email' if you want email login

    def __str__(self):
        return self.username
    
    @property
    def id(self):
        return self.user_id

class Message(models.Model):
    message_id = models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    conversation_id = models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)