"""
Tests for ContributionHandler
"""
import pytest
from chaos_ai.contribution_handler import ContributionHandler
from chaos_ai.models import Player, ContributionType


class TestContributionHandler:
    """Tests for ContributionHandler component"""
    
    def test_create_contribution(self):
        """Test creating a contribution"""
        handler = ContributionHandler()
        player = Player(player_id="p1", username="user1")
        
        contribution = handler.create_contribution(
            player=player,
            content="Hello",
            contribution_type=ContributionType.WORD,
            turn_number=0
        )
        
        assert contribution is not None
        assert contribution.player_id == "p1"
        assert contribution.content == "Hello"
        assert contribution.contribution_type == ContributionType.WORD
        assert contribution.turn_number == 0
        assert contribution.contribution_id is not None
    
    def test_validate_word_contribution(self):
        """Test validating word contributions"""
        handler = ContributionHandler()
        
        # Valid word
        assert handler.validate_contribution("Hello", ContributionType.WORD) is True
        
        # Invalid - multiple words
        assert handler.validate_contribution("Hello world", ContributionType.WORD) is False
        
        # Invalid - empty
        assert handler.validate_contribution("", ContributionType.WORD) is False
        assert handler.validate_contribution("   ", ContributionType.WORD) is False
    
    def test_validate_phrase_contribution(self):
        """Test validating phrase contributions"""
        handler = ContributionHandler()
        
        # Valid phrases (2-5 words)
        assert handler.validate_contribution("Hello world", ContributionType.PHRASE) is True
        assert handler.validate_contribution("Once upon a time", ContributionType.PHRASE) is True
        assert handler.validate_contribution("In the beginning was", ContributionType.PHRASE) is True
        
        # Invalid - too few words
        assert handler.validate_contribution("Hello", ContributionType.PHRASE) is False
        
        # Invalid - too many words
        assert handler.validate_contribution("One two three four five six", ContributionType.PHRASE) is False
        
        # Invalid - empty
        assert handler.validate_contribution("", ContributionType.PHRASE) is False
    
    def test_validate_sentence_contribution(self):
        """Test validating sentence contributions"""
        handler = ContributionHandler()
        
        # Valid sentences (3+ words)
        assert handler.validate_contribution("This is valid.", ContributionType.SENTENCE) is True
        assert handler.validate_contribution("Once upon a time there was", ContributionType.SENTENCE) is True
        
        # Invalid - too few words
        assert handler.validate_contribution("Hello", ContributionType.SENTENCE) is False
        assert handler.validate_contribution("Hello world", ContributionType.SENTENCE) is False
        
        # Invalid - empty
        assert handler.validate_contribution("", ContributionType.SENTENCE) is False
    
    def test_get_contribution(self):
        """Test getting a contribution by ID"""
        handler = ContributionHandler()
        player = Player(player_id="p1", username="user1")
        
        contribution = handler.create_contribution(
            player=player,
            content="Test",
            contribution_type=ContributionType.WORD,
            turn_number=0
        )
        
        retrieved = handler.get_contribution(contribution.contribution_id)
        
        assert retrieved == contribution
        assert retrieved.content == "Test"
    
    def test_get_nonexistent_contribution(self):
        """Test getting a contribution that doesn't exist"""
        handler = ContributionHandler()
        
        result = handler.get_contribution("nonexistent-id")
        
        assert result is None
