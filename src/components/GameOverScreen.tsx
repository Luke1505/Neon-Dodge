'use client';

import React, { useEffect, useState } from 'react';
import { HighScore } from '@/types/game';
import { ACHIEVEMENTS } from '@/lib/constants';

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
  const [showAchievements, setShowAchievements] = useState(false);
  const isNewHighScore = highScores.length === 0 || score > (highScores[highScores.length - 1]?.score || 0);
  const ranking = highScores.findIndex(hs => hs.score <= score) + 1;

  // Check for achievements
  const earnedAchievements = [];
  if (score >= ACHIEVEMENTS.HIGH_SCORER.threshold) {
    earnedAchievements.push(ACHIEVEMENTS.HIGH_SCORER);
  }
  if (score >= ACHIEVEMENTS.GOOD_JOB.threshold) {
    earnedAchievements.push(ACHIEVEMENTS.GOOD_JOB);
  }
  if (maxCombo >= ACHIEVEMENTS.COMBO_MASTER.threshold) {
    earnedAchievements.push(ACHIEVEMENTS.COMBO_MASTER);
  }

  useEffect(() => {
    if (earnedAchievements.length > 0) {
      const timer = setTimeout(() => setShowAchievements(true), 1000);
      return () => clearTimeout(timer);
    }
  }, [earnedAchievements.length]);

  return (
    <div className="flex flex-col items-center justify-center h-full bg-gradient-to-br from-deep-space-black via-red-900/10 to-deep-space-black text-white p-8 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-2 h-2 bg-neon-red rounded-full animate-pulse"></div>
        <div className="absolute top-40 right-20 w-1 h-1 bg-neon-orange rounded-full animate-pulse delay-1000"></div>
        <div className="absolute bottom-40 left-20 w-1.5 h-1.5 bg-neon-yellow rounded-full animate-pulse delay-2000"></div>
        <div className="absolute bottom-20 right-10 w-1 h-1 bg-neon-pink rounded-full animate-pulse delay-3000"></div>
      </div>

      <div className="z-10 w-full max-w-lg mx-auto slide-in">
        {/* Game Over Title */}
        <div className="text-center mb-8">
          <h1 className="game-title text-6xl font-black mb-4 neon-glow text-neon-red pulse-neon">
            GAME OVER
          </h1>
          <div className="h-1 w-40 mx-auto bg-gradient-to-r from-transparent via-neon-red to-transparent rounded-full glow-pulse"></div>
        </div>

        {/* Score Display */}
        <div className="bg-gradient-to-br from-black/80 to-black/60 border-2 border-neon-blue rounded-xl p-8 mb-8 text-center neon-border">
          <h2 className="text-3xl font-bold text-neon-cyan mb-6 game-title">
            {username}
          </h2>
          
          <div className="space-y-4">
            <div className="bg-gradient-to-r from-neon-yellow/20 to-neon-orange/20 rounded-lg p-4">
              <div className="text-sm text-light-text uppercase tracking-wider mb-1">
                Final Score
              </div>
              <div className="text-4xl font-bold text-neon-yellow font-mono">
                {score.toLocaleString()}
              </div>
            </div>
            
            {maxCombo > 0 && (
              <div className="bg-gradient-to-r from-neon-orange/20 to-neon-red/20 rounded-lg p-3">
                <div className="text-sm text-light-text uppercase tracking-wider mb-1">
                  Best Combo
                </div>
                <div className="text-2xl font-bold text-neon-orange">
                  {maxCombo}x
                </div>
              </div>
            )}
            
            {isNewHighScore && ranking <= 10 && (
              <div className="bg-gradient-to-r from-neon-green/20 to-neon-cyan/20 rounded-lg p-4 border border-neon-green animate-pulse">
                <div className="text-neon-green font-bold text-xl">
                  🎉 NEW HIGH SCORE! 🎉
                </div>
                {ranking <= 3 && (
                  <div className="text-neon-cyan text-lg mt-2">
                    #{ranking} on the leaderboard!
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Achievements */}
        {showAchievements && earnedAchievements.length > 0 && (
          <div className="bg-gradient-to-br from-yellow-900/30 to-orange-900/30 border-2 border-neon-yellow rounded-xl p-6 mb-8 slide-in">
            <h3 className="text-xl font-bold text-neon-yellow mb-4 text-center game-title">
              🏆 ACHIEVEMENTS UNLOCKED
            </h3>
            <div className="space-y-2">
              {earnedAchievements.map((achievement, index) => (
                <div 
                  key={index}
                  className="achievement-badge rounded-lg px-4 py-2 text-center font-bold text-sm"
                  style={{ animationDelay: `${index * 200}ms` }}
                >
                  {achievement.icon} {achievement.name}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* High Scores Preview */}
        {highScores.length > 0 && (
          <div className="bg-gradient-to-br from-purple-900/30 to-blue-900/30 border border-neon-purple rounded-xl p-6 mb-8">
            <h3 className="text-xl font-bold text-neon-purple mb-4 text-center game-title">
              🏆 TOP PLAYERS
            </h3>
            <div className="space-y-2">
              {highScores.slice(0, 5).map((hs, index) => (
                <div 
                  key={index} 
                  className={`flex justify-between items-center py-2 px-3 rounded ${
                    hs.username === username && hs.score === score 
                      ? 'bg-neon-yellow/20 text-neon-yellow font-bold border border-neon-yellow/50' 
                      : 'text-light-text'
                  }`}
                >
                  <span className="flex items-center">
                    <span className="w-6 text-center font-bold">
                      {index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `#${index + 1}`}
                    </span>
                    <span className="ml-3">{hs.username}</span>
                  </span>
                  <span className="font-mono font-bold">
                    {hs.score.toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="space-y-4">
          <button
            onClick={onPlayAgain}
            className="w-full neon-button px-8 py-4 rounded-lg text-lg font-bold transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue gpu-accelerated group"
          >
            <span className="flex items-center justify-center">
              <span className="mr-2">🔄</span>
              PLAY AGAIN
              <span className="ml-2 group-hover:rotate-180 transition-transform duration-300">🎮</span>
            </span>
          </button>
          
          <button
            onClick={onMainMenu}
            className="w-full neon-button px-8 py-4 rounded-lg text-lg font-bold transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue gpu-accelerated"
          >
            <span className="flex items-center justify-center">
              <span className="mr-2">🏠</span>
              MAIN MENU
            </span>
          </button>
        </div>

        {/* Footer Message */}
        <div className="mt-8 text-center space-y-2">
          <p className="text-medium-text font-medium">
            Thanks for playing Neon Dodge!
          </p>
          <p className="text-sm text-dark-gray">
            Challenge your friends to beat your score! 🚀
          </p>
        </div>
      </div>
    </div>
  );
};

export default GameOverScreen;