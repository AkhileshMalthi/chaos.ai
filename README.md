# 🌪️ chaos.ai

Multiplayer group storytelling game. Each player contributes one word, phrase, or sentence. GenAI engine adds wild twists to keep the chaos alive. Goal: create unpredictable, funny, dramatic, and chaotic stories together.

## 🎮 How to Play

1. **Create a Game**: One player creates a game and shares the 6-character game code with friends
2. **Join the Game**: Friends join using the game code
3. **Take Turns**: Players take turns adding words, phrases, or sentences to the story
4. **Watch the Chaos**: Every few contributions, the AI throws in a wild twist!
5. **Enjoy**: Create unpredictable, hilarious, and chaotic stories together!

## 🛠️ Tech Stack

- **Frontend**: React.js with modern hooks and CSS
- **Backend**: FastAPI (Python) with in-memory storage for MVP

## 🚀 Getting Started

### Prerequisites

- Node.js 16+ and npm
- Python 3.9+

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The API server runs at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The app runs at `http://localhost:3000`

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/games/create` | Create a new game |
| POST | `/api/games/join` | Join an existing game |
| GET | `/api/games/{game_id}` | Get game state and story |
| POST | `/api/games/{game_id}/contribute` | Add to the story |
| POST | `/api/games/{game_id}/end` | End the game |

## 🧪 Running Tests

### Backend Tests
```bash
cd backend
python -m pytest test_main.py -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📁 Project Structure

```
chaos.ai/
├── backend/
│   ├── main.py           # FastAPI server
│   ├── requirements.txt  # Python dependencies
│   └── test_main.py      # Backend tests
├── frontend/
│   ├── public/           # Static assets
│   ├── src/
│   │   ├── App.js        # Main React component
│   │   ├── App.css       # Styles
│   │   └── App.test.js   # Frontend tests
│   └── package.json      # Node dependencies
├── LICENSE
└── README.md
```

## 🔮 Future Enhancements

- Real-time updates with WebSockets
- Persistent game storage with database
- OpenAI/LLM integration for smarter AI twists
- User authentication and game history
- Share and export completed stories
- Mobile-responsive design improvements

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

