"""
Tests for GameSessionManager - Integration tests using mocks
"""
import pytest
from unittest.mock import Mock, MagicMock
from chaos_ai.game_session_manager import GameSessionManager
from chaos_ai.player_manager import PlayerManager
from chaos_ai.story_engine import StoryEngine
from chaos_ai.contribution_handler import ContributionHandler
from chaos_ai.genai_service import GenAIService
from chaos_ai.models import GameStatus, ContributionType, Player


class TestGameSessionManager:
    """Tests for GameSessionManager component"""
    
    @pytest.fixture
    def setup_managers(self):
        """Setup all required managers"""
        player_manager = PlayerManager()
        genai_service = GenAIService()
        story_engine = StoryEngine(genai_service)
        contribution_handler = ContributionHandler()
        game_manager = GameSessionManager(
            player_manager=player_manager,
            story_engine=story_engine,
            contribution_handler=contribution_handler
        )
        
        return {
            'game_manager': game_manager,
            'player_manager': player_manager,
            'story_engine': story_engine,
            'contribution_handler': contribution_handler,
            'genai_service': genai_service
        }
    
    def test_create_session(self, setup_managers):
        """Test creating a game session"""
        game_manager = setup_managers['game_manager']
        
        session = game_manager.create_session(
            title="Epic Adventure",
            max_players=4,
            min_players=2
        )
        
        assert session is not None
        assert session.session_id is not None
        assert session.story.title == "Epic Adventure"
        assert session.max_players == 4
        assert session.min_players == 2
        assert session.status == GameStatus.WAITING
    
    def test_join_session(self, setup_managers):
        """Test player joining a session"""
        game_manager = setup_managers['game_manager']
        player_manager = setup_managers['player_manager']
        
        session = game_manager.create_session("Test Game")
        player = player_manager.register_player("testuser")
        
        result = game_manager.join_session(session.session_id, player)
        
        assert result is True
        assert player in session.players
        assert len(session.players) == 1
    
    def test_join_full_session(self, setup_managers):
        """Test joining a session that is full"""
        game_manager = setup_managers['game_manager']
        player_manager = setup_managers['player_manager']
        
        session = game_manager.create_session("Test Game", max_players=2)
        
        player1 = player_manager.register_player("user1")
        player2 = player_manager.register_player("user2")
        player3 = player_manager.register_player("user3")
        
        game_manager.join_session(session.session_id, player1)
        game_manager.join_session(session.session_id, player2)
        
        # Session is now full
        result = game_manager.join_session(session.session_id, player3)
        
        assert result is False
        assert len(session.players) == 2
        assert player3 not in session.players
    
    def test_start_session(self, setup_managers):
        """Test starting a game session"""
        game_manager = setup_managers['game_manager']
        player_manager = setup_managers['player_manager']
        
        session = game_manager.create_session("Test Game", min_players=2)
        
        player1 = player_manager.register_player("user1")
        player2 = player_manager.register_player("user2")
        
        game_manager.join_session(session.session_id, player1)
        game_manager.join_session(session.session_id, player2)
        
        result = game_manager.start_session(session.session_id)
        
        assert result is True
        assert session.status == GameStatus.IN_PROGRESS
    
    def test_start_session_without_enough_players(self, setup_managers):
        """Test starting a session without enough players"""
        game_manager = setup_managers['game_manager']
        player_manager = setup_managers['player_manager']
        
        session = game_manager.create_session("Test Game", min_players=2)
        player = player_manager.register_player("user1")
        
        game_manager.join_session(session.session_id, player)
        
        result = game_manager.start_session(session.session_id)
        
        assert result is False
        assert session.status == GameStatus.WAITING
    
    def test_submit_contribution(self, setup_managers):
        """Test submitting a player contribution"""
        game_manager = setup_managers['game_manager']
        player_manager = setup_managers['player_manager']
        
        # Setup game
        session = game_manager.create_session("Test Game", min_players=2)
        player1 = player_manager.register_player("user1")
        player2 = player_manager.register_player("user2")
        
        game_manager.join_session(session.session_id, player1)
        game_manager.join_session(session.session_id, player2)
        game_manager.start_session(session.session_id)
        
        # Submit contribution
        contribution = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player1.player_id,
            content="Hello",
            contribution_type=ContributionType.WORD
        )
        
        assert contribution is not None
        assert contribution.content == "Hello"
        assert len(session.story.contributions) == 1
        assert session.current_turn == 1
    
    def test_submit_contribution_wrong_player(self, setup_managers):
        """Test submitting contribution when it's not player's turn"""
        game_manager = setup_managers['game_manager']
        player_manager = setup_managers['player_manager']
        
        # Setup game
        session = game_manager.create_session("Test Game", min_players=2)
        player1 = player_manager.register_player("user1")
        player2 = player_manager.register_player("user2")
        
        game_manager.join_session(session.session_id, player1)
        game_manager.join_session(session.session_id, player2)
        game_manager.start_session(session.session_id)
        
        # Try to submit as player2 when it's player1's turn
        contribution = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player2.player_id,
            content="Hello",
            contribution_type=ContributionType.WORD
        )
        
        assert contribution is None
        assert len(session.story.contributions) == 0
    
    def test_submit_invalid_contribution(self, setup_managers):
        """Test submitting an invalid contribution"""
        game_manager = setup_managers['game_manager']
        player_manager = setup_managers['player_manager']
        
        # Setup game
        session = game_manager.create_session("Test Game", min_players=2)
        player1 = player_manager.register_player("user1")
        player2 = player_manager.register_player("user2")
        
        game_manager.join_session(session.session_id, player1)
        game_manager.join_session(session.session_id, player2)
        game_manager.start_session(session.session_id)
        
        # Try to submit multiple words as a WORD type
        contribution = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player1.player_id,
            content="Hello world",
            contribution_type=ContributionType.WORD
        )
        
        assert contribution is None
        assert len(session.story.contributions) == 0
    
    def test_end_session(self, setup_managers):
        """Test ending a game session"""
        game_manager = setup_managers['game_manager']
        
        session = game_manager.create_session("Test Game")
        
        result = game_manager.end_session(session.session_id)
        
        assert result is True
        assert session.status == GameStatus.COMPLETED
    
    def test_get_story_text(self, setup_managers):
        """Test getting the complete story text"""
        game_manager = setup_managers['game_manager']
        player_manager = setup_managers['player_manager']
        
        # Setup and play game
        session = game_manager.create_session("Test Game", min_players=2)
        player1 = player_manager.register_player("user1")
        player2 = player_manager.register_player("user2")
        
        game_manager.join_session(session.session_id, player1)
        game_manager.join_session(session.session_id, player2)
        game_manager.start_session(session.session_id)
        
        # Add contributions
        game_manager.submit_contribution(
            session.session_id, player1.player_id, "Once", ContributionType.WORD
        )
        game_manager.submit_contribution(
            session.session_id, player2.player_id, "upon a time", ContributionType.PHRASE
        )
        
        # Get story text
        text = game_manager.get_story_text(session.session_id)
        
        assert text is not None
        assert "Once" in text
        assert "upon a time" in text
    
    def test_ai_twist_added_at_correct_turn(self, setup_managers):
        """Test that AI twists are added at the correct turns"""
        game_manager = setup_managers['game_manager']
        player_manager = setup_managers['player_manager']
        
        # Setup game
        session = game_manager.create_session("Test Game", min_players=2)
        player1 = player_manager.register_player("user1")
        player2 = player_manager.register_player("user2")
        
        game_manager.join_session(session.session_id, player1)
        game_manager.join_session(session.session_id, player2)
        game_manager.start_session(session.session_id)
        
        # Play turns - twist added when turn number % 3 == 0 and turn > 0
        # Turn 0: No twist (turn == 0)
        game_manager.submit_contribution(
            session.session_id, player1.player_id, "Once", ContributionType.WORD
        )
        assert len(session.story.ai_twists) == 0
        
        # Turn 1: No twist (1 % 3 != 0)
        game_manager.submit_contribution(
            session.session_id, player2.player_id, "upon a time", ContributionType.PHRASE
        )
        assert len(session.story.ai_twists) == 0
        
        # Turn 2: No twist (2 % 3 != 0)
        game_manager.submit_contribution(
            session.session_id, player1.player_id, "there was", ContributionType.PHRASE
        )
        assert len(session.story.ai_twists) == 0
        
        # Turn 3: Twist added (3 % 3 == 0 and 3 > 0)
        game_manager.submit_contribution(
            session.session_id, player2.player_id, "a hero", ContributionType.PHRASE
        )
        assert len(session.story.ai_twists) == 1
