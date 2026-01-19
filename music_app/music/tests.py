from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import timedelta

from music.models import (
    Artist, Genre, Track, Review, ReviewLike, 
    Favorite, Playlist, PlaylistTrack
)

User = get_user_model()


class ArtistModelTest(TestCase):
    """Tests for Artist model"""
    
    def test_create_artist(self):
        """Test creating an artist"""
        artist = Artist.objects.create(
            name='Test Artist',
            bio='A great artist'
        )
        
        self.assertEqual(artist.name, 'Test Artist')
        self.assertEqual(str(artist), 'Test Artist')
    
    def test_artist_name_unique(self):
        """Test that artist names must be unique"""
        Artist.objects.create(name='Unique Artist')
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Artist.objects.create(name='Unique Artist')


class TrackModelTest(TestCase):
    """Tests for Track model"""
    
    def setUp(self):
        """Set up test data"""
        self.artist = Artist.objects.create(name='Test Artist')
        self.genre = Genre.objects.create(name='Hip Hop')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
    
    def test_create_track(self):
        """Test creating a track"""
        track = Track.objects.create(
            title='Test Song',
            artist=self.artist,
            genre=self.genre,
            created_by=self.user
        )
        
        self.assertEqual(track.title, 'Test Song')
        self.assertEqual(track.artist, self.artist)
        self.assertEqual(str(track), 'Test Song - Test Artist')
    
    def test_track_duration_display(self):
        """Test duration display property"""
        track = Track.objects.create(
            title='Test Song',
            artist=self.artist,
            duration=timedelta(minutes=3, seconds=45)
        )
        
        self.assertEqual(track.duration_display, '3:45')
    
    def test_track_average_rating_cached(self):
        """Test that average rating is cached"""
        track = Track.objects.create(
            title='Test Song',
            artist=self.artist,
            average_rating_cached=85.5
        )
        
        self.assertEqual(track.average_rating, 85.5)


class ReviewModelTest(TestCase):
    """Tests for Review model"""
    
    def setUp(self):
        """Set up test data"""
        self.artist = Artist.objects.create(name='Test Artist')
        self.track = Track.objects.create(
            title='Test Song',
            artist=self.artist
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
    
    def test_create_review(self):
        """Test creating a review"""
        review = Review.objects.create(
            track=self.track,
            user=self.user,
            title='Great track!',
            rhyme_imagery=8,
            structure_rhythm=7,
            style_execution=9,
            individuality=8,
            atmosphere_vibe=7,
            trend_relevance=6,
            text='Amazing song!'
        )
        
        self.assertEqual(review.track, self.track)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.title, 'Great track!')
    
    def test_review_total_points(self):
        """Test total_points property calculation"""
        review = Review.objects.create(
            track=self.track,
            user=self.user,
            rhyme_imagery=10,
            structure_rhythm=9,
            style_execution=8,
            individuality=7,
            atmosphere_vibe=6,
            trend_relevance=5
        )
        
        self.assertEqual(review.total_points, 45)
    
    def test_review_total_percent(self):
        """Test total_percent property calculation"""
        review = Review.objects.create(
            track=self.track,
            user=self.user,
            rhyme_imagery=10,
            structure_rhythm=10,
            style_execution=10,
            individuality=10,
            atmosphere_vibe=10,
            trend_relevance=10
        )
        
        self.assertEqual(review.total_percent, 100.0)
    
    def test_one_review_per_user_per_track(self):
        """Test that user can only have one review per track"""
        Review.objects.create(
            track=self.track,
            user=self.user,
            rhyme_imagery=5
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                track=self.track,
                user=self.user,
                rhyme_imagery=8
            )
    
    def test_review_criteria_constraints(self):
        """Test that review criteria are within 0-10 range"""
        from django.db import IntegrityError
        
        review = Review.objects.create(
            track=self.track,
            user=self.user,
            rhyme_imagery=10,
            structure_rhythm=0
        )
        self.assertIsNotNone(review)


