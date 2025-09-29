'use client';

import React, { useState } from 'react';
import { HighScore } from '@/types/game';
import { ACHIEVEMENTS } from '@/lib/constants';

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
  const [showConfirmClear, setShowConfirmClear] = useState(false);

  const formatDate = (timestamp?: number) => {
    if (!timestamp) return 'Unknown';
    return new Date(timestamp).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: '2-digit'
    });
  };

  const getRankEmoji = (rank: number) => {
    switch (rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return '🏅';
    }
  };

  const getAchievement = (score: HighScore) => {
    if (score.score >= ACHIEVEMENTS.HIGH_SCORER.threshold) {
      return { icon: ACHIEVEMENTS.HIGH_SCORER.icon, name: ACHIEVEMENTS.HIGH_SCORER.name, color: 'text-neon-yellow' };
    }
    if (score.combo && score.combo >= ACHIEVEMENTS.COMBO_MASTER.threshold) {
      return { icon: ACHIEVEMENTS.COMBO_MASTER.icon, name: ACHIEVEMENTS.COMBO_MASTER.name, color: 'text-neon-orange' };
    }
    if (score.score >= ACHIEVEMENTS.GOOD_JOB.threshold) {
      return { icon: ACHIEVEMENTS.GOOD_JOB.icon, name: ACHIEVEMENTS.GOOD_JOB.name, color: 'text-neon-green' };
    }
    return { icon: '🎯', name: 'Keep Going', color: 'text-neon-cyan' };
  };

  const handleClearScores = () => {
    if (showConfirmClear) {
      onClearScores();
      setShowConfirmClear(false);
    } else {
      setShowConfirmClear(true);
      setTimeout(() => setShowConfirmClear(false), 3000);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-deep-space-black via-yellow-900/5 to-deep-space-black text-white p-8 overflow-y-auto relative">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-12 w-2 h-2 bg-neon-yellow rounded-full animate-pulse"></div>
        <div className="absolute top-40 right-16 w-1 h-1 bg-neon-orange rounded-full animate-pulse delay-1000"></div>
        <div className="absolute bottom-40 left-8 w-1.5 h-1.5 bg-neon-green rounded-full animate-pulse delay-2000"></div>
        <div className="absolute bottom-20 right-12 w-1 h-1 bg-neon-purple rounded-full animate-pulse delay-3000"></div>
      </div>

      <div className="z-10 w-full max-w-6xl mx-auto slide-in">
        {/* Title */}
        <div className="text-center mb-8">
          <h1 className="game-title text-5xl font-black mb-4 neon-glow text-neon-yellow pulse-neon">
            🏆 HIGH SCORES 🏆
          </h1>
          <div className="h-1 w-40 mx-auto bg-gradient-to-r from-transparent via-neon-yellow to-transparent rounded-full glow-pulse"></div>
        </div>

        {highScores.length === 0 ? (
          /* Empty State */
          <div className="text-center py-16">
            <div className="bg-gradient-to-br from-black/80 to-black/60 border-2 border-neon-blue rounded-xl p-12 neon-border max-w-md mx-auto">
              <div className="text-8xl mb-6 animate-bounce">🎮</div>
              <h2 className="text-2xl font-bold text-neon-blue mb-4">No high scores yet!</h2>
              <p className="text-light-text text-lg mb-2">Play some games to see your scores here.</p>
              <p className="text-medium-text">Be the first to set a record!</p>
            </div>
          </div>
        ) : (
          /* Scores Table */
          <div className="space-y-3 mb-8">
            {/* Header */}
            <div className="hidden md:grid grid-cols-6 gap-4 px-6 py-3 bg-gradient-to-r from-black/80 to-black/60 rounded-xl border border-neon-blue text-sm font-bold uppercase tracking-wider">
              <div className="text-neon-cyan">Rank</div>
              <div className="text-neon-cyan">Player</div>
              <div className="text-neon-cyan">Score</div>
              <div className="text-neon-cyan">Combo</div>
              <div className="text-neon-cyan">Date</div>
              <div className="text-neon-cyan">Achievement</div>
            </div>

            {/* Scores */}
            {highScores.map((score, index) => {
              const achievement = getAchievement(score);
              return (
                <div 
                  key={index}
                  className={`
                    grid grid-cols-3 md:grid-cols-6 gap-4 px-6 py-4 rounded-xl border-2 transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl cursor-pointer
                    ${index === 0 
                      ? 'bg-gradient-to-r from-yellow-900/40 to-orange-900/40 border-neon-yellow shadow-yellow-500/20' 
                      : index === 1
                      ? 'bg-gradient-to-r from-blue-900/40 to-cyan-900/40 border-neon-blue shadow-blue-500/20'
                      : index === 2
                      ? 'bg-gradient-to-r from-orange-900/40 to-red-900/40 border-neon-orange shadow-orange-500/20'
                      : 'bg-gradient-to-r from-black/60 to-black/40 border-neon-purple/50 hover:border-neon-purple'
                    }
                  `}
                >
                  {/* Rank */}
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">{getRankEmoji(index + 1)}</span>
                    <span className="font-bold text-xl">#{index + 1}</span>
                  </div>
                  
                  {/* Player (mobile: spans 2 cols) */}
                  <div className="md:col-span-1 col-span-2 flex flex-col">
                    <span className="font-bold text-lg text-bright-white truncate">
                      {score.username}
                    </span>
                    <span className="text-sm text-medium-text md:hidden">
                      {formatDate(score.timestamp)}
                    </span>
                  </div>
                  
                  {/* Score */}
                  <div className="flex flex-col items-end md:items-start">
                    <span className="font-bold text-xl text-neon-green font-mono">
                      {score.score.toLocaleString()}
                    </span>
                    <span className="text-sm text-neon-orange md:hidden">
                      {score.combo ? `${score.combo}x combo` : ''}
                    </span>
                  </div>
                  
                  {/* Combo (desktop only) */}
                  <div className="hidden md:flex items-center">
                    <span className="font-bold text-lg text-neon-orange">
                      {score.combo ? `${score.combo}x` : '-'}
                    </span>
                  </div>
                  
                  {/* Date (desktop only) */}
                  <div className="hidden md:flex items-center">
                    <span className="text-medium-text">
                      {formatDate(score.timestamp)}
                    </span>
                  </div>
                  
                  {/* Achievement (desktop only) */}
                  <div className="hidden md:flex items-center">
                    <span className={`text-sm font-medium ${achievement.color}`}>
                      {achievement.icon} {achievement.name}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Statistics */}
        {highScores.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-gradient-to-br from-green-900/40 to-emerald-900/40 border-2 border-neon-green rounded-xl p-6 text-center neon-border hover:scale-105 transition-transform duration-300">
              <div className="text-4xl font-bold text-neon-green font-mono mb-2">
                {Math.max(...highScores.map(s => s.score)).toLocaleString()}
              </div>
              <div className="text-light-text font-medium">🏆 Best Score</div>
            </div>
            <div className="bg-gradient-to-br from-orange-900/40 to-red-900/40 border-2 border-neon-orange rounded-xl p-6 text-center neon-border hover:scale-105 transition-transform duration-300">
              <div className="text-4xl font-bold text-neon-orange font-mono mb-2">
                {Math.max(...highScores.map(s => s.combo || 0))}x
              </div>
              <div className="text-light-text font-medium">🔥 Best Combo</div>
            </div>
            <div className="bg-gradient-to-br from-purple-900/40 to-blue-900/40 border-2 border-neon-purple rounded-xl p-6 text-center neon-border hover:scale-105 transition-transform duration-300">
              <div className="text-4xl font-bold text-neon-purple font-mono mb-2">
                {Math.round(highScores.reduce((sum, s) => sum + s.score, 0) / highScores.length).toLocaleString()}
              </div>
              <div className="text-light-text font-medium">📊 Average</div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6">
          <button
            onClick={onBack}
            className="neon-button px-12 py-4 rounded-lg text-lg font-bold transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue gpu-accelerated group"
          >
            <span className="flex items-center justify-center">
              <span className="mr-3 group-hover:-translate-x-1 transition-transform duration-300">←</span>
              BACK TO MENU
              <span className="ml-3 text-sm opacity-70">(ESC)</span>
            </span>
          </button>
          
          {highScores.length > 0 && (
            <button
              onClick={handleClearScores}
              className={`
                px-8 py-4 rounded-lg text-lg font-bold transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-red
                ${showConfirmClear 
                  ? 'bg-red-600 border-2 border-red-400 text-white animate-pulse' 
                  : 'bg-red-900/30 border-2 border-neon-red text-neon-red hover:bg-red-900/50'
                }
              `}
            >
              {showConfirmClear ? '⚠️ CONFIRM CLEAR?' : '🗑️ CLEAR SCORES'}
            </button>
          )}
        </div>

        {/* Footer */}
        <div className="mt-8 text-center space-y-2">
          <p className="text-medium-text font-medium">
            🎮 Challenge your friends to beat your scores!
          </p>
          <p className="text-sm text-dark-gray">
            Scores are saved locally in your browser
          </p>
        </div>
      </div>
    </div>
  );
};

export default HighScoresScreen;