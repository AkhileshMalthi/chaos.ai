"""
Game Session Manager - Manages game sessions and game flow
"""
from typing import Dict, Optional, List
from .models import GameSession, Player, GameStatus, Story, Contribution, ContributionType
from .player_manager import PlayerManager
from .story_engine import StoryEngine
from .contribution_handler import ContributionHandler
import uuid


class GameSessionManager:
    """Manages game sessions, players, and game state"""
    
    def __init__(
        self, 
        player_manager: PlayerManager,
        story_engine: StoryEngine,
        contribution_handler: ContributionHandler
    ):
        self._player_manager = player_manager
        self._story_engine = story_engine
        self._contribution_handler = contribution_handler
        self._sessions: Dict[str, GameSession] = {}
    
    def create_session(
        self, 
        title: str, 
        max_players: int = 6, 
        min_players: int = 2
    ) -> GameSession:
        """Create a new game session"""
        session_id = str(uuid.uuid4())
        story = self._story_engine.create_story(title)
        
        session = GameSession(
            session_id=session_id,
            story=story,
            max_players=max_players,
            min_players=min_players
        )
        
        self._sessions[session_id] = session
        return session
    
    def join_session(self, session_id: str, player: Player) -> bool:
        """Add a player to a game session"""
        session = self._sessions.get(session_id)
        
        if not session:
            return False
        
        if session.is_full():
            return False
        
        if session.status != GameStatus.WAITING:
            return False
        
        if player not in session.players:
            session.players.append(player)
        
        return True
    
    def start_session(self, session_id: str) -> bool:
        """Start a game session"""
        session = self._sessions.get(session_id)
        
        if not session:
            return False
        
        if not session.is_ready_to_start():
            return False
        
        if session.status != GameStatus.WAITING:
            return False
        
        session.status = GameStatus.IN_PROGRESS
        return True
    
    def submit_contribution(
        self, 
        session_id: str, 
        player_id: str, 
        content: str,
        contribution_type: ContributionType
    ) -> Optional[Contribution]:
        """Submit a player's contribution"""
        session = self._sessions.get(session_id)
        
        if not session or session.status != GameStatus.IN_PROGRESS:
            return None
        
        current_player = session.get_current_player()
        if not current_player or current_player.player_id != player_id:
            return None
        
        # Validate contribution
        if not self._contribution_handler.validate_contribution(content, contribution_type):
            return None
        
        # Create contribution
        contribution = self._contribution_handler.create_contribution(
            player=current_player,
            content=content,
            contribution_type=contribution_type,
            turn_number=session.current_turn
        )
        
        # Add to story
        self._story_engine.add_contribution(session.story, contribution)
        
        # Check if AI twist should be added
        if self._story_engine.should_add_twist(session.current_turn):
            self._story_engine.add_twist(session.story, session.current_turn)
        
        # Advance turn
        session.current_turn += 1
        
        return contribution
    
    def get_session(self, session_id: str) -> Optional[GameSession]:
        """Get a game session by ID"""
        return self._sessions.get(session_id)
    
    def end_session(self, session_id: str) -> bool:
        """End a game session"""
        session = self._sessions.get(session_id)
        
        if not session:
            return False
        
        session.status = GameStatus.COMPLETED
        return True
    
    def get_story_text(self, session_id: str) -> Optional[str]:
        """Get the complete story text for a session"""
        session = self._sessions.get(session_id)
        
        if not session:
            return None
        
        return self._story_engine.get_story_text(session.story)
