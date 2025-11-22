"""
Integration tests demonstrating the complete prototype flow
This test shows how all components interact in a real game scenario
"""
import pytest
from chaos_ai.game_session_manager import GameSessionManager
from chaos_ai.player_manager import PlayerManager
from chaos_ai.story_engine import StoryEngine
from chaos_ai.contribution_handler import ContributionHandler
from chaos_ai.genai_service import GenAIService
from chaos_ai.models import GameStatus, ContributionType


class TestPrototypeFlow:
    """End-to-end integration tests for the prototype"""
    
    def test_complete_game_flow(self):
        """Test a complete game from start to finish"""
        # Initialize all components
        player_manager = PlayerManager()
        genai_service = GenAIService()
        story_engine = StoryEngine(genai_service)
        contribution_handler = ContributionHandler()
        game_manager = GameSessionManager(
            player_manager=player_manager,
            story_engine=story_engine,
            contribution_handler=contribution_handler
        )
        
        # Step 1: Create a game session
        session = game_manager.create_session(
            title="The Epic Space Adventure",
            max_players=4,
            min_players=2
        )
        assert session is not None
        assert session.status == GameStatus.WAITING
        print(f"\n✓ Game session created: {session.story.title}")
        
        # Step 2: Register players
        player1 = player_manager.register_player("Alice")
        player2 = player_manager.register_player("Bob")
        player3 = player_manager.register_player("Charlie")
        print(f"✓ Players registered: {player1.username}, {player2.username}, {player3.username}")
        
        # Step 3: Players join the session
        assert game_manager.join_session(session.session_id, player1) is True
        assert game_manager.join_session(session.session_id, player2) is True
        assert game_manager.join_session(session.session_id, player3) is True
        assert len(session.players) == 3
        print(f"✓ Players joined session: {len(session.players)} players")
        
        # Step 4: Start the game
        assert game_manager.start_session(session.session_id) is True
        assert session.status == GameStatus.IN_PROGRESS
        print("✓ Game started!")
        
        # Step 5: Players take turns making contributions
        print("\n--- Story Building Phase ---")
        
        # Turn 0: Alice's turn
        contrib1 = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player1.player_id,
            content="Once",
            contribution_type=ContributionType.WORD
        )
        assert contrib1 is not None
        print(f"Turn 0 ({player1.username}): {contrib1.content}")
        
        # Turn 1: Bob's turn
        contrib2 = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player2.player_id,
            content="upon a time",
            contribution_type=ContributionType.PHRASE
        )
        assert contrib2 is not None
        print(f"Turn 1 ({player2.username}): {contrib2.content}")
        
        # Turn 2: Charlie's turn
        contrib3 = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player3.player_id,
            content="there was a brave astronaut",
            contribution_type=ContributionType.SENTENCE
        )
        assert contrib3 is not None
        print(f"Turn 2 ({player3.username}): {contrib3.content}")
        
        # Turn 3: Alice's turn (AI twist should be added)
        contrib4 = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player1.player_id,
            content="who discovered",
            contribution_type=ContributionType.PHRASE
        )
        assert contrib4 is not None
        print(f"Turn 3 ({player1.username}): {contrib4.content}")
        
        # Check that AI twist was added
        assert len(session.story.ai_twists) == 1
        print(f"🎭 AI Twist: {session.story.ai_twists[0].content}")
        
        # Turn 4: Bob's turn
        contrib5 = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player2.player_id,
            content="a mysterious planet",
            contribution_type=ContributionType.PHRASE
        )
        assert contrib5 is not None
        print(f"Turn 4 ({player2.username}): {contrib5.content}")
        
        # Turn 5: Charlie's turn
        contrib6 = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player3.player_id,
            content="filled with strange creatures",
            contribution_type=ContributionType.PHRASE
        )
        assert contrib6 is not None
        print(f"Turn 5 ({player3.username}): {contrib6.content}")
        
        # Step 6: Get the complete story
        story_text = game_manager.get_story_text(session.session_id)
        assert story_text is not None
        assert "Once" in story_text
        assert "astronaut" in story_text
        print(f"\n--- Complete Story ---")
        print(story_text)
        
        # Step 7: End the game
        assert game_manager.end_session(session.session_id) is True
        assert session.status == GameStatus.COMPLETED
        print(f"\n✓ Game completed!")
        
        # Verify final state
        assert len(session.story.contributions) == 6
        assert session.current_turn == 6
        print(f"✓ Total contributions: {len(session.story.contributions)}")
        print(f"✓ Total AI twists: {len(session.story.ai_twists)}")
    
    def test_invalid_turn_scenario(self):
        """Test that wrong player cannot submit during another player's turn"""
        # Setup
        player_manager = PlayerManager()
        genai_service = GenAIService()
        story_engine = StoryEngine(genai_service)
        contribution_handler = ContributionHandler()
        game_manager = GameSessionManager(
            player_manager=player_manager,
            story_engine=story_engine,
            contribution_handler=contribution_handler
        )
        
        # Create game and add players
        session = game_manager.create_session("Test Game")
        player1 = player_manager.register_player("Player1")
        player2 = player_manager.register_player("Player2")
        
        game_manager.join_session(session.session_id, player1)
        game_manager.join_session(session.session_id, player2)
        game_manager.start_session(session.session_id)
        
        # It's player1's turn, but player2 tries to submit
        result = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player2.player_id,
            content="Invalid",
            contribution_type=ContributionType.WORD
        )
        
        assert result is None
        assert len(session.story.contributions) == 0
        print("✓ Invalid turn prevented successfully")
    
    def test_contribution_validation_scenario(self):
        """Test that invalid contributions are rejected"""
        # Setup
        player_manager = PlayerManager()
        genai_service = GenAIService()
        story_engine = StoryEngine(genai_service)
        contribution_handler = ContributionHandler()
        game_manager = GameSessionManager(
            player_manager=player_manager,
            story_engine=story_engine,
            contribution_handler=contribution_handler
        )
        
        # Create game and add players
        session = game_manager.create_session("Test Game")
        player1 = player_manager.register_player("Player1")
        player2 = player_manager.register_player("Player2")
        
        game_manager.join_session(session.session_id, player1)
        game_manager.join_session(session.session_id, player2)
        game_manager.start_session(session.session_id)
        
        # Try to submit multiple words as a WORD type (should fail)
        result = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player1.player_id,
            content="Multiple words here",
            contribution_type=ContributionType.WORD
        )
        
        assert result is None
        assert len(session.story.contributions) == 0
        print("✓ Invalid contribution rejected successfully")
        
        # Submit a valid contribution
        result = game_manager.submit_contribution(
            session_id=session.session_id,
            player_id=player1.player_id,
            content="Hello",
            contribution_type=ContributionType.WORD
        )
        
        assert result is not None
        assert len(session.story.contributions) == 1
        print("✓ Valid contribution accepted successfully")
    
    def test_multiplayer_turn_rotation(self):
        """Test that turns rotate correctly among multiple players"""
        # Setup
        player_manager = PlayerManager()
        genai_service = GenAIService()
        story_engine = StoryEngine(genai_service)
        contribution_handler = ContributionHandler()
        game_manager = GameSessionManager(
            player_manager=player_manager,
            story_engine=story_engine,
            contribution_handler=contribution_handler
        )
        
        # Create game with 3 players
        session = game_manager.create_session("Turn Rotation Test")
        player1 = player_manager.register_player("Player1")
        player2 = player_manager.register_player("Player2")
        player3 = player_manager.register_player("Player3")
        
        game_manager.join_session(session.session_id, player1)
        game_manager.join_session(session.session_id, player2)
        game_manager.join_session(session.session_id, player3)
        game_manager.start_session(session.session_id)
        
        # Track whose turn it is
        turns = []
        
        # Turn 0: Player1
        current_player = session.get_current_player()
        assert current_player == player1
        turns.append(current_player.username)
        game_manager.submit_contribution(
            session.session_id, player1.player_id, "First", ContributionType.WORD
        )
        
        # Turn 1: Player2
        current_player = session.get_current_player()
        assert current_player == player2
        turns.append(current_player.username)
        game_manager.submit_contribution(
            session.session_id, player2.player_id, "Second", ContributionType.WORD
        )
        
        # Turn 2: Player3
        current_player = session.get_current_player()
        assert current_player == player3
        turns.append(current_player.username)
        game_manager.submit_contribution(
            session.session_id, player3.player_id, "Third", ContributionType.WORD
        )
        
        # Turn 3: Back to Player1
        current_player = session.get_current_player()
        assert current_player == player1
        turns.append(current_player.username)
        
        print(f"✓ Turn rotation working: {' -> '.join(turns)}")
        assert turns == ["Player1", "Player2", "Player3", "Player1"]
