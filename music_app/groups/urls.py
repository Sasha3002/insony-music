from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('create/', views.group_create, name='group_create'),
    path('<slug:slug>/', views.group_detail, name='group_detail'),
    path('<slug:slug>/edit/', views.group_edit, name='group_edit'),
    path('<slug:slug>/delete/', views.group_delete, name='group_delete'),
    path('<slug:slug>/join/', views.group_join, name='group_join'),
    path('<slug:slug>/leave/', views.group_leave, name='group_leave'),
    path('<slug:slug>/invite/', views.group_invite, name='group_invite'),
    path('<slug:slug>/members/', views.group_members, name='group_members'),
    path('<slug:slug>/approve/<int:membership_id>/', views.approve_member, name='approve_member'),
    path('<slug:slug>/reject/<int:membership_id>/', views.reject_member, name='reject_member'),
]