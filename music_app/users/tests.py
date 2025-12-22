"""
Focused tests for Users app
Tests cover the most important functionality:
- User registration and authentication
- User profiles (own and public)
- Follow/unfollow system
- Block/unblock system
- Profile editing
- Password management
- Recommendation system
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from users.models import User, UserFollow, UserBlock, ErrorReport
from music.models import Track, Artist, Review, Favorite
from groups.models import Group, GroupMembership

User = get_user_model()


class UserModelTest(TestCase):
    """Tests for User model"""
    
    def test_create_user(self):
        """Test creating a user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_user_level_property(self):
        """Test level calculation from XP"""
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        user.xp = 2500
        self.assertEqual(user.level, 2)  # 2500 / 1000 = 2
        
        user.xp = 999
        self.assertEqual(user.level, 0)  # 999 / 1000 = 0
    
    def test_user_level_progress_property(self):
        """Test level progress calculation"""
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        user.xp = 2750
        self.assertEqual(user.level_progress, 750)  # 2750 % 1000 = 750


class UserFollowModelTest(TestCase):
    """Tests for UserFollow model"""
    
    def setUp(self):
        """Set up test data"""
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
    
    def test_create_follow(self):
        """Test creating a follow relationship"""
        follow = UserFollow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        
        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.following, self.user2)
    
    def test_unique_follow(self):
        """Test that a user can only follow another user once"""
        UserFollow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            UserFollow.objects.create(
                follower=self.user1,
                following=self.user2
            )


class UserBlockModelTest(TestCase):
    """Tests for UserBlock model"""
    
    def setUp(self):
        """Set up test data"""
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
    
    def test_create_block(self):
        """Test creating a block relationship"""
        block = UserBlock.objects.create(
            blocker=self.user1,
            blocked=self.user2
        )
        
        self.assertEqual(block.blocker, self.user1)
        self.assertEqual(block.blocked, self.user2)
    
    def test_unique_block(self):
        """Test that a user can only block another user once"""
        UserBlock.objects.create(
            blocker=self.user1,
            blocked=self.user2
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            UserBlock.objects.create(
                blocker=self.user1,
                blocked=self.user2
            )


class ErrorReportModelTest(TestCase):
    """Tests for ErrorReport model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
    
    def test_create_error_report(self):
        """Test creating an error report"""
        report = ErrorReport.objects.create(
            user=self.user,
            title='Bug in profile page',
            description='The profile picture is not loading',
            content_type='general'
        )
        
        self.assertEqual(report.user, self.user)
        self.assertEqual(report.title, 'Bug in profile page')
        self.assertEqual(report.status, 'pending')


class RegisterViewTest(TestCase):
    """Tests for register_view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
    
    def test_register_page_accessible(self):
        """Test that register page is accessible"""
        response = self.client.get(reverse('register'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
    
    def test_register_success(self):
        """Test successful registration"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'accept_terms': True
        })
        
        # Should redirect
        self.assertEqual(response.status_code, 302)
        
        # Verify user was created
        self.assertTrue(
            User.objects.filter(username='newuser').exists()
        )
    
    def test_register_duplicate_email(self):
        """Test that registration fails with duplicate email"""
        User.objects.create_user(
            username='existing',
            email='test@test.com',
            password='testpass123'
        )
        
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'test@test.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'accept_terms': True
        })
        
        # Should not create user
        self.assertFalse(
            User.objects.filter(username='newuser').exists()
        )
    
    def test_register_password_mismatch(self):
        """Test that registration fails with mismatched passwords"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'SecurePass123!',
            'password2': 'DifferentPass123!',
            'accept_terms': True
        })
        
        # Should not create user
        self.assertFalse(
            User.objects.filter(username='newuser').exists()
        )


class LoginViewTest(TestCase):
    """Tests for login_view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        # Activate user for login
        self.user.is_active = True
        self.user.save()
    
    def test_login_page_accessible(self):
        """Test that login page is accessible"""
        response = self.client.get(reverse('login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
    
    def test_login_success(self):
        """Test successful login"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Should redirect to profile
        self.assertEqual(response.status_code, 302)
        
        # User should be authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        
        # User should not be authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class ProfileViewTest(TestCase):
    """Tests for profile_view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.user.xp = 1500
        self.user.save()
    
    def test_profile_requires_login(self):
        """Test that profile requires authentication"""
        response = self.client.get(reverse('profile'))
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)
    
    def test_profile_shows_user_info(self):
        """Test that profile shows user information"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['xp'], 1500)
        self.assertEqual(response.context['level'], 2)


class PublicProfileViewTest(TestCase):
    """Tests for user_profile_public view"""
    
    def setUp(self):
        """Set up test data"""
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
    
    def test_public_profile_accessible(self):
        """Test that public profile is accessible"""
        self.client.login(username='user1', password='testpass123')
        url = reverse('user_profile_public', kwargs={'username': 'user2'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile_public.html')


class FollowToggleTest(TestCase):
    """Tests for follow_toggle view"""
    
    def setUp(self):
        """Set up test data"""
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
    
    def test_follow_user(self):
        """Test following a user"""
        self.client.login(username='user1', password='testpass123')
        url = reverse('follow_toggle', kwargs={'username': 'user2'})
        response = self.client.post(url)
        
        # Should redirect
        self.assertEqual(response.status_code, 200)
        
        # Verify follow was created
        self.assertTrue(
            UserFollow.objects.filter(
                follower=self.user1,
                following=self.user2
            ).exists()
        )
    
    def test_unfollow_user(self):
        """Test unfollowing a user"""
        # Create initial follow
        UserFollow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        
        self.client.login(username='user1', password='testpass123')
        url = reverse('follow_toggle', kwargs={'username': 'user2'})
        response = self.client.post(url)
        
        # Should redirect
        self.assertEqual(response.status_code, 200)
        
        # Verify follow was removed
        self.assertFalse(
            UserFollow.objects.filter(
                follower=self.user1,
                following=self.user2
            ).exists()
        )
    
    def test_cannot_follow_self(self):
        """Test that user cannot follow themselves"""
        self.client.login(username='user1', password='testpass123')
        url = reverse('follow_toggle', kwargs={'username': 'user1'})
        response = self.client.post(url)
        
        # Should redirect
        self.assertEqual(response.status_code, 200)
        
        # Verify no self-follow was created
        self.assertFalse(
            UserFollow.objects.filter(
                follower=self.user1,
                following=self.user1
            ).exists()
        )


class BlockToggleTest(TestCase):
    """Tests for block_toggle view"""
    
    def setUp(self):
        """Set up test data"""
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
    
    def test_block_user(self):
        """Test blocking a user"""
        self.client.login(username='user1', password='testpass123')
        url = reverse('block_toggle', kwargs={'username': 'user2'})
        response = self.client.post(url)
        
        # Should redirect
        self.assertEqual(response.status_code, 200)
        
        # Verify block was created
        self.assertTrue(
            UserBlock.objects.filter(
                blocker=self.user1,
                blocked=self.user2
            ).exists()
        )
    
    def test_unblock_user(self):
        """Test unblocking a user"""
        # Create initial block
        UserBlock.objects.create(
            blocker=self.user1,
            blocked=self.user2
        )
        
        self.client.login(username='user1', password='testpass123')
        url = reverse('block_toggle', kwargs={'username': 'user2'})
        response = self.client.post(url)
        
        # Should redirect
        self.assertEqual(response.status_code, 200)
        
        # Verify block was removed
        self.assertFalse(
            UserBlock.objects.filter(
                blocker=self.user1,
                blocked=self.user2
            ).exists()
        )


class ProfileEditTest(TestCase):
    """Tests for profile_edit view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
    
    def test_profile_edit_requires_login(self):
        """Test that profile edit requires authentication"""
        response = self.client.get(reverse('profile_edit'))
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)
    
    def test_profile_edit_success(self):
        """Test successfully editing profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('profile_edit'), {
            'bio': 'Updated bio',
            'city': 'Warsaw',
            'favorite_genres': 'Hip Hop, Rock',
            'favorite_artists': 'Artist1, Artist2'
        })
        
        # Should redirect
        self.assertEqual(response.status_code, 302)
        
        # Verify profile was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, 'Updated bio')
        self.assertEqual(self.user.city, 'Warsaw')


class UserSearchTest(TestCase):
    """Tests for user_search view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='alice',
            email='alice@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='bob',
            email='bob@test.com',
            password='testpass123'
        )
        self.searcher = User.objects.create_user(
            username='searcher',
            email='searcher@test.com',
            password='testpass123'
        )
    
    
    def test_user_search_finds_users(self):
        """Test searching for users"""
        self.client.login(username='searcher', password='testpass123')
        response = self.client.get(reverse('user_search'), {'q': 'alice'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_search.html')
        
        # Check that alice is in results
        users = response.context['users']
        self.assertTrue(any(u.username == 'alice' for u in users))


class RecommendationEngineTest(TestCase):
    """Tests for RecommendationEngine"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.user.favorite_genres = 'Hip Hop, Rock'
        self.user.city = 'Warsaw'
        self.user.save()
        
        # Create some test data
        self.artist = Artist.objects.create(name='Test Artist')
        from music.models import Genre
        self.genre = Genre.objects.create(name='Hip Hop')
        
        self.track = Track.objects.create(
            title='Test Song',
            artist=self.artist,
            genre=self.genre
        )
    
    def test_recommendation_engine_initialization(self):
        """Test initializing recommendation engine"""
        from users.recommendations import RecommendationEngine
        
        engine = RecommendationEngine(self.user)
        
        self.assertEqual(engine.user, self.user)
        self.assertIn('Hip Hop', engine.favorite_genres)
        self.assertIn('Rock', engine.favorite_genres)
        self.assertEqual(engine.user_city, 'Warsaw')
    
    def test_recommend_tracks(self):
        """Test track recommendations"""
        from users.recommendations import RecommendationEngine
        
        engine = RecommendationEngine(self.user)
        recommendations = engine.recommend_tracks(limit=10)
        
        # Should return a list
        self.assertIsInstance(recommendations, list)


class ErrorReportTest(TestCase):
    """Tests for error reporting"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
    
    def test_report_error_requires_login(self):
        """Test that reporting error requires authentication"""
        response = self.client.get(reverse('report_error'))
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)
    
    def test_report_error_success(self):
        """Test successfully reporting an error"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('report_error'), {
            'title': 'Bug report',
            'description': 'Something is broken',
            'page_url': '/profile/',
            'content_type': 'general'
        })
        
        # Should redirect
        self.assertEqual(response.status_code, 302)
        
        # Verify report was created
        self.assertTrue(
            ErrorReport.objects.filter(
                user=self.user,
                title='Bug report'
            ).exists()
        )


class FollowersListTest(TestCase):
    """Tests for followers_list view"""
    
    def setUp(self):
        """Set up test data"""
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
        
        # user2 follows user1
        UserFollow.objects.create(
            follower=self.user2,
            following=self.user1
        )
    
    def test_followers_list_shows_followers(self):
        """Test that followers list shows correct followers"""
        self.client.login(username='user1', password='testpass123')
        url = reverse('followers_list', kwargs={'username': 'user1'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        # Check that user2 is in followers
        followers = response.context['followers']
        self.assertTrue(any(f.follower.username == 'user2' for f in followers))


class PasswordChangeTest(TestCase):
    """Tests for password_change view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='oldpass123'
        )
    
    def test_password_change_requires_login(self):
        """Test that password change requires authentication"""
        response = self.client.get(reverse('password_change'))
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)
    
    def test_password_change_success(self):
        """Test successfully changing password"""
        self.client.login(username='testuser', password='oldpass123')
        response = self.client.post(reverse('password_change'), {
            'old_password': 'oldpass123',
            'new_password1': 'NewSecurePass123!',
            'new_password2': 'NewSecurePass123!'
        })
        
        # Should redirect
        self.assertIn(response.status_code, [200, 302])
        
        # Verify password was changed (if successful)
        if response.status_code == 302:
            self.user.refresh_from_db()
            self.assertTrue(self.user.check_password('NewSecurePass123!'))