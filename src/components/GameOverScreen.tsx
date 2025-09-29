'use client';

import React from 'react';
import { HighScore } from '@/types/game';

interface GameOverScreenProps {
  score: number;
  maxCombo: number;
  username: string;
  onPlayAgain: () => void;
  onMainMenu: () => void;
  highScores: HighScore[];
}

const GameOverScreen: React.FC<GameOverScreenProps> = ({
  score,
  maxCombo,
  username,
  onPlayAgain,
  onMainMenu,
  highScores,
}) => {
  const isNewHighScore = highScores.length === 0 || score > highScores[highScores.length - 1]?.score;
  const ranking = highScores.findIndex(hs => hs.score <= score) + 1;

  return (
    <div className="flex flex-col items-center justify-center h-full bg-deep-space-black text-white p-8">
      <h1 className="text-5xl font-bold mb-6 text-neon-red animate-pulse">
        GAME OVER
      </h1>

      <div className="bg-accent-dark-blue/50 border-2 border-neon-blue rounded-lg p-6 mb-8 text-center min-w-80">
        <h2 className="text-2xl font-bold text-neon-cyan mb-4">{username}</h2>
        
        <div className="space-y-2 text-lg">
          <div className="text-neon-yellow">
            Final Score: <span className="font-bold">{score}</span>
          </div>
          
          {maxCombo > 0 && (
            <div className="text-neon-orange">
              Best Combo: <span className="font-bold">{maxCombo}x</span>
            </div>
          )}
          
          {isNewHighScore && ranking <= 10 && (
            <div className="text-neon-green font-bold animate-bounce mt-4">
              🎉 NEW HIGH SCORE! 🎉
              {ranking <= 3 && <div className="text-sm">#{ranking} on the leaderboard!</div>}
            </div>
          )}
        </div>
      </div>

      {/* High Scores Preview */}
      {highScores.length > 0 && (
        <div className="bg-accent-dark-blue/30 border border-neon-purple rounded-lg p-4 mb-6 w-full max-w-md">
          <h3 className="text-xl font-bold text-neon-purple mb-3 text-center">Top Scores</h3>
          <div className="space-y-1 text-sm">
            {highScores.slice(0, 5).map((hs, index) => (
              <div 
                key={index} 
                className={`flex justify-between ${
                  hs.username === username && hs.score === score 
                    ? 'text-neon-yellow font-bold' 
                    : 'text-light-text'
                }`}
              >
                <span>#{index + 1} {hs.username}</span>
                <span>{hs.score}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="space-y-4">
        <button
          onClick={onPlayAgain}
          className="neon-button px-8 py-3 rounded text-lg font-semibold transition-all hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue"
        >
          PLAY AGAIN
        </button>
        
        <button
          onClick={onMainMenu}
          className="neon-button px-8 py-3 rounded text-lg font-semibold transition-all hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue"
        >
          MAIN MENU
        </button>
      </div>

      <div className="mt-6 text-sm text-medium-text text-center">
        <p>Thanks for playing Neon Dodge!</p>
        <p>Challenge your friends to beat your score!</p>
      </div>
    </div>
  );
};

export default GameOverScreen;