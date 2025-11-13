from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count, Max
from django.utils import timezone
from django.contrib import messages
from .models import Conversation, ChatParticipant, Message, MessageRead, GroupChatMessage, GroupChatRead
from groups.models import Group, GroupMembership

User = get_user_model()

@login_required
def chat_list(request):
    """List all conversations for the current user"""
    conversations = Conversation.objects.filter(
        participants__user=request.user,
        type='direct'
    ).annotate(
        message_count=Count('messages'),
        last_message_time=Max('messages__created_at')
    ).filter(message_count__gt=0).order_by('-updated_at').prefetch_related('participants__user', 'messages')
    
    # Add other_user and unread count to each conversation
    for conversation in conversations:
        conversation.other_user = conversation.get_other_participant(request.user)
        
        # Get participant info for current user
        participant = conversation.participants.get(user=request.user)
        
        # Count unread messages (messages created after last_read_at)
        if participant.last_read_at:
            conversation.unread_count = conversation.messages.filter(
                created_at__gt=participant.last_read_at
            ).exclude(sender=request.user).count()
        else:
            # If never read, count all messages except own
            conversation.unread_count = conversation.messages.exclude(
                sender=request.user
            ).count()
    
    return render(request, 'chat/chat_list.html', {
        'conversations': conversations
    })


@login_required
def conversation_detail(request, conversation_id):
    """View a specific conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Check if user is a participant
    if not conversation.participants.filter(user=request.user).exists():
        messages.error(request, 'Nie masz dostępu do tej rozmowy')
        return redirect('chat_list')
    
    # Get messages
    chat_messages = conversation.messages.select_related('sender').order_by('created_at')
    
    # Mark conversation as read
    participant = conversation.participants.get(user=request.user)
    participant.last_read_at = timezone.now()
    participant.save()
    
    # Get other participant (for direct messages)
    other_user = conversation.get_other_participant(request.user)
    
    return render(request, 'chat/conversation_detail.html', {
        'conversation': conversation,
        'messages': chat_messages,
        'other_user': other_user,
    })


@login_required
def start_conversation(request, username):
    """Start a new conversation with a user"""
    other_user = get_object_or_404(User, username=username)
    
    if other_user == request.user:
        messages.error(request, 'Nie możesz rozpocząć rozmowy z samym sobą')
        return redirect('user_search')
    
    # Check if conversation already exists
    existing_conversation = Conversation.objects.filter(
        type='direct',
        participants__user=request.user
    ).filter(
        participants__user=other_user
    ).first()
    
    if existing_conversation:
        return redirect('conversation_detail', conversation_id=existing_conversation.id)
    
    # Create new conversation
    conversation = Conversation.objects.create(type='direct')
    
    # Add participants
    ChatParticipant.objects.create(conversation=conversation, user=request.user)
    ChatParticipant.objects.create(conversation=conversation, user=other_user)
    
    return redirect('conversation_detail', conversation_id=conversation.id)


@require_POST
@login_required
def send_message(request):
    """Send a message via AJAX"""
    conversation_id = request.POST.get('conversation_id')
    content = request.POST.get('content', '').strip()
    
    if not content:
        return JsonResponse({'ok': False, 'message': 'Wiadomość nie może być pusta'})
    
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Check if user is a participant
    if not conversation.participants.filter(user=request.user).exists():
        return JsonResponse({'ok': False, 'message': 'Nie masz dostępu do tej rozmowy'})
    
    # Create message
    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        content=content
    )
    
    # Update conversation timestamp
    conversation.updated_at = timezone.now()
    conversation.save()
    
    return JsonResponse({
        'ok': True,
        'message': {
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'created_at': message.created_at.strftime('%H:%M'),
            'is_own': message.sender == request.user
        }
    })

@login_required
def get_new_messages(request, conversation_id):
    """Get new messages via AJAX"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Check if user is a participant
    if not conversation.participants.filter(user=request.user).exists():
        return JsonResponse({'ok': False, 'message': 'Brak dostępu'})
    
    # Get last message ID from request
    last_message_id = request.GET.get('last_message_id', 0)
    
    # Get messages newer than last_message_id
    new_messages = conversation.messages.filter(
        id__gt=last_message_id
    ).exclude(
        sender=request.user  # Don't fetch our own messages (already displayed)
    ).select_related('sender').order_by('created_at')
    
    messages_data = []
    for msg in new_messages:
        messages_data.append({
            'id': msg.id,
            'content': msg.content,
            'sender': msg.sender.username,
            'sender_picture': msg.sender.profile_picture.url if msg.sender.profile_picture else None,
            'created_at': msg.created_at.strftime('%H:%M'),
            'is_own': False
        })
    
    return JsonResponse({
        'ok': True,
        'messages': messages_data
    })

