from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('start/<str:username>/', views.start_conversation, name='start_conversation'),
    path('send/', views.send_message, name='send_message'),
    path('conversation/<int:conversation_id>/new/', views.get_new_messages, name='get_new_messages'),
    path('unread-counts/', views.get_unread_counts, name='get_unread_counts'),
    path('group/send/', views.send_group_message, name='send_group_message'),
    path('group/<int:group_id>/new/', views.get_new_group_messages, name='get_new_group_messages'),
    path('group/message/<int:message_id>/delete/', views.delete_group_message, name='delete_group_message'),
    path('group/<slug:group_slug>/', views.group_chat, name='group_chat'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
]