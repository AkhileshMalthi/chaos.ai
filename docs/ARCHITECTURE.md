# chaos.ai Architecture Documentation

## Overview

chaos.ai is a multiplayer group storytelling game where each player contributes one word, phrase, or sentence. A GenAI engine adds wild twists to keep the chaos alive, creating unpredictable, funny, dramatic, and chaotic stories together.

This document describes the Mock-First, Test-Driven Development (TDD) architecture implemented for the prototype.

## Architecture Principles

1. **Mock-First Approach**: All components are designed with clear interfaces that can be mocked for testing
2. **Test-Driven Development**: Comprehensive tests validate component interactions before full implementation
3. **Separation of Concerns**: Each component has a single, well-defined responsibility
4. **Dependency Injection**: Components receive their dependencies through constructors

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GameSessionManager                        │
│  (Orchestrates game flow and coordinates all components)    │
└───────────────┬─────────────┬─────────────┬─────────────────┘
                │             │             │
        ┌───────▼──────┐ ┌───▼──────┐ ┌───▼──────────┐
        │ PlayerManager│ │StoryEngine│ │Contribution  │
        │              │ │           │ │   Handler    │
        └──────────────┘ └─────┬─────┘ └──────────────┘
                               │
                         ┌─────▼──────┐
                         │GenAIService│
                         └────────────┘
```

## Core Components

### 1. GameSessionManager
**Responsibility**: Orchestrates the entire game flow and coordinates all other components.

**Key Methods**:
- `create_session()` - Creates a new game session
- `join_session()` - Adds players to a session
- `start_session()` - Starts the game
- `submit_contribution()` - Processes player contributions
- `end_session()` - Ends the game
- `get_story_text()` - Retrieves the complete story

**Dependencies**: PlayerManager, StoryEngine, ContributionHandler

### 2. PlayerManager
**Responsibility**: Manages player registration, authentication, and tracking.

**Key Methods**:
- `register_player()` - Registers a new player
- `get_player()` - Retrieves player by ID
- `deactivate_player()` - Deactivates a player
- `get_active_players()` - Lists active players
- `player_exists()` - Checks player existence

**Dependencies**: None

### 3. StoryEngine
**Responsibility**: Handles story creation, progression, and AI twist integration.

**Key Methods**:
- `create_story()` - Creates a new story
- `add_contribution()` - Adds a contribution to the story
- `add_twist()` - Generates and adds an AI twist
- `should_add_twist()` - Determines when to add twists
- `get_story_text()` - Returns complete story text

**Dependencies**: GenAIService

### 4. ContributionHandler
**Responsibility**: Processes and validates player contributions.

**Key Methods**:
- `create_contribution()` - Creates a new contribution
- `validate_contribution()` - Validates contribution based on type
- `get_contribution()` - Retrieves contribution by ID

**Validation Rules**:
- **WORD**: Exactly 1 word
- **PHRASE**: 2-5 words
- **SENTENCE**: 3+ words

**Dependencies**: None

### 5. GenAIService
**Responsibility**: Integrates with AI to generate chaotic twists.

**Key Methods**:
- `generate_twist()` - Generates an AI twist based on story context
- `should_add_twist()` - Determines twist timing (currently every 3 turns)

**Current Implementation**: Mock/stub returning predefined twists
**Future Implementation**: Will integrate with actual AI service

**Dependencies**: Optional AI client (for future use)

## Data Models

### Player
```python
@dataclass
class Player:
    player_id: str
    username: str
    joined_at: datetime
    is_active: bool = True
```

### Contribution
```python
@dataclass
class Contribution:
    contribution_id: str
    player_id: str
    content: str
    contribution_type: ContributionType  # WORD, PHRASE, or SENTENCE
    timestamp: datetime
    turn_number: int
```

### AITwist
```python
@dataclass
class AITwist:
    twist_id: str
    content: str
    applied_after_turn: int
    timestamp: datetime
```

### Story
```python
@dataclass
class Story:
    story_id: str
    title: str
    contributions: List[Contribution]
    ai_twists: List[AITwist]
    created_at: datetime
```

### GameSession
```python
@dataclass
class GameSession:
    session_id: str
    story: Story
    players: List[Player]
    status: GameStatus  # WAITING, IN_PROGRESS, COMPLETED, CANCELLED
    current_turn: int
    max_players: int
    min_players: int
    created_at: datetime
```

## Game Flow

1. **Session Creation**
   - GameSessionManager creates a new session with a story
   - Session status: WAITING

2. **Player Registration & Joining**
   - Players register through PlayerManager
   - Players join session via GameSessionManager
   - Minimum players required to start

3. **Game Start**
   - Session transitions to IN_PROGRESS
   - Turn counter starts at 0

4. **Gameplay Loop**
   - Current player determined by: `players[turn % num_players]`
   - Player submits contribution
   - ContributionHandler validates contribution
   - StoryEngine adds contribution to story
   - Every 3 turns, GenAIService adds a twist
   - Turn counter increments

5. **Game End**
   - Session transitions to COMPLETED
   - Final story text available

## Testing Strategy

### Unit Tests
Each component has dedicated unit tests:
- `test_models.py` - Data model tests
- `test_player_manager.py` - Player management tests
- `test_genai_service.py` - AI service tests
- `test_contribution_handler.py` - Contribution validation tests
- `test_story_engine.py` - Story management tests

### Integration Tests
- `test_game_session_manager.py` - Component interaction tests
- `test_integration_flow.py` - End-to-end game flow tests

### Mock Usage
- GenAIService uses mock implementations for twists
- All components can be easily mocked using `unittest.mock`
- Tests validate component interfaces and interactions

## Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=chaos_ai --cov-report=term-missing

# Run specific test file
pytest tests/test_integration_flow.py -v
```

## Future Enhancements

1. **Real AI Integration**
   - Replace mock GenAI service with actual AI API
   - Implement context-aware twist generation
   - Add multiple twist styles (funny, dramatic, chaotic)

2. **Persistence Layer**
   - Add database for storing games and stories
   - Implement game history and replay

3. **Multiplayer Networking**
   - WebSocket server for real-time gameplay
   - REST API for game management

4. **UI/UX**
   - Web frontend for game interface
   - Real-time story display
   - Player avatars and profiles

5. **Game Modes**
   - Different story genres
   - Timed contributions
   - Voting system for best contributions

## Design Decisions

### Why Mock-First?
- Allows testing component interactions before full implementation
- Validates architecture and interfaces early
- Enables parallel development of components
- Makes refactoring safer

### Why Dataclasses?
- Clear, immutable data structures
- Built-in `__repr__` and `__eq__` for testing
- Type hints for better IDE support

### Why Dependency Injection?
- Makes testing easier with mocks
- Loose coupling between components
- Flexible configuration and substitution

## Contributing

When adding new features:
1. Define the interface/contract first
2. Write tests using mocks
3. Implement the component
4. Verify tests pass
5. Update documentation