@login_required
def get_unread_counts(request):
    """Get unread message counts for all conversations via AJAX"""
    conversations = Conversation.objects.filter(
        participants__user=request.user,
        type='direct'
    ).prefetch_related('messages')
    
    data_list = []
    for conversation in conversations:
        participant = conversation.participants.get(user=request.user)
        
        if participant.last_read_at:
            unread_count = conversation.messages.filter(
                created_at__gt=participant.last_read_at
            ).exclude(sender=request.user).count()
        else:
            unread_count = conversation.messages.exclude(
                sender=request.user
            ).count()
        
        last_msg = conversation.messages.last()
        
        data_list.append({
            'conversation_id': conversation.id,
            'unread_count': unread_count,
            'last_message': {
                'content': last_msg.content if last_msg else '',
                'sender': last_msg.sender.username if last_msg else '',
                'is_own': last_msg.sender == request.user if last_msg else False,
                'time': last_msg.created_at.strftime('%H:%M') if last_msg else ''
            } if last_msg else None
        })
    
    return JsonResponse({
        'ok': True,
        'conversations': data_list
    })


@login_required
def group_chat(request, group_slug):
    """View group chat"""
    group = get_object_or_404(Group, slug=group_slug)
    
    # Check if user is a member
    from groups.models import GroupMembership
    if not GroupMembership.objects.filter(group=group, user=request.user, status='accepted').exists():
        messages.error(request, 'Tylko członkowie mogą przeglądać czat grupy')
        return redirect('group_detail', slug=group_slug)
    
    # Get messages
    chat_messages = group.chat_messages.select_related('sender').order_by('created_at')
    
    # Mark as read
    chat_read, created = GroupChatRead.objects.get_or_create(
        group=group,
        user=request.user
    )
    chat_read.save()  # Updates last_read_at
    
    is_admin = group.admin == request.user
    
    return render(request, 'chat/group_chat.html', {
        'group': group,
        'messages': chat_messages,
        'is_admin': is_admin,
    })


@require_POST
@login_required
def send_group_message(request):
    """Send a message to group chat via AJAX"""
    group_id = request.POST.get('group_id')
    content = request.POST.get('content', '').strip()
    
    if not content:
        return JsonResponse({'ok': False, 'message': 'Wiadomość nie może być pusta'})
    
    group = get_object_or_404(Group, id=group_id)
    
    # Check if user is a member
    from groups.models import GroupMembership
    if not GroupMembership.objects.filter(group=group, user=request.user, status='accepted').exists():
        return JsonResponse({'ok': False, 'message': 'Nie jesteś członkiem grupy'})
    
    # Create message
    message = GroupChatMessage.objects.create(
        group=group,
        sender=request.user,
        content=content
    )
    
    return JsonResponse({
        'ok': True,
        'message': {
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'sender_picture': message.sender.profile_picture.url if message.sender.profile_picture else None,
            'created_at': message.created_at.strftime('%H:%M'),
            'is_own': message.sender == request.user
        }
    })


@login_required
def get_new_group_messages(request, group_id):
    """Get new group messages via AJAX"""
    group = get_object_or_404(Group, id=group_id)
    
    # Check if user is a member
    from groups.models import GroupMembership
    if not GroupMembership.objects.filter(group=group, user=request.user, status='accepted').exists():
        return JsonResponse({'ok': False, 'message': 'Brak dostępu'})
    
    # Get last message ID from request
    last_message_id = request.GET.get('last_message_id', 0)
    
    # Get messages newer than last_message_id
    new_messages = group.chat_messages.filter(
        id__gt=last_message_id
    ).exclude(
        sender=request.user
    ).select_related('sender').order_by('created_at')
    
    messages_data = []
    for msg in new_messages:
        messages_data.append({
            'id': msg.id,
            'content': msg.content,
            'sender': msg.sender.username,
            'sender_picture': msg.sender.profile_picture.url if msg.sender.profile_picture else None,
            'created_at': msg.created_at.strftime('%H:%M'),
            'is_own': False
        })
    
    return JsonResponse({
        'ok': True,
        'messages': messages_data
    })


@require_POST
@login_required
def delete_group_message(request, message_id):
    """Delete a group message (admin only or message sender)"""
    message = get_object_or_404(GroupChatMessage, id=message_id)
    group = message.group
    
    # Only admin or message sender can delete
    if message.sender != request.user and group.admin != request.user:
        return JsonResponse({'ok': False, 'message': 'Brak uprawnień'})
    
    message.delete()
    return JsonResponse({'ok': True})

