"""
GenAI Service - Integrates with AI to generate chaotic twists
"""
from .models import AITwist, Story
import uuid


class GenAIService:
    """Handles AI-generated twists for stories"""
    
    def __init__(self, ai_client=None):
        """
        Initialize with optional AI client
        For mock/prototype, ai_client is None and we use stub responses
        """
        self._ai_client = ai_client
    
    def generate_twist(self, story: Story, turn_number: int) -> AITwist:
        """
        Generate an AI twist based on the current story
        In prototype mode, returns a mock twist
        """
        twist_id = str(uuid.uuid4())
        
        # Mock implementation - returns predefined twist
        # Real implementation would call AI service
        mock_twists = [
            "Suddenly, a purple dragon appeared from the clouds!",
            "But then, everything turned into cheese!",
            "Without warning, the characters swapped personalities!",
            "A mysterious portal opened, revealing an upside-down world!",
            "Time started flowing backwards for everyone!",
        ]
        
        twist_content = mock_twists[turn_number % len(mock_twists)]
        
        return AITwist(
            twist_id=twist_id,
            content=twist_content,
            applied_after_turn=turn_number
        )
    
    def should_add_twist(self, turn_number: int) -> bool:
        """
        Determine if a twist should be added at this turn
        Currently adds twist every 3 turns
        """
        return turn_number > 0 and turn_number % 3 == 0
