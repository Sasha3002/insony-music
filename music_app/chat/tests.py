from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import json

from chat.models import (
    Conversation, ChatParticipant, Message, MessageRead,
    GroupChatMessage, GroupChatRead
)
from groups.models import Group, GroupMembership

User = get_user_model()


class ConversationModelTest(TestCase):
    def setUp(self):
        """Set up test users"""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
    
    def test_create_direct_conversation(self):
        conversation = Conversation.objects.create(type='direct')
        self.assertEqual(conversation.type, 'direct')
        self.assertIsNotNone(conversation.created_at)
        self.assertIsNotNone(conversation.updated_at)
    
    def test_conversation_str_method(self):
        conversation = Conversation.objects.create(type='direct')
        ChatParticipant.objects.create(conversation=conversation, user=self.user1)
        ChatParticipant.objects.create(conversation=conversation, user=self.user2)
        
        expected_str = f"Chat: {self.user1.username} ↔ {self.user2.username}"
        self.assertEqual(str(conversation), expected_str)
    
    def test_last_message_property(self):
        conversation = Conversation.objects.create(type='direct')
        ChatParticipant.objects.create(conversation=conversation, user=self.user1)

        message1 = Message.objects.create(
            conversation=conversation,
            sender=self.user1,
            content="First message"
        )
    
        message1.created_at = timezone.now() - timedelta(seconds=1)
        message1.save()

        message2 = Message.objects.create(
            conversation=conversation,
            sender=self.user1,
            content="Second message"
        )

        last_msg = conversation.last_message
        self.assertIsNotNone(last_msg)
        self.assertEqual(last_msg.content, "Second message")
    
    def test_get_other_participant(self):
        conversation = Conversation.objects.create(type='direct')
        ChatParticipant.objects.create(conversation=conversation, user=self.user1)
        ChatParticipant.objects.create(conversation=conversation, user=self.user2)
        
        other = conversation.get_other_participant(self.user1)
        self.assertEqual(other, self.user2)
        
        other = conversation.get_other_participant(self.user2)
        self.assertEqual(other, self.user1)
    
    def test_conversation_ordering(self):
        conv1 = Conversation.objects.create(type='direct')
        conv2 = Conversation.objects.create(type='direct')
        
        conv1.updated_at = timezone.now()
        conv1.save()
        
        conversations = Conversation.objects.all()
        self.assertEqual(conversations[0], conv1)
        self.assertEqual(conversations[1], conv2)


class MessageModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        self.conversation = Conversation.objects.create(type='direct')
        ChatParticipant.objects.create(conversation=self.conversation, user=self.user1)
        ChatParticipant.objects.create(conversation=self.conversation, user=self.user2)
    
    def test_create_message(self):
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content="Hello, this is a test message"
        )
        
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.content, "Hello, this is a test message")
        self.assertFalse(message.is_edited)
        self.assertIsNone(message.edited_at)
    
    def test_message_str_method(self):
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content="This is a long message that should be truncated in the string representation"
        )
        
        str_representation = str(message)
        self.assertTrue(str_representation.startswith(f"{self.user1.username}: This is a long message"))
        self.assertTrue(str_representation.endswith("..."))
    
    def test_message_ordering(self):
        message1 = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content="First message"
        )
        message2 = Message.objects.create(
            conversation=self.conversation,
            sender=self.user2,
            content="Second message"
        )
        
        messages = Message.objects.all()
        self.assertEqual(messages[0], message1)
        self.assertEqual(messages[1], message2)
    
    def test_is_read_by_others_property(self):
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content="Test message"
        )
        
        self.assertFalse(message.is_read_by_others)
        participant2 = self.conversation.participants.get(user=self.user2)
        participant2.last_read_at = timezone.now()
        participant2.save()
        message.refresh_from_db()
        self.assertTrue(message.is_read_by_others)


class ChatParticipantModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.conversation = Conversation.objects.create(type='direct')
    
    def test_create_participant(self):
        participant = ChatParticipant.objects.create(
            conversation=self.conversation,
            user=self.user
        )
        
        self.assertEqual(participant.user, self.user)
        self.assertEqual(participant.conversation, self.conversation)
        self.assertIsNotNone(participant.joined_at)
        self.assertIsNone(participant.last_read_at)
    
    def test_unique_together_constraint(self):
        ChatParticipant.objects.create(
            conversation=self.conversation,
            user=self.user
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            ChatParticipant.objects.create(
                conversation=self.conversation,
                user=self.user
            )


class GroupChatMessageModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test description',
            admin=self.user
        )
    
    def test_create_group_message(self):
        message = GroupChatMessage.objects.create(
            group=self.group,
            sender=self.user,
            content="Hello group!"
        )
        
        self.assertEqual(message.group, self.group)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.content, "Hello group!")
        self.assertFalse(message.is_edited)
    
    def test_group_message_ordering(self):
        message1 = GroupChatMessage.objects.create(
            group=self.group,
            sender=self.user,
            content="First"
        )
        message2 = GroupChatMessage.objects.create(
            group=self.group,
            sender=self.user,
            content="Second"
        )
        
        messages = GroupChatMessage.objects.all()
        self.assertEqual(messages[0], message1)
        self.assertEqual(messages[1], message2)


class ChatListViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        
        self.conversation = Conversation.objects.create(type='direct')
        ChatParticipant.objects.create(conversation=self.conversation, user=self.user1)
        ChatParticipant.objects.create(conversation=self.conversation, user=self.user2)
        
        Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content="Test message"
        )
    
    def test_chat_list_requires_login(self):
        response = self.client.get(reverse('chat_list'))
        self.assertEqual(response.status_code, 302)  
        self.assertIn('/users/login/', response.url)
    
    def test_chat_list_shows_conversations(self):
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('chat_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat_list.html')
        self.assertIn('conversations', response.context)
        self.assertEqual(len(response.context['conversations']), 1)
    
    def test_chat_list_empty_conversations_not_shown(self):
        empty_conv = Conversation.objects.create(type='direct')
        ChatParticipant.objects.create(conversation=empty_conv, user=self.user1)
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('chat_list'))
        self.assertEqual(len(response.context['conversations']), 1)
    
    def test_chat_list_unread_count(self):
        Message.objects.create(
            conversation=self.conversation,
            sender=self.user2,
            content="Unread message"
        )
        
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('chat_list')) 
        conversation = response.context['conversations'][0]
        self.assertGreater(conversation.unread_count, 0)


class ConversationDetailViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@test.com',
            password='testpass123'
        )
        
        self.conversation = Conversation.objects.create(type='direct')
        ChatParticipant.objects.create(conversation=self.conversation, user=self.user1)
        ChatParticipant.objects.create(conversation=self.conversation, user=self.user2)
        
        Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content="Test message"
        )
    
    def test_conversation_detail_requires_login(self):
        url = reverse('conversation_detail', kwargs={'conversation_id': self.conversation.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_conversation_detail_access_denied_for_non_participant(self):
        self.client.login(username='user3', password='testpass123')
        url = reverse('conversation_detail', kwargs={'conversation_id': self.conversation.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(response.url.endswith('/chat/') or 'chat_list' in response.url)
    
    def test_conversation_detail_marks_as_read(self):
        self.client.login(username='user1', password='testpass123')
        
        participant = ChatParticipant.objects.get(
            conversation=self.conversation,
            user=self.user1
        )
        self.assertIsNone(participant.last_read_at)
        url = reverse('conversation_detail', kwargs={'conversation_id': self.conversation.id})
        response = self.client.get(url)
        participant.refresh_from_db()
        self.assertIsNotNone(participant.last_read_at)
    
    def test_conversation_detail_shows_messages(self):
        self.client.login(username='user1', password='testpass123')
        url = reverse('conversation_detail', kwargs={'conversation_id': self.conversation.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/conversation_detail.html')
        self.assertIn('messages', response.context)
        self.assertEqual(len(response.context['messages']), 1)


class StartConversationViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
    
    def test_start_conversation_requires_login(self):
        url = reverse('start_conversation', kwargs={'username': 'user2'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_start_new_conversation(self):
        self.client.login(username='user1', password='testpass123')
        url = reverse('start_conversation', kwargs={'username': 'user2'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('conversation', response.url)
        self.assertEqual(Conversation.objects.count(), 1)
        conversation = Conversation.objects.first()
        self.assertEqual(conversation.participants.count(), 2)
    
    def test_start_conversation_redirects_to_existing(self):
        conversation = Conversation.objects.create(type='direct')
        ChatParticipant.objects.create(conversation=conversation, user=self.user1)
        ChatParticipant.objects.create(conversation=conversation, user=self.user2)
        self.client.login(username='user1', password='testpass123')
        url = reverse('start_conversation', kwargs={'username': 'user2'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(conversation.id), response.url)
        self.assertEqual(Conversation.objects.count(), 1)
    
    def test_cannot_start_conversation_with_self(self):
        self.client.login(username='user1', password='testpass123')
        url = reverse('start_conversation', kwargs={'username': 'user1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Conversation.objects.count(), 0)


class SendMessageViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        
        self.conversation = Conversation.objects.create(type='direct')
        ChatParticipant.objects.create(conversation=self.conversation, user=self.user1)
        ChatParticipant.objects.create(conversation=self.conversation, user=self.user2)
    
    def test_send_message_requires_post(self):
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('send_message'))
        self.assertEqual(response.status_code, 405)  
    
    def test_send_message_success(self):
        self.client.login(username='user1', password='testpass123')
        response = self.client.post(reverse('send_message'), {
            'conversation_id': self.conversation.id,
            'content': 'Hello, this is a test message!'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['ok'])
        self.assertIn('message', data)
        self.assertEqual(data['message']['content'], 'Hello, this is a test message!')
        self.assertEqual(Message.objects.count(), 1)
        message = Message.objects.first()
        self.assertEqual(message.content, 'Hello, this is a test message!')
    
    def test_send_empty_message_fails(self):
        self.client.login(username='user1', password='testpass123')
        response = self.client.post(reverse('send_message'), {
            'conversation_id': self.conversation.id,
            'content': '   '  
        })
        
        data = json.loads(response.content)
        self.assertFalse(data['ok'])
        self.assertEqual(Message.objects.count(), 0)
    
    def test_send_message_non_participant_fails(self):
        user3 = User.objects.create_user(
            username='user3',
            email='user3@test.com',
            password='testpass123'
        )
        
        self.client.login(username='user3', password='testpass123')
        response = self.client.post(reverse('send_message'), {
            'conversation_id': self.conversation.id,
            'content': 'Unauthorized message'
        })
        
        data = json.loads(response.content)
        self.assertFalse(data['ok'])
        self.assertEqual(Message.objects.count(), 0)
    
    def test_send_message_updates_conversation_timestamp(self):
        old_timestamp = self.conversation.updated_at
        
        self.client.login(username='user1', password='testpass123')
        self.client.post(reverse('send_message'), {
            'conversation_id': self.conversation.id,
            'content': 'Test message'
        })
        
        self.conversation.refresh_from_db()
        self.assertGreater(self.conversation.updated_at, old_timestamp)


class GetNewMessagesViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        
        self.conversation = Conversation.objects.create(type='direct')
        ChatParticipant.objects.create(conversation=self.conversation, user=self.user1)
        ChatParticipant.objects.create(conversation=self.conversation, user=self.user2)
        
        self.message1 = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content="Message 1"
        )
    
    def test_get_new_messages_success(self):
        message2 = Message.objects.create(
            conversation=self.conversation,
            sender=self.user2,
            content="Message 2"
        )
        
        self.client.login(username='user1', password='testpass123')
        url = reverse('get_new_messages', kwargs={'conversation_id': self.conversation.id})
        response = self.client.get(url, {'last_message_id': self.message1.id})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['ok'])
        self.assertEqual(len(data['messages']), 1)
        self.assertEqual(data['messages'][0]['content'], 'Message 2')
    
    def test_get_new_messages_excludes_own_messages(self):
        message2 = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content="My own message"
        )
        
        self.client.login(username='user1', password='testpass123')
        url = reverse('get_new_messages', kwargs={'conversation_id': self.conversation.id})
        response = self.client.get(url, {'last_message_id': self.message1.id})
        data = json.loads(response.content)
        self.assertEqual(len(data['messages']), 0)
    
    def test_get_new_messages_non_participant_denied(self):
        user3 = User.objects.create_user(
            username='user3',
            email='user3@test.com',
            password='testpass123'
        )
        
        self.client.login(username='user3', password='testpass123')
        url = reverse('get_new_messages', kwargs={'conversation_id': self.conversation.id})
        response = self.client.get(url, {'last_message_id': 0})
        
        data = json.loads(response.content)
        self.assertFalse(data['ok'])


class GroupChatViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@test.com',
            password='testpass123'
        )
        self.non_member = User.objects.create_user(
            username='nonmember',
            email='nonmember@test.com',
            password='testpass123'
        )
        
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test description',
            admin=self.admin
        )
        
        GroupMembership.objects.create(
            group=self.group,
            user=self.admin,
            status='accepted'
        )
        GroupMembership.objects.create(
            group=self.group,
            user=self.member,
            status='accepted'
        )
    
    def test_group_chat_requires_login(self):
        url = reverse('group_chat', kwargs={'group_slug': self.group.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_group_chat_member_access(self):
        self.client.login(username='member', password='testpass123')
        url = reverse('group_chat', kwargs={'group_slug': self.group.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/group_chat.html')
    
    def test_group_chat_non_member_denied(self):
        self.client.login(username='nonmember', password='testpass123')
        url = reverse('group_chat', kwargs={'group_slug': self.group.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_group_chat_marks_as_read(self):
        self.client.login(username='member', password='testpass123')
        url = reverse('group_chat', kwargs={'group_slug': self.group.slug})
        response = self.client.get(url)
        
        self.assertTrue(
            GroupChatRead.objects.filter(
                group=self.group,
                user=self.member
            ).exists()
        )


class SendGroupMessageViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@test.com',
            password='testpass123'
        )
        
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test description',
            admin=self.admin
        )
        
        GroupMembership.objects.create(
            group=self.group,
            user=self.admin,
            status='accepted'
        )
        GroupMembership.objects.create(
            group=self.group,
            user=self.member,
            status='accepted'
        )
    
    def test_send_group_message_success(self):
        self.client.login(username='member', password='testpass123')
        response = self.client.post(reverse('send_group_message'), {
            'group_id': self.group.id,
            'content': 'Hello group!'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['ok'])
        self.assertEqual(data['message']['content'], 'Hello group!')
        
        self.assertEqual(GroupChatMessage.objects.count(), 1)
    
    def test_send_group_message_non_member_denied(self):
        non_member = User.objects.create_user(
            username='nonmember',
            email='nonmember@test.com',
            password='testpass123'
        )
        
        self.client.login(username='nonmember', password='testpass123')
        response = self.client.post(reverse('send_group_message'), {
            'group_id': self.group.id,
            'content': 'Unauthorized message'
        })
        
        data = json.loads(response.content)
        self.assertFalse(data['ok'])
        self.assertEqual(GroupChatMessage.objects.count(), 0)


class DeleteGroupMessageViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.member = User.objects.create_user(
            username='member',
            email='member@test.com',
            password='testpass123'
        )
        
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test description',
            admin=self.admin
        )
        
        GroupMembership.objects.create(
            group=self.group,
            user=self.admin,
            status='accepted'
        )
        GroupMembership.objects.create(
            group=self.group,
            user=self.member,
            status='accepted'
        )
        
        self.message = GroupChatMessage.objects.create(
            group=self.group,
            sender=self.member,
            content='Test message'
        )
    
    def test_delete_own_message(self):
        self.client.login(username='member', password='testpass123')
        url = reverse('delete_group_message', kwargs={'message_id': self.message.id})
        response = self.client.post(url)
        data = json.loads(response.content)
        self.assertTrue(data['ok'])
        self.assertEqual(GroupChatMessage.objects.count(), 0)
    
    def test_admin_can_delete_any_message(self):
        self.client.login(username='admin', password='testpass123')
        url = reverse('delete_group_message', kwargs={'message_id': self.message.id})
        response = self.client.post(url)
        
        data = json.loads(response.content)
        self.assertTrue(data['ok'])
        self.assertEqual(GroupChatMessage.objects.count(), 0)
    
    def test_cannot_delete_others_message(self):
        other_member = User.objects.create_user(
            username='other',
            email='other@test.com',
            password='testpass123'
        )
        GroupMembership.objects.create(
            group=self.group,
            user=other_member,
            status='accepted'
        )
        
        self.client.login(username='other', password='testpass123')
        url = reverse('delete_group_message', kwargs={'message_id': self.message.id})
        response = self.client.post(url)
        
        data = json.loads(response.content)
        self.assertFalse(data['ok'])
        self.assertEqual(GroupChatMessage.objects.count(), 1)


class GetUnreadCountsViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
        
        self.conversation = Conversation.objects.create(type='direct')
        ChatParticipant.objects.create(conversation=self.conversation, user=self.user1)
        ChatParticipant.objects.create(conversation=self.conversation, user=self.user2)
        
        Message.objects.create(
            conversation=self.conversation,
            sender=self.user2,
            content="Unread message 1"
        )
        Message.objects.create(
            conversation=self.conversation,
            sender=self.user2,
            content="Unread message 2"
        )
    
    def test_get_unread_counts(self):
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('get_unread_counts'))
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['ok'])
        self.assertEqual(len(data['conversations']), 1)
        self.assertEqual(data['conversations'][0]['unread_count'], 2)