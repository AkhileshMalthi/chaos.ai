"""
chaos.ai Backend - FastAPI Server
Multiplayer group storytelling game with AI-generated twists
"""

import random
import uuid
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(
    title="chaos.ai API",
    description="Multiplayer group storytelling game with AI-generated twists",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for MVP
games: dict = {}
players: dict = {}


# Pydantic models
class CreateGameRequest(BaseModel):
    player_name: str


class JoinGameRequest(BaseModel):
    game_code: str
    player_name: str


class ContributeRequest(BaseModel):
    game_id: str
    player_id: str
    contribution: str


class GameResponse(BaseModel):
    game_id: str
    game_code: str
    player_id: str
    player_name: str


class StoryResponse(BaseModel):
    game_id: str
    story: list
    players: list
    current_turn: Optional[str]
    is_active: bool


# AI Twist Generator (simulated for MVP)
TWIST_TEMPLATES = [
    "Suddenly, {subject} appeared out of nowhere!",
    "But wait... everything was actually a dream... or was it?",
    "A mysterious voice whispered: 'The plot thickens!'",
    "Thunder struck, and {subject} changed forever!",
    "Meanwhile, in a parallel universe, this was happening backwards.",
    "Little did they know, a twist was coming!",
    "The unexpected happened: {subject} revealed a secret!",
    "Chaos ensued when {subject} entered the scene!",
    "Just then, time seemed to freeze for a moment...",
    "And that's when {subject} made everything weird!",
]

SUBJECTS = [
    "a dancing penguin", "a time-traveling toaster", "a philosophical cat",
    "three confused aliens", "a karaoke-loving dragon", "a ninja grandma",
    "a sentient pizza", "a breakdancing robot", "a mysterious stranger",
    "a talking cloud", "a mischievous genie", "a detective banana"
]


def generate_ai_twist() -> str:
    """Generate a random AI twist for the story"""
    template = random.choice(TWIST_TEMPLATES)
    subject = random.choice(SUBJECTS)
    return template.format(subject=subject)


def generate_game_code() -> str:
    """Generate a 6-character game code"""
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(random.choices(chars, k=6))


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Welcome to chaos.ai!", "status": "running"}


@app.post("/api/games/create", response_model=GameResponse)
async def create_game(request: CreateGameRequest):
    """Create a new game session"""
    game_id = str(uuid.uuid4())
    game_code = generate_game_code()
    player_id = str(uuid.uuid4())

    # Create game
    games[game_id] = {
        "id": game_id,
        "code": game_code,
        "story": [],
        "players": [{"id": player_id, "name": request.player_name}],
        "current_turn_index": 0,
        "contribution_count": 0,
        "is_active": True,
        "created_at": datetime.now().isoformat()
    }

    # Track player
    players[player_id] = {"game_id": game_id, "name": request.player_name}

    return GameResponse(
        game_id=game_id,
        game_code=game_code,
        player_id=player_id,
        player_name=request.player_name
    )


@app.post("/api/games/join", response_model=GameResponse)
async def join_game(request: JoinGameRequest):
    """Join an existing game session"""
    # Find game by code
    game = None
    for g in games.values():
        if g["code"] == request.game_code.upper():
            game = g
            break

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if not game["is_active"]:
        raise HTTPException(status_code=400, detail="Game has ended")

    # Check if player name already exists
    for player in game["players"]:
        if player["name"].lower() == request.player_name.lower():
            raise HTTPException(status_code=400, detail="Player name already taken")

    # Add player
    player_id = str(uuid.uuid4())
    game["players"].append({"id": player_id, "name": request.player_name})
    players[player_id] = {"game_id": game["id"], "name": request.player_name}

    return GameResponse(
        game_id=game["id"],
        game_code=game["code"],
        player_id=player_id,
        player_name=request.player_name
    )


@app.get("/api/games/{game_id}", response_model=StoryResponse)
async def get_game(game_id: str):
    """Get current game state and story"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    current_player = None
    if game["players"] and game["is_active"]:
        idx = game["current_turn_index"] % len(game["players"])
        current_player = game["players"][idx]["name"]

    return StoryResponse(
        game_id=game["id"],
        story=game["story"],
        players=[p["name"] for p in game["players"]],
        current_turn=current_player,
        is_active=game["is_active"]
    )


@app.post("/api/games/{game_id}/contribute")
async def contribute_to_story(game_id: str, request: ContributeRequest):
    """Add a contribution to the story"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]

    if not game["is_active"]:
        raise HTTPException(status_code=400, detail="Game has ended")

    # Find player
    player = None
    for p in game["players"]:
        if p["id"] == request.player_id:
            player = p
            break

    if not player:
        raise HTTPException(status_code=403, detail="Player not in this game")

    # Check if it's player's turn
    current_idx = game["current_turn_index"] % len(game["players"])
    if game["players"][current_idx]["id"] != request.player_id:
        raise HTTPException(status_code=400, detail="Not your turn!")

    # Add player contribution
    game["story"].append({
        "type": "player",
        "player_name": player["name"],
        "text": request.contribution,
        "timestamp": datetime.now().isoformat()
    })

    game["contribution_count"] += 1

    # Add AI twist every 3 contributions
    if game["contribution_count"] % 3 == 0:
        twist = generate_ai_twist()
        game["story"].append({
            "type": "ai_twist",
            "player_name": "🤖 Chaos AI",
            "text": twist,
            "timestamp": datetime.now().isoformat()
        })

    # Move to next player
    game["current_turn_index"] += 1

    # Get next player
    next_idx = game["current_turn_index"] % len(game["players"])
    next_player = game["players"][next_idx]["name"]

    return {
        "success": True,
        "story": game["story"],
        "next_turn": next_player
    }


@app.post("/api/games/{game_id}/end")
async def end_game(game_id: str):
    """End the game"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    games[game_id]["is_active"] = False
    return {"success": True, "message": "Game ended"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
