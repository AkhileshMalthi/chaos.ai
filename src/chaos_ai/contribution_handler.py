"""
Contribution Handler - Processes player contributions
"""
from .models import Contribution, ContributionType, Player
import uuid


class ContributionHandler:
    """Handles player contributions to the story"""
    
    def __init__(self):
        self._contributions = {}
    
    def create_contribution(
        self, 
        player: Player, 
        content: str, 
        contribution_type: ContributionType,
        turn_number: int
    ) -> Contribution:
        """Create a new contribution"""
        contribution_id = str(uuid.uuid4())
        contribution = Contribution(
            contribution_id=contribution_id,
            player_id=player.player_id,
            content=content,
            contribution_type=contribution_type,
            turn_number=turn_number
        )
        self._contributions[contribution_id] = contribution
        return contribution
    
    def validate_contribution(self, content: str, contribution_type: ContributionType) -> bool:
        """
        Validate a contribution based on its type
        Returns True if valid, False otherwise
        """
        if not content or not content.strip():
            return False
        
        word_count = len(content.split())
        
        if contribution_type == ContributionType.WORD:
            return word_count == 1
        elif contribution_type == ContributionType.PHRASE:
            return 2 <= word_count <= 5
        elif contribution_type == ContributionType.SENTENCE:
            return word_count >= 3
        
        return False
    
    def get_contribution(self, contribution_id: str) -> Contribution:
        """Get a contribution by ID"""
        return self._contributions.get(contribution_id)
