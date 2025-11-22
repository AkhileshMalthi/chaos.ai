"""
Data models for the chaos.ai game
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class GameStatus(Enum):
    """Game session status"""
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ContributionType(Enum):
    """Type of player contribution"""
    WORD = "word"
    PHRASE = "phrase"
    SENTENCE = "sentence"


@dataclass
class Player:
    """Represents a player in the game"""
    player_id: str
    username: str
    joined_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    
    def __hash__(self):
        return hash(self.player_id)


@dataclass
class Contribution:
    """Represents a player's contribution to the story"""
    contribution_id: str
    player_id: str
    content: str
    contribution_type: ContributionType
    timestamp: datetime = field(default_factory=datetime.now)
    turn_number: int = 0


@dataclass
class AITwist:
    """Represents an AI-generated twist in the story"""
    twist_id: str
    content: str
    applied_after_turn: int
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Story:
    """Represents the complete story being created"""
    story_id: str
    title: str
    contributions: List[Contribution] = field(default_factory=list)
    ai_twists: List[AITwist] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def get_full_text(self) -> str:
        """Get the complete story text"""
        parts = []
        for contribution in self.contributions:
            parts.append(contribution.content)
        for twist in self.ai_twists:
            parts.append(twist.content)
        return " ".join(parts)


@dataclass
class GameSession:
    """Represents an active game session"""
    session_id: str
    story: Story
    players: List[Player] = field(default_factory=list)
    status: GameStatus = GameStatus.WAITING
    current_turn: int = 0
    max_players: int = 6
    min_players: int = 2
    created_at: datetime = field(default_factory=datetime.now)
    
    def is_ready_to_start(self) -> bool:
        """Check if session has enough players to start"""
        return len(self.players) >= self.min_players
    
    def is_full(self) -> bool:
        """Check if session has reached max players"""
        return len(self.players) >= self.max_players
    
    def get_current_player(self) -> Optional[Player]:
        """Get the player whose turn it is"""
        if not self.players:
            return None
        player_index = self.current_turn % len(self.players)
        return self.players[player_index]
