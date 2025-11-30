"""
Tests for chaos.ai Backend API
"""

import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_root():
    """Test health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_create_game():
    """Test game creation"""
    response = client.post(
        "/api/games/create",
        json={"player_name": "TestPlayer"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "game_id" in data
    assert "game_code" in data
    assert "player_id" in data
    assert data["player_name"] == "TestPlayer"
    assert len(data["game_code"]) == 6


def test_join_game():
    """Test joining an existing game"""
    # Create a game first
    create_response = client.post(
        "/api/games/create",
        json={"player_name": "Player1"}
    )
    game_code = create_response.json()["game_code"]
    
    # Join the game
    join_response = client.post(
        "/api/games/join",
        json={"player_name": "Player2", "game_code": game_code}
    )
    assert join_response.status_code == 200
    data = join_response.json()
    assert data["player_name"] == "Player2"
    assert data["game_code"] == game_code


def test_join_nonexistent_game():
    """Test joining a game that doesn't exist"""
    response = client.post(
        "/api/games/join",
        json={"player_name": "TestPlayer", "game_code": "XXXXXX"}
    )
    assert response.status_code == 404


def test_get_game():
    """Test getting game state"""
    # Create a game
    create_response = client.post(
        "/api/games/create",
        json={"player_name": "TestPlayer"}
    )
    game_id = create_response.json()["game_id"]
    
    # Get game state
    response = client.get(f"/api/games/{game_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["game_id"] == game_id
    assert "TestPlayer" in data["players"]
    assert data["is_active"] is True


def test_contribute_to_story():
    """Test adding contribution to story"""
    # Create a game
    create_response = client.post(
        "/api/games/create",
        json={"player_name": "TestPlayer"}
    )
    data = create_response.json()
    game_id = data["game_id"]
    player_id = data["player_id"]
    
    # Add contribution
    response = client.post(
        f"/api/games/{game_id}/contribute",
        json={
            "game_id": game_id,
            "player_id": player_id,
            "contribution": "Once upon a time"
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert result["success"] is True
    assert len(result["story"]) >= 1
    assert result["story"][0]["text"] == "Once upon a time"


def test_contribute_wrong_turn():
    """Test contributing when it's not your turn"""
    # Create a game with player 1
    create_response = client.post(
        "/api/games/create",
        json={"player_name": "Player1"}
    )
    data = create_response.json()
    game_id = data["game_id"]
    game_code = data["game_code"]
    
    # Join with player 2
    join_response = client.post(
        "/api/games/join",
        json={"player_name": "Player2", "game_code": game_code}
    )
    player2_id = join_response.json()["player_id"]
    
    # Player 2 tries to contribute (it's Player 1's turn)
    response = client.post(
        f"/api/games/{game_id}/contribute",
        json={
            "game_id": game_id,
            "player_id": player2_id,
            "contribution": "Test contribution"
        }
    )
    assert response.status_code == 400
    assert "Not your turn" in response.json()["detail"]


def test_ai_twist_generation():
    """Test that AI twist is added every 3 contributions"""
    # Create a game
    create_response = client.post(
        "/api/games/create",
        json={"player_name": "SoloPlayer"}
    )
    data = create_response.json()
    game_id = data["game_id"]
    player_id = data["player_id"]
    
    # Add 3 contributions
    for i in range(3):
        response = client.post(
            f"/api/games/{game_id}/contribute",
            json={
                "game_id": game_id,
                "player_id": player_id,
                "contribution": f"Contribution {i+1}"
            }
        )
        assert response.status_code == 200
    
    # Get game state
    game_response = client.get(f"/api/games/{game_id}")
    story = game_response.json()["story"]
    
    # Should have 4 entries: 3 player + 1 AI twist
    assert len(story) == 4
    assert story[3]["type"] == "ai_twist"
    assert story[3]["player_name"] == "🤖 Chaos AI"
