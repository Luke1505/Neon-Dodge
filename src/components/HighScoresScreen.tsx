'use client';

import React from 'react';
import { HighScore } from '@/types/game';

interface HighScoresScreenProps {
  highScores: HighScore[];
  onBack: () => void;
  onClearScores: () => void;
}

const HighScoresScreen: React.FC<HighScoresScreenProps> = ({ 
  highScores, 
  onBack, 
  onClearScores 
}) => {
  const formatDate = (timestamp?: number) => {
    if (!timestamp) return 'Unknown';
    return new Date(timestamp).toLocaleDateString();
  };

  const getRankEmoji = (rank: number) => {
    switch (rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return '🏅';
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-full bg-deep-space-black text-white p-8 overflow-y-auto">
      <h1 className="text-4xl font-bold mb-8 text-neon-yellow neon-glow">
        🏆 HIGH SCORES 🏆
      </h1>

      <div className="w-full max-w-4xl">
        {highScores.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🎮</div>
            <p className="text-xl text-light-text mb-4">No high scores yet!</p>
            <p className="text-medium-text">Play some games to see your scores here.</p>
          </div>
        ) : (
          <div className="space-y-2">
            {/* Header */}
            <div className="grid grid-cols-6 gap-4 px-4 py-2 bg-accent-dark-blue/50 rounded-lg border border-neon-blue text-sm font-semibold">
              <div className="text-neon-cyan">Rank</div>
              <div className="text-neon-cyan">Player</div>
              <div className="text-neon-cyan">Score</div>
              <div className="text-neon-cyan">Best Combo</div>
              <div className="text-neon-cyan">Date</div>
              <div className="text-neon-cyan">Achievement</div>
            </div>

            {/* Scores */}
            {highScores.map((score, index) => (
              <div 
                key={index}
                className={`grid grid-cols-6 gap-4 px-4 py-3 rounded-lg border transition-all hover:scale-[1.02] ${
                  index === 0 
                    ? 'bg-gradient-to-r from-neon-yellow/20 to-neon-orange/20 border-neon-yellow' 
                    : index === 1
                    ? 'bg-gradient-to-r from-neon-blue/20 to-neon-cyan/20 border-neon-blue'
                    : index === 2
                    ? 'bg-gradient-to-r from-neon-orange/20 to-neon-red/20 border-neon-orange'
                    : 'bg-accent-dark-blue/30 border-neon-purple'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <span className="text-lg">{getRankEmoji(index + 1)}</span>
                  <span className="font-bold text-lg">#{index + 1}</span>
                </div>
                <div className="font-semibold text-bright-white truncate">
                  {score.username}
                </div>
                <div className="font-bold text-neon-green text-lg">
                  {score.score.toLocaleString()}
                </div>
                <div className="text-neon-orange">
                  {score.combo ? `${score.combo}x` : '-'}
                </div>
                <div className="text-medium-text text-sm">
                  {formatDate(score.timestamp)}
                </div>
                <div className="text-xs">
                  {score.score >= 1000 ? '🌟 High Scorer' : 
                   score.combo && score.combo >= 10 ? '🔥 Combo Master' :
                   score.score >= 500 ? '⭐ Good Job' : '🎯 Keep Going'}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Statistics */}
        {highScores.length > 0 && (
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-accent-dark-blue/30 border border-neon-green rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-neon-green">
                {Math.max(...highScores.map(s => s.score)).toLocaleString()}
              </div>
              <div className="text-sm text-light-text">Best Score</div>
            </div>
            <div className="bg-accent-dark-blue/30 border border-neon-orange rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-neon-orange">
                {Math.max(...highScores.map(s => s.combo || 0))}x
              </div>
              <div className="text-sm text-light-text">Best Combo</div>
            </div>
            <div className="bg-accent-dark-blue/30 border border-neon-purple rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-neon-purple">
                {Math.round(highScores.reduce((sum, s) => sum + s.score, 0) / highScores.length).toLocaleString()}
              </div>
              <div className="text-sm text-light-text">Average Score</div>
            </div>
          </div>
        )}
      </div>

      <div className="mt-8 flex space-x-4">
        <button
          onClick={onBack}
          className="neon-button px-8 py-3 rounded text-lg font-semibold transition-all hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue"
        >
          BACK TO MENU (ESC)
        </button>
        
        {highScores.length > 0 && (
          <button
            onClick={onClearScores}
            className="bg-neon-red/20 border-2 border-neon-red text-neon-red px-6 py-3 rounded text-lg font-semibold transition-all hover:scale-105 hover:bg-neon-red/30 focus:outline-none focus:ring-2 focus:ring-neon-red"
          >
            CLEAR SCORES
          </button>
        )}
      </div>

      <div className="mt-6 text-center text-sm text-medium-text">
        <p>🎮 Challenge your friends to beat your scores!</p>
        <p>Scores are saved locally in your browser</p>
      </div>
    </div>
  );
};

export default HighScoresScreen;