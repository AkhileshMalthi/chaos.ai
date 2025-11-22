# chaos.ai Usage Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/AkhileshMalthi/chaos.ai.git
cd chaos.ai

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=chaos_ai --cov-report=term-missing

# Run specific test file
pytest tests/test_integration_flow.py -v

# Run a specific test
pytest tests/test_integration_flow.py::TestPrototypeFlow::test_complete_game_flow -v
```

## Using the Prototype

### Basic Game Setup

```python
from chaos_ai.game_session_manager import GameSessionManager
from chaos_ai.player_manager import PlayerManager
from chaos_ai.story_engine import StoryEngine
from chaos_ai.contribution_handler import ContributionHandler
from chaos_ai.genai_service import GenAIService
from chaos_ai.models import ContributionType

# Initialize all components
player_manager = PlayerManager()
genai_service = GenAIService()
story_engine = StoryEngine(genai_service)
contribution_handler = ContributionHandler()
game_manager = GameSessionManager(
    player_manager=player_manager,
    story_engine=story_engine,
    contribution_handler=contribution_handler
)

# Create a game session
session = game_manager.create_session(
    title="The Epic Space Adventure",
    max_players=6,
    min_players=2
)

# Register players
player1 = player_manager.register_player("Alice")
player2 = player_manager.register_player("Bob")
player3 = player_manager.register_player("Charlie")

# Players join the session
game_manager.join_session(session.session_id, player1)
game_manager.join_session(session.session_id, player2)
game_manager.join_session(session.session_id, player3)

# Start the game
game_manager.start_session(session.session_id)

# Players take turns
game_manager.submit_contribution(
    session_id=session.session_id,
    player_id=player1.player_id,
    content="Once",
    contribution_type=ContributionType.WORD
)

game_manager.submit_contribution(
    session_id=session.session_id,
    player_id=player2.player_id,
    content="upon a time",
    contribution_type=ContributionType.PHRASE
)

game_manager.submit_contribution(
    session_id=session.session_id,
    player_id=player3.player_id,
    content="there was a brave astronaut",
    contribution_type=ContributionType.SENTENCE
)

# Get the story text
story_text = game_manager.get_story_text(session.session_id)
print(f"Story so far: {story_text}")

# End the game
game_manager.end_session(session.session_id)
```

## Contribution Types

### WORD
- Exactly 1 word
- Example: `"Hello"`, `"Dragon"`, `"Suddenly"`

### PHRASE
- 2-5 words
- Example: `"once upon a time"`, `"in the forest"`, `"with great power"`

### SENTENCE
- 3 or more words
- Example: `"The hero discovered a secret."`, `"Everything turned upside down."`

## Game Rules

1. **Minimum Players**: 2 (configurable)
2. **Maximum Players**: 6 (configurable)
3. **Turn Order**: Players take turns in the order they joined
4. **AI Twists**: Automatically added every 3 turns
5. **Validation**: Contributions must match their declared type

## Example Game Session

See the complete example in `tests/test_integration_flow.py::test_complete_game_flow`

This test demonstrates:
- Creating a game session
- Registering multiple players
- Players joining and starting the game
- Multiple turns with different contribution types
- AI twists being added automatically
- Getting the complete story
- Ending the game

## Mock AI Twists

The current prototype uses predefined AI twists that cycle through:

1. "Suddenly, a purple dragon appeared from the clouds!"
2. "But then, everything turned into cheese!"
3. "Without warning, the characters swapped personalities!"
4. "A mysterious portal opened, revealing an upside-down world!"
5. "Time started flowing backwards for everyone!"

These will be replaced with real AI-generated content in the production version.

## Error Handling

### Invalid Turn
If a player tries to contribute when it's not their turn:
```python
result = game_manager.submit_contribution(...)
# result will be None
```

### Invalid Contribution
If a contribution doesn't match its type:
```python
result = game_manager.submit_contribution(
    session_id=session.session_id,
    player_id=player_id,
    content="Too many words",  # Multiple words
    contribution_type=ContributionType.WORD  # But marked as WORD
)
# result will be None
```

### Session Full
If a session has reached maximum players:
```python
result = game_manager.join_session(session_id, player)
# result will be False
```

### Not Enough Players
If trying to start without minimum players:
```python
result = game_manager.start_session(session_id)
# result will be False
```

## Development Workflow

### Adding New Features

1. **Define the Interface**
   - Add methods to relevant component
   - Update data models if needed

2. **Write Tests**
   - Create test file or add to existing
   - Write tests using mocks
   - Run tests (they should fail)

3. **Implement Feature**
   - Add implementation
   - Run tests until they pass

4. **Update Documentation**
   - Update ARCHITECTURE.md
   - Update USAGE.md
   - Add code examples

### Testing with Mocks

```python
from unittest.mock import Mock
from chaos_ai.story_engine import StoryEngine
from chaos_ai.models import AITwist

# Create a mock GenAI service
mock_genai = Mock()
mock_twist = AITwist(
    twist_id="test-twist",
    content="Custom test twist!",
    applied_after_turn=3
)
mock_genai.generate_twist.return_value = mock_twist

# Use mock in tests
engine = StoryEngine(mock_genai)
story = engine.create_story("Test")
twist = engine.add_twist(story, turn_number=3)

# Verify mock was called
mock_genai.generate_twist.assert_called_once_with(story, 3)
```

## Troubleshooting

### Tests Fail with Import Errors
```bash
# Ensure package is installed
pip install -e .
```

### Coverage Not Working
```bash
# Install coverage dependencies
pip install pytest-cov
```

### Type Checking
```bash
# Install mypy (optional)
pip install -r requirements-dev.txt
mypy src/chaos_ai
```

## Next Steps

1. Run the test suite to see the prototype in action
2. Review the architecture documentation
3. Try creating your own game scenario
4. Contribute new features or improvements
