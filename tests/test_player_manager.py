"""
Tests for PlayerManager
"""
import pytest
from chaos_ai.player_manager import PlayerManager
from chaos_ai.models import Player


class TestPlayerManager:
    """Tests for PlayerManager component"""
    
    def test_register_player(self):
        """Test registering a new player"""
        manager = PlayerManager()
        
        player = manager.register_player("testuser")
        
        assert player is not None
        assert player.username == "testuser"
        assert player.player_id is not None
        assert player.is_active is True
    
    def test_get_player(self):
        """Test getting a player by ID"""
        manager = PlayerManager()
        
        player = manager.register_player("testuser")
        retrieved_player = manager.get_player(player.player_id)
        
        assert retrieved_player == player
        assert retrieved_player.username == "testuser"
    
    def test_get_nonexistent_player(self):
        """Test getting a player that doesn't exist"""
        manager = PlayerManager()
        
        player = manager.get_player("nonexistent-id")
        
        assert player is None
    
    def test_deactivate_player(self):
        """Test deactivating a player"""
        manager = PlayerManager()
        
        player = manager.register_player("testuser")
        assert player.is_active is True
        
        result = manager.deactivate_player(player.player_id)
        
        assert result is True
        assert player.is_active is False
    
    def test_deactivate_nonexistent_player(self):
        """Test deactivating a player that doesn't exist"""
        manager = PlayerManager()
        
        result = manager.deactivate_player("nonexistent-id")
        
        assert result is False
    
    def test_get_active_players(self):
        """Test getting all active players"""
        manager = PlayerManager()
        
        player1 = manager.register_player("user1")
        player2 = manager.register_player("user2")
        player3 = manager.register_player("user3")
        
        manager.deactivate_player(player2.player_id)
        
        active_players = manager.get_active_players()
        
        assert len(active_players) == 2
        assert player1 in active_players
        assert player2 not in active_players
        assert player3 in active_players
    
    def test_player_exists(self):
        """Test checking if a player exists"""
        manager = PlayerManager()
        
        player = manager.register_player("testuser")
        
        assert manager.player_exists(player.player_id) is True
        assert manager.player_exists("nonexistent-id") is False
