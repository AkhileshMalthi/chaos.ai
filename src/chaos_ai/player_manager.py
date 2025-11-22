"""
Player Manager - Handles player registration and management
"""
from typing import Dict, Optional
from .models import Player
import uuid


class PlayerManager:
    """Manages player registration, authentication, and tracking"""
    
    def __init__(self):
        self._players: Dict[str, Player] = {}
    
    def register_player(self, username: str) -> Player:
        """Register a new player"""
        player_id = str(uuid.uuid4())
        player = Player(player_id=player_id, username=username)
        self._players[player_id] = player
        return player
    
    def get_player(self, player_id: str) -> Optional[Player]:
        """Get a player by ID"""
        return self._players.get(player_id)
    
    def deactivate_player(self, player_id: str) -> bool:
        """Deactivate a player"""
        player = self._players.get(player_id)
        if player:
            player.is_active = False
            return True
        return False
    
    def get_active_players(self) -> list:
        """Get all active players"""
        return [p for p in self._players.values() if p.is_active]
    
    def player_exists(self, player_id: str) -> bool:
        """Check if a player exists"""
        return player_id in self._players
