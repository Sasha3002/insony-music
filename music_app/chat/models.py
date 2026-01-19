from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Group

User = get_user_model()

class Conversation(models.Model):
    TYPE_CHOICES = [
        ('direct', 'Direct Message'),
        ('group', 'Group Chat'), 
    ]
    
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='direct')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group_name = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        if self.type == 'direct':
            participants = list(self.participants.all())
            if len(participants) == 2:
                return f"Chat: {participants[0].user.username} ↔ {participants[1].user.username}"
        return f"Conversation {self.id}"
    
    @property
    def last_message(self):
        return self.messages.last()
    
    def get_other_participant(self, user):
        if self.type == 'direct':
            participants = self.participants.exclude(user=user)
            return participants.first().user if participants.exists() else None
        return None


class ChatParticipant(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('conversation', 'user')
    
    def __str__(self):
        return f"{self.user.username} in {self.conversation}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}..."
    
    @property
    def is_read_by_others(self):
        participants = self.conversation.participants.exclude(user=self.sender)
        for participant in participants:
            if not participant.last_read_at or participant.last_read_at < self.created_at:
                return False
        return True


class MessageRead(models.Model):
    message = models.ForeignKey(Message, related_name='reads', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('message', 'user')


class GroupChatMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.username} in {self.group.name}: {self.content[:50]}..."


class GroupChatRead(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='chat_reads')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_read_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('group', 'user')
    
    def __str__(self):
        return f"{self.user.username} read {self.group.name} at {self.last_read_at}"