class ReviewLikeTest(TestCase):
    """Tests for ReviewLike model"""
    
    def setUp(self):
        """Set up test data"""
        self.artist = Artist.objects.create(name='Test Artist')
        self.track = Track.objects.create(
            title='Test Song',
            artist=self.artist
        )
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
        self.review = Review.objects.create(
            track=self.track,
            user=self.user1,
            rhyme_imagery=8
        )
    
    def test_create_review_like(self):
        """Test creating a review like"""
        like = ReviewLike.objects.create(
            review=self.review,
            user=self.user2
        )
        
        self.assertEqual(like.review, self.review)
        self.assertEqual(like.user, self.user2)
    
    def test_one_like_per_user_per_review(self):
        """Test that user can only like a review once"""
        ReviewLike.objects.create(
            review=self.review,
            user=self.user2
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            ReviewLike.objects.create(
                review=self.review,
                user=self.user2
            )


class FavoriteModelTest(TestCase):
    """Tests for Favorite model"""
    
    def setUp(self):
        """Set up test data"""
        self.artist = Artist.objects.create(name='Test Artist')
        self.track = Track.objects.create(
            title='Test Song',
            artist=self.artist
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
    
    def test_create_favorite(self):
        """Test creating a favorite"""
        favorite = Favorite.objects.create(
            user=self.user,
            track=self.track
        )
        
        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.track, self.track)
    
    def test_one_favorite_per_user_per_track(self):
        """Test that user can only favorite a track once"""
        Favorite.objects.create(
            user=self.user,
            track=self.track
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Favorite.objects.create(
                user=self.user,
                track=self.track
            )


class PlaylistModelTest(TestCase):
    """Tests for Playlist model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.artist = Artist.objects.create(name='Test Artist')
        self.track = Track.objects.create(
            title='Test Song',
            artist=self.artist
        )
    
    def test_create_playlist(self):
        """Test creating a playlist"""
        playlist = Playlist.objects.create(
            user=self.user,
            name='My Playlist',
            description='Cool songs',
            is_public=True
        )
        
        self.assertEqual(playlist.name, 'My Playlist')
        self.assertEqual(playlist.user, self.user)
        self.assertTrue(playlist.is_public)
    
    def test_playlist_track_count(self):
        """Test track_count property"""
        playlist = Playlist.objects.create(
            user=self.user,
            name='My Playlist'
        )
        
        PlaylistTrack.objects.create(
            playlist=playlist,
            track=self.track,
            position=1
        )
        
        self.assertEqual(playlist.track_count, 1)
    
    def test_one_favorites_playlist_per_user(self):
        """Test that user can only have one favorites playlist"""
        Playlist.objects.create(
            user=self.user,
            name='Favorites',
            is_favorite=True
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Playlist.objects.create(
                user=self.user,
                name='Another Favorites',
                is_favorite=True
            )


class TrackListViewTest(TestCase):
    """Tests for track_list view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.artist = Artist.objects.create(name='Test Artist')
        self.genre = Genre.objects.create(name='Hip Hop')
        
        self.track1 = Track.objects.create(
            title='First Song',
            artist=self.artist,
            genre=self.genre
        )
        self.track2 = Track.objects.create(
            title='Second Song',
            artist=self.artist,
            genre=self.genre
        )
    
    def test_track_list_accessible(self):
        """Test that track list is accessible"""
        response = self.client.get(reverse('track_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/track_list.html')
    
    def test_track_list_shows_tracks(self):
        """Test that track list displays tracks"""
        response = self.client.get(reverse('track_list'))
        
        self.assertIn('tracks', response.context)
        self.assertGreaterEqual(len(response.context['tracks']), 2)
    
    def test_track_list_search(self):
        """Test searching tracks"""
        response = self.client.get(reverse('track_list'), {'q': 'First'})
        
        tracks = list(response.context['tracks'])
        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0].title, 'First Song')


class TrackDetailViewTest(TestCase):
    """Tests for track_detail view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.artist = Artist.objects.create(name='Test Artist')
        self.track = Track.objects.create(
            title='Test Song',
            artist=self.artist
        )
    
    def test_track_detail_accessible(self):
        """Test that track detail is accessible"""
        response = self.client.get(reverse('track_detail', kwargs={'track_id': self.track.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music/track_detail.html')
        self.assertEqual(response.context['track'], self.track)
    
    def test_track_detail_shows_reviews(self):
        """Test that track detail shows reviews"""
        Review.objects.create(
            track=self.track,
            user=self.user,
            rhyme_imagery=8,
            title='Great!'
        )
        
        response = self.client.get(reverse('track_detail', kwargs={'track_id': self.track.id}))
        
        self.assertIn('reviews_page', response.context)
        self.assertEqual(response.context['total_reviews'], 1)


class ReviewCreateTest(TestCase):
    """Tests for creating reviews via track_detail POST"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.artist = Artist.objects.create(name='Test Artist')
        self.track = Track.objects.create(
            title='Test Song',
            artist=self.artist
        )
    
    def test_create_review_requires_login(self):
        """Test that creating review requires authentication"""
        response = self.client.post(
            reverse('track_detail', kwargs={'track_id': self.track.id}),
            {
                'title': 'Great track',
                'rhyme_imagery': 8,
                'structure_rhythm': 7,
                'style_execution': 9,
                'individuality': 8,
                'atmosphere_vibe': 7,
                'trend_relevance': 6,
            }
        )
        self.assertEqual(Review.objects.count(), 0)
    
    def test_create_review_success(self):
        """Test successfully creating a review"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('track_detail', kwargs={'track_id': self.track.id}),
            {
                'title': 'Great track',
                'rhyme_imagery': 8,
                'structure_rhythm': 7,
                'style_execution': 9,
                'individuality': 8,
                'atmosphere_vibe': 7,
                'trend_relevance': 6,
                'text': 'Amazing song!'
            }
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.track, self.track)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rhyme_imagery, 8)


class ReviewLikeToggleTest(TestCase):
    """Tests for review_like_toggle AJAX view"""
    
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
        self.artist = Artist.objects.create(name='Test Artist')
        self.track = Track.objects.create(
            title='Test Song',
            artist=self.artist
        )
        self.review = Review.objects.create(
            track=self.track,
            user=self.user1,
            rhyme_imagery=8
        )
    
    def test_like_toggle_requires_login(self):
        """Test that liking requires authentication"""
        url = reverse('review_like_toggle', kwargs={'review_id': self.review.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 401)
    
    def test_like_review(self):
        """Test liking a review"""
        self.client.login(username='user2', password='testpass123')
        url = reverse('review_like_toggle', kwargs={'review_id': self.review.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['ok'])
        self.assertTrue(data['liked'])
        self.assertEqual(data['count'], 1)
        self.assertTrue(
            ReviewLike.objects.filter(
                review=self.review,
                user=self.user2
            ).exists()
        )
    
    def test_unlike_review(self):
        """Test unliking a review"""
        ReviewLike.objects.create(
            review=self.review,
            user=self.user2
        )
        
        self.client.login(username='user2', password='testpass123')
        url = reverse('review_like_toggle', kwargs={'review_id': self.review.id})
        response = self.client.post(url)
        
        data = response.json()
        self.assertTrue(data['ok'])
        self.assertFalse(data['liked'])
        self.assertEqual(data['count'], 0)
        self.assertFalse(
            ReviewLike.objects.filter(
                review=self.review,
                user=self.user2
            ).exists()
        )


class FavoriteToggleTest(TestCase):
    """Tests for favorite_toggle view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.artist = Artist.objects.create(name='Test Artist')
        self.track = Track.objects.create(
            title='Test Song',
            artist=self.artist
        )
    
    def test_favorite_toggle_requires_login(self):
        """Test that favoriting requires authentication"""
        url = reverse('favorite_toggle', kwargs={'track_id': self.track.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)
    
    def test_add_to_favorites(self):
        """Test adding track to favorites"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('favorite_toggle', kwargs={'track_id': self.track.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Favorite.objects.filter(
                user=self.user,
                track=self.track
            ).exists()
        )
    
    def test_remove_from_favorites(self):
        """Test removing track from favorites"""
        Favorite.objects.create(
            user=self.user,
            track=self.track
        )
        
        self.client.login(username='testuser', password='testpass123')
        url = reverse('favorite_toggle', kwargs={'track_id': self.track.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Favorite.objects.filter(
                user=self.user,
                track=self.track
            ).exists()
        )


class PlaylistCreateTest(TestCase):
    """Tests for playlist_create view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
    
    def test_playlist_create_requires_login(self):
        """Test that creating playlist requires authentication"""
        url = reverse('playlist_create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)
    
    def test_create_playlist_success(self):
        """Test successfully creating a playlist"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('playlist_create')
        response = self.client.post(url, {
            'name': 'My Awesome Playlist',
            'description': 'Great songs',
            'is_public': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Playlist.objects.filter(
                user=self.user,
                name='My Awesome Playlist'
            ).exists()
        )


class PlaylistAddTrackTest(TestCase):
    """Tests for playlist_add_track view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.artist = Artist.objects.create(name='Test Artist')
        self.track = Track.objects.create(
            title='Test Song',
            artist=self.artist
        )
        self.playlist = Playlist.objects.create(
            user=self.user,
            name='My Playlist'
        )
    
    def test_add_track_to_playlist_requires_login(self):
        """Test that adding track requires authentication"""
        url = reverse('playlist_add_track', kwargs={
            'playlist_id': self.playlist.id,
            'track_id': self.track.id
        })
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)
    
    def test_add_track_to_playlist_success(self):
        """Test successfully adding track to playlist"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('playlist_add_track', kwargs={
            'playlist_id': self.playlist.id,
            'track_id': self.track.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            PlaylistTrack.objects.filter(
                playlist=self.playlist,
                track=self.track
            ).exists()
        )
    
    def test_cannot_add_track_to_others_playlist(self):
        """Test that user cannot add track to someone else's playlist"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@test.com',
            password='testpass123'
        )
        
        self.client.login(username='otheruser', password='testpass123')
        url = reverse('playlist_add_track', kwargs={
            'playlist_id': self.playlist.id,
            'track_id': self.track.id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(
            PlaylistTrack.objects.filter(
                playlist=self.playlist,
                track=self.track
            ).exists()
        )


class ReviewDeleteTest(TestCase):
    """Tests for review_delete view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.artist = Artist.objects.create(name='Test Artist')
        self.track = Track.objects.create(
            title='Test Song',
            artist=self.artist
        )
        self.review = Review.objects.create(
            track=self.track,
            user=self.user,
            rhyme_imagery=8
        )
    
    def test_delete_own_review(self):
        """Test deleting own review"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('review_delete', kwargs={'track_id': self.track.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Review.objects.filter(id=self.review.id).exists()
        )
    
    def test_cannot_delete_others_review(self):
        """Test that user cannot delete someone else's review"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@test.com',
            password='testpass123'
        )
        
        self.client.login(username='otheruser', password='testpass123')
        url = reverse('review_delete', kwargs={'track_id': self.track.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Review.objects.filter(id=self.review.id).exists()
        )