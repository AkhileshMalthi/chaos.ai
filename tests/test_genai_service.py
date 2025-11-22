"""
Tests for GenAIService
"""
import pytest
from chaos_ai.genai_service import GenAIService
from chaos_ai.models import Story, AITwist, Contribution, ContributionType


class TestGenAIService:
    """Tests for GenAIService component"""
    
    def test_generate_twist(self):
        """Test generating an AI twist"""
        service = GenAIService()
        story = Story(story_id="story-1", title="Test Story")
        
        twist = service.generate_twist(story, turn_number=3)
        
        assert twist is not None
        assert isinstance(twist, AITwist)
        assert twist.twist_id is not None
        assert twist.content is not None
        assert len(twist.content) > 0
        assert twist.applied_after_turn == 3
    
    def test_generate_twist_with_mock_client(self):
        """Test generating twist with mock AI client"""
        mock_client = object()  # Placeholder for future AI client
        service = GenAIService(ai_client=mock_client)
        story = Story(story_id="story-1", title="Test Story")
        
        twist = service.generate_twist(story, turn_number=1)
        
        assert twist is not None
        assert isinstance(twist, AITwist)
    
    def test_should_add_twist(self):
        """Test determining when to add twists"""
        service = GenAIService()
        
        # Should not add twist at turn 0
        assert service.should_add_twist(0) is False
        
        # Should not add twist at turn 1 or 2
        assert service.should_add_twist(1) is False
        assert service.should_add_twist(2) is False
        
        # Should add twist at turn 3 (every 3 turns)
        assert service.should_add_twist(3) is True
        
        # Should not add at turn 4 or 5
        assert service.should_add_twist(4) is False
        assert service.should_add_twist(5) is False
        
        # Should add twist at turn 6
        assert service.should_add_twist(6) is True
    
    def test_multiple_twists_are_different(self):
        """Test that multiple twists can vary"""
        service = GenAIService()
        story = Story(story_id="story-1", title="Test Story")
        
        twist1 = service.generate_twist(story, turn_number=0)
        twist2 = service.generate_twist(story, turn_number=1)
        
        # Twists should have unique IDs
        assert twist1.twist_id != twist2.twist_id
        
        # Content may or may not be different (cycling through mock twists)
        # but twists are distinct objects
        assert twist1 is not twist2
