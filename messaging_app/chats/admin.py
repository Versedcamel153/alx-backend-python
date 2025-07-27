from django.contrib import admin
from .models import User, Message, Conversation

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('role',)
    ordering = ('-created_at',)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender_id', 'conversation', 'sent_at')
    search_fields = ('sender_id__username', 'conversation__conversation_id')
    list_filter = ('sent_at',)
    ordering = ('-sent_at',)
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at')
    search_fields = ('conversation_id',)
    filter_horizontal = ('participants',)
    ordering = ('-created_at',)
    