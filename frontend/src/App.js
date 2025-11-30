import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [screen, setScreen] = useState('home'); // home, game
  const [playerName, setPlayerName] = useState('');
  const [gameCode, setGameCode] = useState('');
  const [gameData, setGameData] = useState(null);
  const [story, setStory] = useState([]);
  const [players, setPlayers] = useState([]);
  const [currentTurn, setCurrentTurn] = useState('');
  const [contribution, setContribution] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const storyEndRef = useRef(null);

  // Scroll to bottom of story when updated
  useEffect(() => {
    if (storyEndRef.current) {
      storyEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [story]);

  // Poll for game updates
  useEffect(() => {
    let interval;
    if (gameData && screen === 'game') {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`${API_URL}/api/games/${gameData.game_id}`);
          if (res.ok) {
            const data = await res.json();
            setStory(data.story);
            setPlayers(data.players);
            setCurrentTurn(data.current_turn);
          }
        } catch (err) {
          console.error('Failed to fetch game state:', err);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [gameData, screen]);

  const createGame = async () => {
    if (!playerName.trim()) {
      setError('Please enter your name');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_URL}/api/games/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_name: playerName.trim() })
      });
      if (!res.ok) throw new Error('Failed to create game');
      const data = await res.json();
      setGameData(data);
      setScreen('game');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const joinGame = async () => {
    if (!playerName.trim()) {
      setError('Please enter your name');
      return;
    }
    if (!gameCode.trim()) {
      setError('Please enter a game code');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_URL}/api/games/join`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          player_name: playerName.trim(),
          game_code: gameCode.trim().toUpperCase()
        })
      });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Failed to join game');
      }
      const data = await res.json();
      setGameData(data);
      setScreen('game');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const submitContribution = async () => {
    if (!contribution.trim()) {
      setError('Please enter something for the story');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_URL}/api/games/${gameData.game_id}/contribute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          game_id: gameData.game_id,
          player_id: gameData.player_id,
          contribution: contribution.trim()
        })
      });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Failed to add contribution');
      }
      const data = await res.json();
      setStory(data.story);
      setCurrentTurn(data.next_turn);
      setContribution('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const leaveGame = () => {
    setScreen('home');
    setGameData(null);
    setStory([]);
    setPlayers([]);
    setCurrentTurn('');
    setContribution('');
    setError('');
  };

  const isMyTurn = currentTurn === gameData?.player_name;

  if (screen === 'home') {
    return (
      <div className="App">
        <div className="home-container">
          <h1 className="title">🌪️ chaos.ai</h1>
          <p className="subtitle">Multiplayer Chaotic Storytelling</p>
          
          <div className="form-section">
            <input
              type="text"
              placeholder="Enter your name"
              value={playerName}
              onChange={(e) => setPlayerName(e.target.value)}
              className="input"
              maxLength={20}
            />
            
            <button 
              onClick={createGame} 
              disabled={loading}
              className="btn btn-primary"
            >
              {loading ? 'Creating...' : '✨ Create New Game'}
            </button>
            
            <div className="divider">
              <span>or join existing game</span>
            </div>
            
            <input
              type="text"
              placeholder="Enter game code"
              value={gameCode}
              onChange={(e) => setGameCode(e.target.value.toUpperCase())}
              className="input"
              maxLength={6}
            />
            
            <button 
              onClick={joinGame} 
              disabled={loading}
              className="btn btn-secondary"
            >
              {loading ? 'Joining...' : '🎮 Join Game'}
            </button>
            
            {error && <p className="error">{error}</p>}
          </div>
          
          <div className="how-to-play">
            <h3>How to Play</h3>
            <ul>
              <li>Create or join a game with friends</li>
              <li>Take turns adding words, phrases, or sentences</li>
              <li>Watch as AI adds wild twists to the story!</li>
              <li>Create the most chaotic story together!</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <div className="game-container">
        <div className="game-header">
          <div className="game-info">
            <h2>🌪️ chaos.ai</h2>
            <div className="game-code">
              Game Code: <span>{gameData?.game_code}</span>
            </div>
          </div>
          <button onClick={leaveGame} className="btn btn-small">Leave Game</button>
        </div>
        
        <div className="players-bar">
          <span className="players-label">Players:</span>
          {players.map((player, idx) => (
            <span 
              key={idx} 
              className={`player-badge ${player === currentTurn ? 'active' : ''} ${player === gameData?.player_name ? 'me' : ''}`}
            >
              {player === gameData?.player_name ? `${player} (You)` : player}
            </span>
          ))}
        </div>
        
        <div className="story-container">
          <h3>📖 The Story So Far...</h3>
          <div className="story-content">
            {story.length === 0 ? (
              <p className="empty-story">The story is empty. Start writing!</p>
            ) : (
              story.map((entry, idx) => (
                <div key={idx} className={`story-entry ${entry.type}`}>
                  <span className="author">{entry.player_name}:</span>
                  <span className="text">{entry.text}</span>
                </div>
              ))
            )}
            <div ref={storyEndRef} />
          </div>
        </div>
        
        <div className="contribution-section">
          <div className="turn-indicator">
            {isMyTurn ? (
              <span className="your-turn">✨ It's your turn!</span>
            ) : (
              <span className="waiting">Waiting for {currentTurn}...</span>
            )}
          </div>
          
          <div className="input-row">
            <input
              type="text"
              placeholder={isMyTurn ? "Add to the story..." : "Wait for your turn..."}
              value={contribution}
              onChange={(e) => setContribution(e.target.value)}
              className="input contribution-input"
              disabled={!isMyTurn || loading}
              onKeyPress={(e) => e.key === 'Enter' && isMyTurn && submitContribution()}
              maxLength={200}
            />
            <button 
              onClick={submitContribution}
              disabled={!isMyTurn || loading || !contribution.trim()}
              className="btn btn-primary"
            >
              {loading ? '...' : 'Add ✨'}
            </button>
          </div>
          
          {error && <p className="error">{error}</p>}
        </div>
      </div>
    </div>
  );
}

export default App;
