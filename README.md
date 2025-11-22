# chaos.ai

Multiplayer group storytelling game where each player contributes one word, phrase, or sentence. A GenAI engine adds wild twists to keep the chaos alive. The goal is to create unpredictable, funny, dramatic, and chaotic stories together.

## 🎯 Status: Mock-First TDD Prototype

This repository implements a **fully functional prototype** using Mock-First, Test-Driven Development (TDD). All components have been designed, implemented, and thoroughly tested with 95% code coverage.

## ✨ Features

- **Multiplayer Support**: 2-6 players per game session
- **Three Contribution Types**: Word, Phrase, or Sentence
- **AI-Powered Twists**: Automatic story twists every 3 turns (currently mocked)
- **Turn-Based Gameplay**: Fair rotation system for all players
- **Validation System**: Ensures contributions match their declared type
- **Complete Test Suite**: 49 tests demonstrating all functionality

## 🏗️ Architecture

The system is built with five core components:

1. **GameSessionManager** - Orchestrates game flow
2. **PlayerManager** - Handles player registration
3. **StoryEngine** - Manages story creation and progression
4. **ContributionHandler** - Validates and processes contributions
5. **GenAIService** - Generates story twists (currently mocked)

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed documentation.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/AkhileshMalthi/chaos.ai.git
cd chaos.ai

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run with verbose output
pytest -v

# Run integration tests to see the prototype in action
pytest tests/test_integration_flow.py::TestPrototypeFlow::test_complete_game_flow -v -s
```

### Example Output

```
✓ Game session created: The Epic Space Adventure
✓ Players registered: Alice, Bob, Charlie
✓ Game started!

Turn 0 (Alice): Once
Turn 1 (Bob): upon a time
Turn 2 (Charlie): there was a brave astronaut
Turn 3 (Alice): who discovered
🎭 AI Twist: A mysterious portal opened, revealing an upside-down world!
Turn 4 (Bob): a mysterious planet
Turn 5 (Charlie): filled with strange creatures

Complete Story: Once upon a time there was a brave astronaut who discovered a mysterious planet filled with strange creatures...
```

## 📖 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - Detailed system design and component interactions
- [Usage Guide](docs/USAGE.md) - How to use the prototype and API examples

## 🧪 Testing

The project uses a comprehensive Mock-First TDD approach:

- **Unit Tests**: Each component tested individually
- **Integration Tests**: Full game flow validation
- **Mock Testing**: Demonstrates component interactions
- **95% Code Coverage**: Thoroughly validated

Run tests:
```bash
pytest                           # All tests
pytest -v                        # Verbose output
pytest --cov=chaos_ai            # With coverage report
```

## 🎮 Game Rules

1. **Players**: 2-6 players per session
2. **Contributions**:
   - **Word**: Exactly 1 word
   - **Phrase**: 2-5 words
   - **Sentence**: 3+ words
3. **Turns**: Players rotate in order they joined
4. **AI Twists**: Added every 3 turns automatically

## 🔮 Future Enhancements

- [ ] Real AI integration (OpenAI, Anthropic, etc.)
- [ ] WebSocket server for real-time multiplayer
- [ ] Web UI for game interface
- [ ] Database persistence for game history
- [ ] Multiple story genres and game modes
- [ ] Voting system for best contributions

## 🤝 Contributing

This is a Mock-First TDD project. To contribute:

1. Define the interface/contract
2. Write tests using mocks
3. Implement the feature
4. Ensure all tests pass
5. Update documentation

## 📝 License

See [LICENSE](LICENSE) file for details.
