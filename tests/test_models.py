"""
Tests for data models
"""
import pytest
from datetime import datetime
from chaos_ai.models import (
    Player, GameSession, Contribution, Story, AITwist,
    GameStatus, ContributionType
)


class TestPlayer:
    """Tests for Player model"""
    
    def test_player_creation(self):
        """Test creating a player"""
        player = Player(player_id="123", username="testuser")
        assert player.player_id == "123"
        assert player.username == "testuser"
        assert player.is_active is True
        assert isinstance(player.joined_at, datetime)
    
    def test_player_hashable(self):
        """Test that player can be used in sets/dicts"""
        player1 = Player(player_id="123", username="user1")
        player2 = Player(player_id="123", username="user2")
        player3 = Player(player_id="456", username="user3")
        
        assert hash(player1) == hash(player2)
        assert hash(player1) != hash(player3)


class TestContribution:
    """Tests for Contribution model"""
    
    def test_contribution_creation(self):
        """Test creating a contribution"""
        contribution = Contribution(
            contribution_id="contrib-1",
            player_id="player-1",
            content="Once upon a time",
            contribution_type=ContributionType.PHRASE,
            turn_number=1
        )
        
        assert contribution.contribution_id == "contrib-1"
        assert contribution.player_id == "player-1"
        assert contribution.content == "Once upon a time"
        assert contribution.contribution_type == ContributionType.PHRASE
        assert contribution.turn_number == 1


class TestAITwist:
    """Tests for AITwist model"""
    
    def test_ai_twist_creation(self):
        """Test creating an AI twist"""
        twist = AITwist(
            twist_id="twist-1",
            content="Suddenly, dragons appeared!",
            applied_after_turn=3
        )
        
        assert twist.twist_id == "twist-1"
        assert twist.content == "Suddenly, dragons appeared!"
        assert twist.applied_after_turn == 3


class TestStory:
    """Tests for Story model"""
    
    def test_story_creation(self):
        """Test creating a story"""
        story = Story(story_id="story-1", title="Epic Adventure")
        
        assert story.story_id == "story-1"
        assert story.title == "Epic Adventure"
        assert story.contributions == []
        assert story.ai_twists == []
    
    def test_story_get_full_text(self):
        """Test getting full story text"""
        story = Story(story_id="story-1", title="Test Story")
        
        contribution1 = Contribution(
            contribution_id="c1",
            player_id="p1",
            content="Hello",
            contribution_type=ContributionType.WORD,
            turn_number=0
        )
        contribution2 = Contribution(
            contribution_id="c2",
            player_id="p2",
            content="world",
            contribution_type=ContributionType.WORD,
            turn_number=1
        )
        
        story.contributions = [contribution1, contribution2]
        
        assert story.get_full_text() == "Hello world"


class TestGameSession:
    """Tests for GameSession model"""
    
    def test_game_session_creation(self):
        """Test creating a game session"""
        story = Story(story_id="story-1", title="Test")
        session = GameSession(session_id="session-1", story=story)
        
        assert session.session_id == "session-1"
        assert session.story == story
        assert session.players == []
        assert session.status == GameStatus.WAITING
        assert session.current_turn == 0
    
    def test_is_ready_to_start(self):
        """Test checking if session is ready to start"""
        story = Story(story_id="story-1", title="Test")
        session = GameSession(session_id="session-1", story=story, min_players=2)
        
        assert session.is_ready_to_start() is False
        
        session.players.append(Player(player_id="p1", username="user1"))
        assert session.is_ready_to_start() is False
        
        session.players.append(Player(player_id="p2", username="user2"))
        assert session.is_ready_to_start() is True
    
    def test_is_full(self):
        """Test checking if session is full"""
        story = Story(story_id="story-1", title="Test")
        session = GameSession(session_id="session-1", story=story, max_players=2)
        
        assert session.is_full() is False
        
        session.players.append(Player(player_id="p1", username="user1"))
        assert session.is_full() is False
        
        session.players.append(Player(player_id="p2", username="user2"))
        assert session.is_full() is True
    
    def test_get_current_player(self):
        """Test getting current player based on turn"""
        story = Story(story_id="story-1", title="Test")
        session = GameSession(session_id="session-1", story=story)
        
        player1 = Player(player_id="p1", username="user1")
        player2 = Player(player_id="p2", username="user2")
        
        session.players = [player1, player2]
        
        # Turn 0 should be player1
        session.current_turn = 0
        assert session.get_current_player() == player1
        
        # Turn 1 should be player2
        session.current_turn = 1
        assert session.get_current_player() == player2
        
        # Turn 2 should cycle back to player1
        session.current_turn = 2
        assert session.get_current_player() == player1
