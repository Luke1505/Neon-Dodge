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
    <div className="flex flex-col items-center justify-center h-full bg-gradient-to-br from-deep-space-black via-purple-900/20 to-deep-space-black text-white p-8 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-10 left-10 w-2 h-2 bg-neon-blue rounded-full animate-pulse"></div>
        <div className="absolute top-20 right-20 w-1 h-1 bg-neon-pink rounded-full animate-pulse delay-1000"></div>
        <div className="absolute bottom-20 left-20 w-1.5 h-1.5 bg-neon-green rounded-full animate-pulse delay-2000"></div>
        <div className="absolute bottom-10 right-10 w-1 h-1 bg-neon-yellow rounded-full animate-pulse delay-3000"></div>
        <div className="absolute top-1/2 left-5 w-1 h-1 bg-neon-cyan rounded-full animate-pulse delay-500"></div>
        <div className="absolute top-1/3 right-5 w-1.5 h-1.5 bg-neon-purple rounded-full animate-pulse delay-1500"></div>
      </div>

      {/* Main content */}
      <div className="z-10 w-full max-w-md mx-auto slide-in">
        {/* Title with enhanced styling */}
        <div className="text-center mb-8">
          <h1 className="game-title text-6xl font-black mb-4 neon-glow text-neon-pink pulse-neon bg-gradient-to-r from-neon-pink via-neon-purple to-neon-cyan bg-clip-text text-transparent">
            NEON DODGE
          </h1>
          <div className="h-1 w-32 mx-auto bg-gradient-to-r from-transparent via-neon-blue to-transparent rounded-full glow-pulse"></div>
        </div>

        {/* Subtitle with professional styling */}
        <p className="text-xl text-light-text mb-8 text-center font-medium tracking-wide">
          Dodge obstacles, collect power-ups, and set high scores in this 
          <span className="text-neon-cyan font-semibold"> neon-futuristic</span> adventure!
        </p>

        {/* High Score Display with enhanced styling */}
        {topScore > 0 && (
          <div className="mb-8 text-center">
            <div className="inline-block bg-gradient-to-r from-neon-yellow/20 to-neon-orange/20 border-2 border-neon-yellow rounded-lg p-4 neon-border">
              <p className="text-neon-yellow text-lg font-semibold">
                🏆 High Score
              </p>
              <p className="text-3xl font-bold text-neon-orange glow-pulse">
                {topScore.toLocaleString()}
              </p>
            </div>
          </div>
        )}

        {/* Username Input with enhanced styling */}
        <div className="mb-8">
          <label htmlFor="username" className="block text-light-text mb-3 font-medium tracking-wide">
            Enter Username (optional):
          </label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value.slice(0, 12))}
            placeholder="Anonymous Player"
            className="w-full px-4 py-3 neon-input rounded-lg font-medium placeholder-medium-text transition-all duration-300"
            maxLength={12}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleStartGame();
              }
            }}
          />
        </div>

        {/* Menu Buttons with enhanced styling */}
        <div className="space-y-4">
          <button
            onClick={handleStartGame}
            className="w-full neon-button px-8 py-4 rounded-lg text-lg font-bold transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue gpu-accelerated group"
          >
            <span className="flex items-center justify-center">
              <span className="mr-2">🚀</span>
              START GAME
              <span className="ml-2 group-hover:translate-x-1 transition-transform duration-300">▶</span>
            </span>
          </button>

          <button
            onClick={onShowInstructions}
            className="w-full neon-button px-8 py-4 rounded-lg text-lg font-bold transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue gpu-accelerated"
          >
            <span className="flex items-center justify-center">
              <span className="mr-2">📖</span>
              INSTRUCTIONS
            </span>
          </button>

          <button
            onClick={onShowHighScores}
            className="w-full neon-button px-8 py-4 rounded-lg text-lg font-bold transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue gpu-accelerated"
          >
            <span className="flex items-center justify-center">
              <span className="mr-2">🏆</span>
              HIGH SCORES
            </span>
          </button>
        </div>

        {/* Footer with enhanced styling */}
        <div className="mt-8 text-center space-y-2">
          <div className="text-sm text-medium-text font-medium">
            <p className="flex items-center justify-center">
              <span className="mr-2">⌨️</span>
              Use WASD or Arrow Keys to move
            </p>
            <p className="flex items-center justify-center mt-1">
              <span className="mr-2">⏸️</span>
              Press P to pause • Press ESC for menu
            </p>
          </div>
          <div className="text-xs text-dark-gray mt-4 font-medium tracking-wider">
            v1.0.0 • Built with ❤️ and neon lights
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainMenu;