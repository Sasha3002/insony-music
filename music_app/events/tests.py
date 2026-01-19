"""
Focused tests for Events app
Tests cover the most important functionality:
- Model creation and properties
- Event CRUD operations
- Attendance management
- Event ratings (for past events)
- Poll system (voting and applying changes)
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from events.models import Event, EventAttendee, EventRating, EventPoll, PollVote
from groups.models import Group, GroupMembership
from music.models import Playlist

User = get_user_model()


class EventModelTest(TestCase):
    """Tests for Event model"""
    
    def setUp(self):
        """Set up test data"""
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
    
    def test_create_event(self):
        """Test creating an event"""
        future_date = timezone.now() + timedelta(days=7)
        
        event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Test Concert',
            description='A great concert',
            location='Club XYZ',
            event_date=future_date
        )
        
        self.assertEqual(event.title, 'Test Concert')
        self.assertEqual(event.group, self.group)
        self.assertEqual(event.creator, self.admin)
    
    def test_slug_auto_generation(self):
        """Test that slug is automatically generated"""
        event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='My Awesome Concert',
            description='Test',
            location='Club',
            event_date=timezone.now()
        )
        
        self.assertEqual(event.slug, 'my-awesome-concert')
    
    def test_is_past_property(self):
        """Test is_past property"""
        past_date = timezone.now() - timedelta(days=7)
        past_event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Past Event',
            description='Test',
            location='Club',
            event_date=past_date
        )
        self.assertTrue(past_event.is_past)
        future_date = timezone.now() + timedelta(days=7)
        future_event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Future Event',
            description='Test',
            location='Club',
            event_date=future_date
        )
        self.assertFalse(future_event.is_past)
    
    def test_attendee_count_property(self):
        """Test attendee_count property"""
        event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Test Event',
            description='Test',
            location='Club',
            event_date=timezone.now()
        )
        
        user1 = User.objects.create_user(username='user1', email='u1@test.com', password='pass')
        user2 = User.objects.create_user(username='user2', email='u2@test.com', password='pass')
        user3 = User.objects.create_user(username='user3', email='u3@test.com', password='pass')
        
        EventAttendee.objects.create(event=event, user=user1, status='going')
        EventAttendee.objects.create(event=event, user=user2, status='going')
        EventAttendee.objects.create(event=event, user=user3, status='maybe') 
        
        self.assertEqual(event.attendee_count, 2)


class EventAttendeeModelTest(TestCase):
    """Tests for EventAttendee model"""
    
    def setUp(self):
        """Set up test data"""
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='testpass123'
        )
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
        self.event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Test Event',
            description='Test',
            location='Club',
            event_date=timezone.now()
        )
    
    def test_create_attendee(self):
        """Test creating an attendee"""
        attendee = EventAttendee.objects.create(
            event=self.event,
            user=self.user,
            status='going'
        )
        
        self.assertEqual(attendee.event, self.event)
        self.assertEqual(attendee.user, self.user)
        self.assertEqual(attendee.status, 'going')
    
    def test_unique_attendee_per_user_per_event(self):
        """Test that a user can only have one attendance per event"""
        EventAttendee.objects.create(
            event=self.event,
            user=self.user,
            status='going'
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            EventAttendee.objects.create(
                event=self.event,
                user=self.user,
                status='maybe'
            )


class EventRatingModelTest(TestCase):
    """Tests for EventRating model"""
    
    def setUp(self):
        """Set up test data"""
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
        self.event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Test Event',
            description='Test',
            location='Club',
            event_date=timezone.now() - timedelta(days=1) 
        )
    
    def test_create_rating(self):
        """Test creating a rating"""
        rating = EventRating.objects.create(
            event=self.event,
            user=self.admin,
            rating=5,
            comment='Great event!'
        )
        
        self.assertEqual(rating.event, self.event)
        self.assertEqual(rating.user, self.admin)
        self.assertEqual(rating.rating, 5)
    
    def test_average_rating(self):
        """Test average rating calculation"""
        user1 = User.objects.create_user(username='user1', email='u1@test.com', password='pass')
        user2 = User.objects.create_user(username='user2', email='u2@test.com', password='pass')
        
        EventRating.objects.create(event=self.event, user=user1, rating=5)
        EventRating.objects.create(event=self.event, user=user2, rating=3)
        
        self.assertEqual(self.event.average_rating, 4.0)


class EventCreateViewTest(TestCase):
    """Tests for event_create view"""
    
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
        self.non_member = User.objects.create_user(
            username='nonmember',
            email='nonmember@test.com',
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
    
    def test_event_create_requires_login(self):
        """Test that creating event requires authentication"""
        url = reverse('event_create', kwargs={'group_slug': self.group.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_only_members_can_create(self):
        """Test that only group members can create events"""
        self.client.login(username='nonmember', password='testpass123')
        url = reverse('event_create', kwargs={'group_slug': self.group.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_event_create_success(self):
        """Test successfully creating an event"""
        self.client.login(username='member', password='testpass123')
        future_date = timezone.now() + timedelta(days=7)
        future_date_str = future_date.strftime('%Y-%m-%dT%H:%M')

        url = reverse('event_create', kwargs={'group_slug': self.group.slug})
        response = self.client.post(url, {
            'title': 'New Concert',
            'description': 'Amazing concert',
            'location': 'Club XYZ',
            'event_date': future_date_str,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.exists())
        event = Event.objects.first()
        self.assertEqual(event.title, 'New Concert')
        self.assertEqual(event.creator, self.member)
        self.assertTrue(
            EventAttendee.objects.filter(
                event=event,
                user=self.member,
                status='going'
            ).exists()
        )


class EventDetailViewTest(TestCase):
    """Tests for event_detail view"""
    
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
        
        self.event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Test Event',
            slug='test-event',
            description='Test',
            location='Club',
            event_date=timezone.now() + timedelta(days=7)
        )
        
        GroupMembership.objects.create(group=self.group, user=self.admin, status='accepted')
        GroupMembership.objects.create(group=self.group, user=self.member, status='accepted')
    
    def test_event_detail_requires_login(self):
        """Test that viewing event requires authentication"""
        url = reverse('event_detail', kwargs={'slug': self.event.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_event_detail_shows_info(self):
        """Test that event detail shows event information"""
        self.client.login(username='member', password='testpass123')
        url = reverse('event_detail', kwargs={'slug': self.event.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_detail.html')
        self.assertEqual(response.context['event'], self.event)


class EventAttendViewTest(TestCase):
    """Tests for event_attend view"""
    
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
        
        self.event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Test Event',
            slug='test-event',
            description='Test',
            location='Club',
            event_date=timezone.now() + timedelta(days=7)
        )
        
        GroupMembership.objects.create(group=self.group, user=self.admin, status='accepted')
        GroupMembership.objects.create(group=self.group, user=self.member, status='accepted')
    
    def test_attend_requires_post(self):
        """Test that attending requires POST method"""
        self.client.login(username='member', password='testpass123')
        url = reverse('event_attend', kwargs={'slug': self.event.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
    
    def test_attend_event_success(self):
        """Test successfully marking attendance"""
        self.client.login(username='member', password='testpass123')
        url = reverse('event_attend', kwargs={'slug': self.event.slug})
        response = self.client.post(url, {'status': 'going'})
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            EventAttendee.objects.filter(
                event=self.event,
                user=self.member,
                status='going'
            ).exists()
        )
    
    def test_update_attendance_status(self):
        """Test updating attendance status"""
        EventAttendee.objects.create(
            event=self.event,
            user=self.member,
            status='going'
        )
        
        self.client.login(username='member', password='testpass123')
        url = reverse('event_attend', kwargs={'slug': self.event.slug})
        response = self.client.post(url, {'status': 'maybe'})
        attendee = EventAttendee.objects.get(event=self.event, user=self.member)
        self.assertEqual(attendee.status, 'maybe')
    
    def test_non_member_cannot_attend(self):
        """Test that non-members cannot attend"""
        non_member = User.objects.create_user(
            username='outsider',
            email='outsider@test.com',
            password='testpass123'
        )
        
        self.client.login(username='outsider', password='testpass123')
        url = reverse('event_attend', kwargs={'slug': self.event.slug})
        response = self.client.post(url, {'status': 'going'})

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            EventAttendee.objects.filter(
                event=self.event,
                user=non_member
            ).exists()
        )


class RateEventViewTest(TestCase):
    """Tests for rate_event view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.attendee = User.objects.create_user(
            username='attendee',
            email='attendee@test.com',
            password='testpass123'
        )
        
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
        
        self.past_event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Past Event',
            slug='past-event',
            description='Test',
            location='Club',
            event_date=timezone.now() - timedelta(days=7)
        )
        
        GroupMembership.objects.create(group=self.group, user=self.admin, status='accepted')
        GroupMembership.objects.create(group=self.group, user=self.attendee, status='accepted')
        EventAttendee.objects.create(
            event=self.past_event,
            user=self.attendee,
            status='going'
        )
    
    def test_rate_past_event_success(self):
        """Test rating a past event"""
        self.client.login(username='attendee', password='testpass123')
        url = reverse('rate_event', kwargs={'slug': self.past_event.slug})
        response = self.client.post(url, {
            'rating': 5,
            'comment': 'Great event!'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            EventRating.objects.filter(
                event=self.past_event,
                user=self.attendee,
                rating=5
            ).exists()
        )
    
    def test_cannot_rate_future_event(self):
        """Test that users cannot rate future events"""
        future_event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Future Event',
            slug='future-event',
            description='Test',
            location='Club',
            event_date=timezone.now() + timedelta(days=7)
        )
        
        self.client.login(username='attendee', password='testpass123')
        url = reverse('rate_event', kwargs={'slug': future_event.slug})
        response = self.client.post(url, {
            'rating': 5,
            'comment': 'Test'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            EventRating.objects.filter(
                event=future_event,
                user=self.attendee
            ).exists()
        )


class EventPollTest(TestCase):
    """Tests for EventPoll model and voting"""
    
    def setUp(self):
        """Set up test data"""
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.attendee = User.objects.create_user(
            username='attendee',
            email='attendee@test.com',
            password='testpass123'
        )
        
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
        
        self.event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Test Event',
            slug='test-event',
            description='Test',
            location='Club',
            event_date=timezone.now() + timedelta(days=7)
        )
        
        self.poll = EventPoll.objects.create(
            event=self.event,
            creator=self.admin,
            poll_type='time',
            title='Change event time?',
            description='Propose moving event 1 hour later',
            proposed_date=timezone.now() + timedelta(days=7, hours=1),
            closes_at=timezone.now() + timedelta(days=3)
        )
        
        GroupMembership.objects.create(group=self.group, user=self.admin, status='accepted')
        GroupMembership.objects.create(group=self.group, user=self.attendee, status='accepted')
        
        EventAttendee.objects.create(event=self.event, user=self.attendee, status='going')
    
    def test_poll_properties(self):
        """Test poll property calculations"""
        PollVote.objects.create(poll=self.poll, user=self.admin, vote=True)
        PollVote.objects.create(poll=self.poll, user=self.attendee, vote=True)
        
        self.assertEqual(self.poll.votes_for, 2)
        self.assertEqual(self.poll.votes_against, 0)
        self.assertEqual(self.poll.total_votes, 2)
        self.assertEqual(self.poll.approval_percentage, 100.0)
    
    def test_is_closed_property(self):
        """Test is_closed property"""
        self.assertFalse(self.poll.is_closed)
        self.poll.is_active = False
        self.poll.save()
        self.assertTrue(self.poll.is_closed)


class VoteOnPollViewTest(TestCase):
    """Tests for vote_on_poll view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.attendee = User.objects.create_user(
            username='attendee',
            email='attendee@test.com',
            password='testpass123'
        )
        
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
        
        self.event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Test Event',
            slug='test-event',
            description='Test',
            location='Club',
            event_date=timezone.now() + timedelta(days=7)
        )
        
        self.poll = EventPoll.objects.create(
            event=self.event,
            creator=self.admin,
            poll_type='time',
            title='Change time?',
            description='Test',
            closes_at=timezone.now() + timedelta(days=3)
        )
        
        GroupMembership.objects.create(group=self.group, user=self.admin, status='accepted')
        GroupMembership.objects.create(group=self.group, user=self.attendee, status='accepted')
        
        EventAttendee.objects.create(event=self.event, user=self.attendee, status='going')
    
    def test_vote_on_poll_success(self):
        """Test successfully voting on a poll"""
        self.client.login(username='attendee', password='testpass123')
        url = reverse('vote_on_poll', kwargs={'poll_id': self.poll.id})
        response = self.client.post(url, {'vote': 'yes'})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            PollVote.objects.filter(
                poll=self.poll,
                user=self.attendee,
                vote=True
            ).exists()
        )
    
    def test_only_attendees_can_vote(self):
        """Test that only event attendees can vote"""
        non_attendee = User.objects.create_user(
            username='member',
            email='member@test.com',
            password='testpass123'
        )
        GroupMembership.objects.create(group=self.group, user=non_attendee, status='accepted')
        
        self.client.login(username='member', password='testpass123')
        url = reverse('vote_on_poll', kwargs={'poll_id': self.poll.id})
        response = self.client.post(url, {'vote': 'yes'})

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            PollVote.objects.filter(
                poll=self.poll,
                user=non_attendee
            ).exists()
        )


class ApplyPollChangesViewTest(TestCase):
    """Tests for apply_poll_changes view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.attendee = User.objects.create_user(
            username='attendee',
            email='attendee@test.com',
            password='testpass123'
        )
        
        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            description='Test',
            location='Warsaw',
            admin=self.admin
        )
        
        self.original_date = timezone.now() + timedelta(days=7)
        self.new_date = timezone.now() + timedelta(days=7, hours=2)
        
        self.event = Event.objects.create(
            group=self.group,
            creator=self.admin,
            title='Test Event',
            slug='test-event',
            description='Test',
            location='Club',
            event_date=self.original_date
        )
        
        self.poll = EventPoll.objects.create(
            event=self.event,
            creator=self.admin,
            poll_type='time',
            title='Change time?',
            description='Test',
            proposed_date=self.new_date,
            closes_at=timezone.now() + timedelta(days=3)
        )
        
        GroupMembership.objects.create(group=self.group, user=self.admin, status='accepted')
        GroupMembership.objects.create(group=self.group, user=self.attendee, status='accepted')
        
        EventAttendee.objects.create(event=self.event, user=self.attendee, status='going')
    
    def test_admin_can_apply_approved_changes(self):
        """Test that admin can apply changes if poll passed"""
        PollVote.objects.create(poll=self.poll, user=self.admin, vote=True)
        PollVote.objects.create(poll=self.poll, user=self.attendee, vote=True)
        
        self.client.login(username='admin', password='testpass123')
        url = reverse('apply_poll_changes', kwargs={'poll_id': self.poll.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.event_date, self.new_date)
        self.poll.refresh_from_db()
        self.assertFalse(self.poll.is_active)
    
    def test_cannot_apply_without_majority(self):
        """Test that changes cannot be applied without majority approval"""
        PollVote.objects.create(poll=self.poll, user=self.admin, vote=False)
        PollVote.objects.create(poll=self.poll, user=self.attendee, vote=False)  
        self.assertLess(self.poll.approval_percentage, 50)
        original_date = self.event.event_date
        
        self.client.login(username='admin', password='testpass123')
        url = reverse('apply_poll_changes', kwargs={'poll_id': self.poll.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.event.refresh_from_db()
        self.assertEqual(self.event.event_date.replace(microsecond=0), 
                         original_date.replace(microsecond=0))
    
    def test_only_admin_can_apply_changes(self):
        """Test that only group admin can apply poll changes"""
        PollVote.objects.create(poll=self.poll, user=self.admin, vote=True)
        PollVote.objects.create(poll=self.poll, user=self.attendee, vote=True)
        
        self.client.login(username='attendee', password='testpass123')
        url = reverse('apply_poll_changes', kwargs={'poll_id': self.poll.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.event_date, self.original_date)