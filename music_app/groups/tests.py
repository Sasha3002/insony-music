from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

from groups.models import Group, GroupMembership, GroupInvitation
from music.models import Genre

User = get_user_model()


class GroupModelTest(TestCase):
    """Tests for Group model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.genre = Genre.objects.create(name='Rock')
    
    def test_create_group(self):
        """Test creating a group"""
        group = Group.objects.create(
            name='Test Group',
            description='Test description',
            location='Warsaw',
            admin=self.user
        )
        
        self.assertEqual(group.name, 'Test Group')
        self.assertEqual(group.admin, self.user)
        self.assertEqual(group.type, 'public')  
    
    def test_slug_auto_generation(self):
        """Test that slug is automatically generated from name"""
        group = Group.objects.create(
            name='My Awesome Group',
            description='Test',
            location='Krakow',
            admin=self.user
        )
        
        self.assertEqual(group.slug, 'my-awesome-group')
    
    def test_member_count_property(self):
        """Test member_count property"""
        group = Group.objects.create(
            name='Test Group',
            description='Test',
            location='Warsaw',
            admin=self.user
        )
        
        user2 = User.objects.create_user(username='user2', email='u2@test.com', password='pass')
        user3 = User.objects.create_user(username='user3', email='u3@test.com', password='pass')
        GroupMembership.objects.create(group=group, user=user2, status='accepted')
        GroupMembership.objects.create(group=group, user=user3, status='accepted')
        user4 = User.objects.create_user(username='user4', email='u4@test.com', password='pass')
        GroupMembership.objects.create(group=group, user=user4, status='pending')
        
        self.assertEqual(group.member_count, 2) 


class GroupMembershipModelTest(TestCase):
    """Tests for GroupMembership model"""
    
    def setUp(self):
        """Set up test data"""
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.user = User.objects.create_user(
            username='member',
            email='member@test.com',
            password='testpass123'
        )
        self.group = Group.objects.create(
            name='Test Group',
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
    
    def test_create_membership(self):
        """Test creating a membership"""
        membership = GroupMembership.objects.create(
            group=self.group,
            user=self.user,
            status='accepted'
        )
        
        self.assertEqual(membership.group, self.group)
        self.assertEqual(membership.user, self.user)
        self.assertEqual(membership.status, 'accepted')
    
    def test_unique_membership_per_user_per_group(self):
        """Test that a user can only have one membership per group"""
        GroupMembership.objects.create(
            group=self.group,
            user=self.user,
            status='accepted'
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            GroupMembership.objects.create(
                group=self.group,
                user=self.user,
                status='pending'
            )


class GroupInvitationModelTest(TestCase):
    """Tests for GroupInvitation model"""
    
    def setUp(self):
        """Set up test data"""
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.user = User.objects.create_user(
            username='invitee',
            email='invitee@test.com',
            password='testpass123'
        )
        self.group = Group.objects.create(
            name='Test Group',
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
    
    def test_create_invitation(self):
        """Test creating an invitation"""
        invitation = GroupInvitation.objects.create(
            group=self.group,
            invited_by=self.admin,
            invited_user=self.user
        )
        
        self.assertEqual(invitation.group, self.group)
        self.assertEqual(invitation.invited_by, self.admin)
        self.assertEqual(invitation.invited_user, self.user)
        self.assertFalse(invitation.accepted)


class GroupCreateViewTest(TestCase):
    """Tests for group_create view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.genre = Genre.objects.create(name='Rock')
    
    def test_group_create_requires_login(self):
        """Test that creating group requires authentication"""
        response = self.client.get(reverse('group_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)
    
    def test_group_create_get(self):
        """Test GET request to create group page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('group_create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/group_create.html')
    
    def test_group_create_success(self):
        """Test successfully creating a group"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('group_create'), {
            'name': 'New Test Group',
            'description': 'A great group for testing',
            'location': 'Online',  
            'type': 'public',
            'genres': [self.genre.id]
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Group.objects.count(), 1)
        group = Group.objects.first()
        self.assertEqual(group.name, 'New Test Group')
        self.assertEqual(group.admin, self.user)
        self.assertTrue(
            GroupMembership.objects.filter(
                group=group,
                user=self.user,
                status='accepted'
            ).exists()
        )
    
    def test_group_create_missing_fields(self):
        """Test that creating group with missing fields fails"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('group_create'), {
            'name': 'Test Group',
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Group.objects.count(), 0)


class GroupDetailViewTest(TestCase):
    """Tests for group_detail view"""
    
    def setUp(self):
        """Set up test data"""
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
            location='Warsaw',
            admin=self.admin
        )
        
        GroupMembership.objects.create(
            group=self.group,
            user=self.admin,
            status='accepted'
        )
    
    def test_group_detail_requires_login(self):
        """Test that viewing group requires authentication"""
        response = self.client.get(reverse('group_detail', kwargs={'slug': self.group.slug}))
        self.assertEqual(response.status_code, 302)
    
    def test_group_detail_shows_info(self):
        """Test that group detail page displays group info"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('group_detail', kwargs={'slug': self.group.slug}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/group_detail.html')
        self.assertEqual(response.context['group'], self.group)
        self.assertTrue(response.context['is_admin'])


class GroupJoinViewTest(TestCase):
    """Tests for group_join view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.user = User.objects.create_user(
            username='joiner',
            email='joiner@test.com',
            password='testpass123'
        )
        self.public_group = Group.objects.create(
            name='Public Group',
            slug='public-group',
            description='Test',
            location='Warsaw',
            type='public',
            admin=self.admin
        )
        self.private_group = Group.objects.create(
            name='Private Group',
            slug='private-group',
            description='Test',
            location='Warsaw',
            type='private',
            admin=self.admin
        )
    
    def test_join_requires_post(self):
        """Test that joining requires POST method"""
        self.client.login(username='joiner', password='testpass123')
        response = self.client.get(reverse('group_join', kwargs={'slug': self.public_group.slug}))
        self.assertEqual(response.status_code, 405)  
    
    def test_join_public_group(self):
        """Test joining a public group"""
        self.client.login(username='joiner', password='testpass123')
        response = self.client.post(reverse('group_join', kwargs={'slug': self.public_group.slug}))
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            GroupMembership.objects.filter(
                group=self.public_group,
                user=self.user,
                status='accepted'
            ).exists()
        )
    
    def test_join_private_group(self):
        """Test joining a private group creates pending membership"""
        self.client.login(username='joiner', password='testpass123')
        response = self.client.post(reverse('group_join', kwargs={'slug': self.private_group.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            GroupMembership.objects.filter(
                group=self.private_group,
                user=self.user,
                status='pending'
            ).exists()
        )
    
    def test_cannot_join_twice(self):
        """Test that user cannot join a group they're already in"""
        GroupMembership.objects.create(
            group=self.public_group,
            user=self.user,
            status='accepted'
        )
        
        self.client.login(username='joiner', password='testpass123')
        response = self.client.post(reverse('group_join', kwargs={'slug': self.public_group.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            GroupMembership.objects.filter(
                group=self.public_group,
                user=self.user
            ).count(),
            1
        )


class GroupLeaveViewTest(TestCase):
    """Tests for group_leave view"""
    
    def setUp(self):
        """Set up test data"""
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
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
        
        GroupMembership.objects.create(group=self.group, user=self.admin, status='accepted')
        GroupMembership.objects.create(group=self.group, user=self.member, status='accepted')
    
    def test_leave_group_success(self):
        """Test successfully leaving a group"""
        self.client.login(username='member', password='testpass123')
        response = self.client.post(reverse('group_leave', kwargs={'slug': self.group.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            GroupMembership.objects.filter(
                group=self.group,
                user=self.member
            ).exists()
        )
    
    def test_admin_cannot_leave(self):
        """Test that admin cannot leave their own group"""
        self.client.login(username='admin', password='testpass123')
        response = self.client.post(reverse('group_leave', kwargs={'slug': self.group.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            GroupMembership.objects.filter(
                group=self.group,
                user=self.admin
            ).exists()
        )


class ApproveMemberViewTest(TestCase):
    """Tests for approve_member view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.regular_member = User.objects.create_user(
            username='regular',
            email='regular@test.com',
            password='testpass123'
        )
        self.pending_user = User.objects.create_user(
            username='pending',
            email='pending@test.com',
            password='testpass123'
        )
        
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test',
            location='Warsaw',
            type='private',
            admin=self.admin
        )
        
        GroupMembership.objects.create(group=self.group, user=self.admin, status='accepted')
        GroupMembership.objects.create(group=self.group, user=self.regular_member, status='accepted')
        self.pending_membership = GroupMembership.objects.create(
            group=self.group,
            user=self.pending_user,
            status='pending'
        )
    
    def test_admin_can_approve_member(self):
        """Test that admin can approve pending member"""
        self.client.login(username='admin', password='testpass123')
        url = reverse('approve_member', kwargs={
            'slug': self.group.slug,
            'membership_id': self.pending_membership.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.pending_membership.refresh_from_db()
        self.assertEqual(self.pending_membership.status, 'accepted')
    
    def test_regular_member_cannot_approve(self):
        """Test that regular member cannot approve pending members"""
        self.client.login(username='regular', password='testpass123')
        url = reverse('approve_member', kwargs={
            'slug': self.group.slug,
            'membership_id': self.pending_membership.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.pending_membership.refresh_from_db()
        self.assertEqual(self.pending_membership.status, 'pending')


class RejectMemberViewTest(TestCase):
    """Tests for reject_member view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.pending_user = User.objects.create_user(
            username='pending',
            email='pending@test.com',
            password='testpass123'
        )
        
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test',
            location='Warsaw',
            type='private',
            admin=self.admin
        )
        
        self.pending_membership = GroupMembership.objects.create(
            group=self.group,
            user=self.pending_user,
            status='pending'
        )
    
    def test_admin_can_reject_member(self):
        """Test that admin can reject pending member"""
        self.client.login(username='admin', password='testpass123')
        url = reverse('reject_member', kwargs={
            'slug': self.group.slug,
            'membership_id': self.pending_membership.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            GroupMembership.objects.filter(
                id=self.pending_membership.id
            ).exists()
        )


class GroupInviteViewTest(TestCase):
    """Tests for group_invite view"""
    
    def setUp(self):
        """Set up test data"""
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
        self.invitee = User.objects.create_user(
            username='invitee',
            email='invitee@test.com',
            password='testpass123'
        )
        
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
        
        GroupMembership.objects.create(group=self.group, user=self.admin, status='accepted')
        GroupMembership.objects.create(group=self.group, user=self.member, status='accepted')
    
    def test_member_can_invite(self):
        """Test that member can invite users"""
        self.client.login(username='member', password='testpass123')
        response = self.client.post(
            reverse('group_invite', kwargs={'slug': self.group.slug}),
            {'username': 'invitee'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            GroupInvitation.objects.filter(
                group=self.group,
                invited_user=self.invitee
            ).exists()
        )
    
    def test_non_member_cannot_invite(self):
        """Test that non-member cannot invite users"""
        non_member = User.objects.create_user(
            username='outsider',
            email='outsider@test.com',
            password='testpass123'
        )
        
        self.client.login(username='outsider', password='testpass123')
        response = self.client.post(
            reverse('group_invite', kwargs={'slug': self.group.slug}),
            {'username': 'invitee'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            GroupInvitation.objects.filter(
                group=self.group,
                invited_user=self.invitee
            ).exists()
        )


class AcceptInvitationViewTest(TestCase):
    """Tests for accept_invitation view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.invitee = User.objects.create_user(
            username='invitee',
            email='invitee@test.com',
            password='testpass123'
        )
        
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
        
        self.invitation = GroupInvitation.objects.create(
            group=self.group,
            invited_by=self.admin,
            invited_user=self.invitee
        )
    
    def test_accept_invitation_success(self):
        """Test successfully accepting an invitation"""
        self.client.login(username='invitee', password='testpass123')
        url = reverse('accept_invitation', kwargs={'invitation_id': self.invitation.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            GroupMembership.objects.filter(
                group=self.group,
                user=self.invitee,
                status='accepted'
            ).exists()
        )
        self.assertFalse(
            GroupInvitation.objects.filter(
                id=self.invitation.id
            ).exists()
        )


class DeclineInvitationViewTest(TestCase):
    """Tests for decline_invitation view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.invitee = User.objects.create_user(
            username='invitee',
            email='invitee@test.com',
            password='testpass123'
        )
        
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
        
        self.invitation = GroupInvitation.objects.create(
            group=self.group,
            invited_by=self.admin,
            invited_user=self.invitee
        )
    
    def test_decline_invitation_success(self):
        """Test successfully declining an invitation"""
        self.client.login(username='invitee', password='testpass123')
        url = reverse('decline_invitation', kwargs={'invitation_id': self.invitation.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            GroupInvitation.objects.filter(
                id=self.invitation.id
            ).exists()
        )
        
        self.assertFalse(
            GroupMembership.objects.filter(
                group=self.group,
                user=self.invitee
            ).exists()
        )


class RemoveMemberViewTest(TestCase):
    """Tests for remove_member view"""
    
    def setUp(self):
        """Set up test data"""
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
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
        
        GroupMembership.objects.create(group=self.group, user=self.admin, status='accepted')
        GroupMembership.objects.create(group=self.group, user=self.member, status='accepted')
    
    def test_admin_can_remove_member(self):
        """Test that admin can remove a member"""
        self.client.login(username='admin', password='testpass123')
        url = reverse('remove_member', kwargs={
            'slug': self.group.slug,
            'user_id': self.member.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            GroupMembership.objects.filter(
                group=self.group,
                user=self.member
            ).exists()
        )
    
    def test_admin_cannot_remove_self(self):
        """Test that admin cannot remove themselves"""
        self.client.login(username='admin', password='testpass123')
        url = reverse('remove_member', kwargs={
            'slug': self.group.slug,
            'user_id': self.admin.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            GroupMembership.objects.filter(
                group=self.group,
                user=self.admin
            ).exists()
        )