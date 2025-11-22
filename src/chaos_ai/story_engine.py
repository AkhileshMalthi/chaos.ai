"""
Story Engine - Handles story creation and flow
"""
from .models import Story, Contribution, AITwist
from .genai_service import GenAIService
import uuid


class StoryEngine:
    """Manages story creation and progression"""
    
    def __init__(self, genai_service: GenAIService):
        self._genai_service = genai_service
        self._stories = {}
    
    def create_story(self, title: str) -> Story:
        """Create a new story"""
        story_id = str(uuid.uuid4())
        story = Story(story_id=story_id, title=title)
        self._stories[story_id] = story
        return story
    
    def add_contribution(self, story: Story, contribution: Contribution) -> None:
        """Add a contribution to the story"""
        story.contributions.append(contribution)
    
    def add_twist(self, story: Story, turn_number: int) -> AITwist:
        """Generate and add an AI twist to the story"""
        twist = self._genai_service.generate_twist(story, turn_number)
        story.ai_twists.append(twist)
        return twist
    
    def should_add_twist(self, turn_number: int) -> bool:
        """Check if a twist should be added at this turn"""
        return self._genai_service.should_add_twist(turn_number)
    
    def get_story(self, story_id: str) -> Story:
        """Get a story by ID"""
        return self._stories.get(story_id)
    
    def get_story_text(self, story: Story) -> str:
        """Get the complete story text"""
        return story.get_full_text()
