from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from music.models import Track, Genre
from groups.models import Group
from events.models import Event, EventAttendee


class RecommendationEngine:
    
    def __init__(self, user):
        self.user = user
        self.favorite_genres = [g.strip() for g in user.favorite_genres.split(',') if g.strip()] if user.favorite_genres else []
        self.favorite_artists = [a.strip() for a in user.favorite_artists.split(',') if a.strip()] if user.favorite_artists else []
        self.user_city = getattr(user, 'city', None)
    
    # Track recomendations
    def recommend_tracks(self, limit=20):
        recommendations = []
        
        # 40% Content-based 
        content_tracks = self._content_based_tracks(limit=8)
        recommendations.extend(content_tracks)
        
        # 40% Collaborative 
        collaborative_tracks = self._collaborative_tracks(limit=8)
        recommendations.extend(collaborative_tracks)
        
        # 20% Trending 
        trending_tracks = self._trending_tracks(limit=4)
        recommendations.extend(trending_tracks)
        
        return self._remove_duplicates(recommendations)[:limit]
    
    def _content_based_tracks(self, limit=8):
        tracks = Track.objects.exclude(
            reviews__user=self.user
        ).select_related('artist', 'genre')
        
        # Filter by favorite genres or artists
        if self.favorite_genres or self.favorite_artists:
            tracks = tracks.filter(
                Q(genre__name__in=self.favorite_genres) |
                Q(artist__name__in=self.favorite_artists)
            )
        
        return list(tracks.order_by('-average_rating_cached', '-created_at')[:limit])
    
    def _collaborative_tracks(self, limit=8):
        # Find similar users
        user_favorites = self.user.favorite_tracks.values_list('track_id', flat=True)
        
        if not user_favorites:
            return []
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        similar_users = User.objects.filter(
            favorite_tracks__track_id__in=user_favorites
        ).exclude(
            id=self.user.id
        ).annotate(
            common_tracks=Count('favorite_tracks')
        ).filter(
            common_tracks__gte=2  # At least 2 tracks in common
        ).order_by('-common_tracks')[:10]
        
        if not similar_users:
            return []
        
        # Get tracks liked by similar users
        tracks = Track.objects.filter(
            favorites__user__in=similar_users
        ).exclude(
            Q(favorites__user=self.user) |  
            Q(reviews__user=self.user)  
        ).annotate(
            score=Count('favorites')
        ).select_related('artist', 'genre').order_by('-score', '-average_rating_cached')[:limit]
        
        return list(tracks)
    
    def _trending_tracks(self, limit=4):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        tracks = Track.objects.filter(
            created_at__gte=thirty_days_ago
        ).exclude(
            reviews__user=self.user
        ).select_related('artist', 'genre').order_by(
            '-reviews_count_cached',
            '-average_rating_cached'
        )[:limit]
        
        return list(tracks)
    
    # Group recommendations
    
    def recommend_groups(self, limit=10):
        groups = Group.objects.exclude(
            members__user=self.user
        ).annotate(
            members_count=Count('members', filter=Q(members__status='accepted'))
        ).select_related('admin').prefetch_related('genres')
        
        scored_groups = []
        for group in groups:
            score = self._calculate_group_score(group)
            if score > 0:
                scored_groups.append((score, group))
        
        scored_groups.sort(key=lambda x: x[0], reverse=True)
        return [group for score, group in scored_groups[:limit]]
    
    def _calculate_group_score(self, group):
        score = 0
        # Genre match (0-40 points)
        group_genres = [g.name for g in group.genres.all()]
        matching_genres = set(group_genres) & set(self.favorite_genres)
        score += len(matching_genres) * 20  # 20 points per matching genre
        
        # Location match (0-30 points)
        if self.user_city and group.location:
            if group.location.lower() == self.user_city.lower():
                score += 30
            elif self.user_city.lower() in group.location.lower():
                score += 15
        
        # Popularity (0-20 points)
        members_count = getattr(group, 'members_count', 0)
        if members_count > 0:
            score += min(members_count, 20)
        
        # Recent activity (0-10 points)
        recent_events = group.events.filter(
            event_date__gte=timezone.now()
        ).count()
        score += min(recent_events * 5, 10)
        
        return score
    
    # Event recommendations
    
    def recommend_events(self, limit=10):
        now = timezone.now()
        
        user_groups = Group.objects.filter(
            members__user=self.user,
            members__status='accepted'
        )

        attending_event_ids = EventAttendee.objects.filter(
            user=self.user,
            status='going'
        ).values_list('event_id', flat=True)
        
        events = Event.objects.filter(
            event_date__gte=now
        ).exclude(
            id__in=attending_event_ids
        ).select_related('group', 'creator').prefetch_related('attendees')
        
        scored_events = []
        for event in events:
            score = self._calculate_event_score(event, user_groups)
            if score > 0:
                scored_events.append((score, event))
        
        # Sort by score, then by date
        scored_events.sort(key=lambda x: (-x[0], x[1].event_date))
        
        return [event for score, event in scored_events[:limit]]
    
    def _calculate_event_score(self, event, user_groups):
        score = 0
        
        # From user's groups (0-50 points)
        if event.group in user_groups:
            score += 50
        
        # Genre match (0-30 points)
        event_genres = [g.name for g in event.group.genres.all()]
        matching_genres = set(event_genres) & set(self.favorite_genres)
        score += len(matching_genres) * 15
        
        # Location match (0-20 points)
        if self.user_city and event.group.location:
            if event.group.location.lower() == self.user_city.lower():
                score += 20
        
        # Popularity (0-10 points)
        attendee_count = event.attendee_count
        score += min(attendee_count, 10)
        
        # Upcoming soon (0-10 points) - prioritize near events
        days_until = (event.event_date - timezone.now()).days
        if days_until < 7:
            score += 10
        elif days_until < 14:
            score += 5
        
        return score

    # Utility methods

    def _remove_duplicates(self, items):
        seen = set()
        unique = []
        for item in items:
            if item.id not in seen:
                seen.add(item.id)
                unique.append(item)
        return unique
    
    def get_recommendation_stats(self):
        return {
            'favorite_genres': self.favorite_genres,
            'favorite_artists': self.favorite_artists,
            'city': self.user_city,
            'total_favorites': self.user.favorite_tracks.count(),
            'total_reviews': self.user.reviews.count(),
        }