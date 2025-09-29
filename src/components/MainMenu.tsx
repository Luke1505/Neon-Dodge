'use client';

import React, { useState } from 'react';
import { HighScore } from '@/types/game';

interface MainMenuProps {
  onStartGame: (username: string) => void;
  onShowInstructions: () => void;
  onShowHighScores: () => void;
  username: string;
  highScores: HighScore[];
}

const MainMenu: React.FC<MainMenuProps> = ({
  onStartGame,
  onShowInstructions,
  onShowHighScores,
  username: initialUsername,
  highScores,
}) => {
  const [username, setUsername] = useState(initialUsername || '');

  const handleStartGame = () => {
    onStartGame(username.trim() || 'Guest');
  };

  const topScore = highScores.length > 0 ? highScores[0].score : 0;

  return (
    <div className="flex flex-col items-center justify-center h-full bg-deep-space-black text-white p-8">
      {/* Title */}
      <h1 className="text-6xl font-bold mb-8 neon-glow text-neon-pink animate-pulse-neon">
        NEON DODGE
      </h1>

      {/* Subtitle */}
      <p className="text-xl text-light-text mb-8 text-center">
        Dodge obstacles, collect power-ups, and set high scores!
      </p>

      {/* High Score Display */}
      {topScore > 0 && (
        <div className="mb-6 text-center">
          <p className="text-neon-yellow text-lg">
            High Score: <span className="font-bold">{topScore}</span>
          </p>
        </div>
      )}

      {/* Username Input */}
      <div className="mb-8">
        <label htmlFor="username" className="block text-light-text mb-2">
          Enter Username (optional):
        </label>
        <input
          id="username"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value.slice(0, 12))}
          placeholder="Guest"
          className="px-4 py-2 bg-accent-dark-blue border-2 border-neon-blue rounded text-white placeholder-medium-text focus:outline-none focus:border-neon-cyan transition-colors"
          maxLength={12}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleStartGame();
            }
          }}
        />
      </div>

      {/* Menu Buttons */}
      <div className="space-y-4">
        <button
          onClick={handleStartGame}
          className="neon-button px-8 py-3 rounded text-lg font-semibold transition-all hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue"
        >
          START GAME
        </button>

        <button
          onClick={onShowInstructions}
          className="neon-button px-8 py-3 rounded text-lg font-semibold transition-all hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue"
        >
          INSTRUCTIONS
        </button>

        <button
          onClick={onShowHighScores}
          className="neon-button px-8 py-3 rounded text-lg font-semibold transition-all hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue"
        >
          HIGH SCORES
        </button>
      </div>

      {/* Footer */}
      <div className="mt-8 text-sm text-medium-text text-center">
        <p>Use WASD or Arrow Keys to move</p>
        <p>Press P to pause • Press ESC for menu</p>
      </div>
    </div>
  );
};

export default MainMenu;