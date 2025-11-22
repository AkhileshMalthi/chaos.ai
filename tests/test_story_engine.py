"""
Tests for StoryEngine
"""
import pytest
from unittest.mock import Mock, MagicMock
from chaos_ai.story_engine import StoryEngine
from chaos_ai.genai_service import GenAIService
from chaos_ai.models import Story, Contribution, AITwist, ContributionType


class TestStoryEngine:
    """Tests for StoryEngine component"""
    
    def test_create_story(self):
        """Test creating a new story"""
        genai_service = GenAIService()
        engine = StoryEngine(genai_service)
        
        story = engine.create_story("Epic Adventure")
        
        assert story is not None
        assert story.title == "Epic Adventure"
        assert story.story_id is not None
        assert story.contributions == []
        assert story.ai_twists == []
    
    def test_add_contribution(self):
        """Test adding a contribution to a story"""
        genai_service = GenAIService()
        engine = StoryEngine(genai_service)
        
        story = engine.create_story("Test Story")
        contribution = Contribution(
            contribution_id="c1",
            player_id="p1",
            content="Hello",
            contribution_type=ContributionType.WORD,
            turn_number=0
        )
        
        engine.add_contribution(story, contribution)
        
        assert len(story.contributions) == 1
        assert story.contributions[0] == contribution
    
    def test_add_twist(self):
        """Test adding an AI twist to a story"""
        genai_service = GenAIService()
        engine = StoryEngine(genai_service)
        
        story = engine.create_story("Test Story")
        
        twist = engine.add_twist(story, turn_number=3)
        
        assert twist is not None
        assert isinstance(twist, AITwist)
        assert len(story.ai_twists) == 1
        assert story.ai_twists[0] == twist
    
    def test_should_add_twist(self):
        """Test determining when to add twists"""
        genai_service = GenAIService()
        engine = StoryEngine(genai_service)
        
        assert engine.should_add_twist(0) is False
        assert engine.should_add_twist(1) is False
        assert engine.should_add_twist(2) is False
        assert engine.should_add_twist(3) is True
        assert engine.should_add_twist(6) is True
    
    def test_get_story(self):
        """Test getting a story by ID"""
        genai_service = GenAIService()
        engine = StoryEngine(genai_service)
        
        story = engine.create_story("Test Story")
        retrieved = engine.get_story(story.story_id)
        
        assert retrieved == story
        assert retrieved.title == "Test Story"
    
    def test_get_story_text(self):
        """Test getting complete story text"""
        genai_service = GenAIService()
        engine = StoryEngine(genai_service)
        
        story = engine.create_story("Test Story")
        
        contribution1 = Contribution(
            contribution_id="c1",
            player_id="p1",
            content="Once",
            contribution_type=ContributionType.WORD,
            turn_number=0
        )
        contribution2 = Contribution(
            contribution_id="c2",
            player_id="p2",
            content="upon a time",
            contribution_type=ContributionType.PHRASE,
            turn_number=1
        )
        
        engine.add_contribution(story, contribution1)
        engine.add_contribution(story, contribution2)
        
        text = engine.get_story_text(story)
        
        assert "Once" in text
        assert "upon a time" in text
    
    def test_with_mocked_genai_service(self):
        """Test StoryEngine with mocked GenAI service"""
        mock_genai = Mock(spec=GenAIService)
        mock_twist = AITwist(
            twist_id="twist-1",
            content="Mocked twist!",
            applied_after_turn=3
        )
        mock_genai.generate_twist.return_value = mock_twist
        mock_genai.should_add_twist.return_value = True
        
        engine = StoryEngine(mock_genai)
        story = engine.create_story("Test Story")
        
        # Test that engine delegates to mocked service
        twist = engine.add_twist(story, turn_number=3)
        
        assert twist == mock_twist
        assert twist.content == "Mocked twist!"
        mock_genai.generate_twist.assert_called_once_with(story, 3)
