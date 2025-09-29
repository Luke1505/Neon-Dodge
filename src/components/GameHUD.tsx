'use client';

import React from 'react';
import { GameState } from '@/types/game';

interface GameHUDProps {
  gameState: GameState;
  username: string;
}

const GameHUD: React.FC<GameHUDProps> = ({ gameState, username }) => {
  const { player, score, lives, combo, maxCombo, activeEffects, timeElapsed } = gameState;

  // Format time elapsed
  const formatTime = (ms: number) => {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="absolute inset-0 pointer-events-none">
      {/* Top HUD */}
      <div className="absolute top-0 left-0 right-0 p-6 bg-gradient-to-b from-black/80 via-black/40 to-transparent">
        <div className="flex justify-between items-start">
          {/* Left Side - Player & Score Info */}
          <div className="space-y-2">
            <div className="flex items-center space-x-3">
              <div className="w-3 h-3 bg-neon-pink rounded-full animate-pulse"></div>
              <span className="text-neon-blue text-lg font-bold tracking-wide">
                {username}
              </span>
            </div>
            
            <div className="bg-black/60 rounded-lg px-4 py-2 border border-neon-yellow/50">
              <div className="text-neon-yellow text-2xl font-bold font-mono">
                {score.toLocaleString()}
              </div>
              <div className="text-xs text-light-text uppercase tracking-wider">
                Score
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="bg-black/60 rounded-lg px-3 py-1 border border-neon-red/50">
                <div className="flex items-center space-x-2">
                  <span className="text-neon-red text-lg">♥</span>
                  <span className="text-neon-red font-bold">{lives}</span>
                </div>
              </div>
              
              <div className="bg-black/60 rounded-lg px-3 py-1 border border-neon-green/50">
                <div className="text-neon-green text-sm font-mono">
                  {formatTime(timeElapsed)}
                </div>
              </div>
            </div>
          </div>

          {/* Right Side - Combo & Effects */}
          <div className="text-right space-y-2">
            {/* Combo Display */}
            {combo > 0 && (
              <div className="bg-black/70 rounded-lg px-4 py-2 border border-neon-orange/50">
                <div className="text-neon-orange text-3xl font-bold animate-pulse">
                  {combo}x
                </div>
                <div className="text-xs text-light-text uppercase tracking-wider">
                  Combo
                </div>
              </div>
            )}
            
            {maxCombo > 0 && combo === 0 && (
              <div className="bg-black/40 rounded-lg px-3 py-1 border border-neon-purple/30">
                <div className="text-neon-purple text-sm">
                  Best: {maxCombo}x
                </div>
              </div>
            )}
            
            {/* Active Effects */}
            <div className="space-y-1">
              {activeEffects.shield && (
                <div className="bg-black/70 rounded-lg px-3 py-1 border border-neon-blue/50 animate-pulse">
                  <div className="text-neon-blue text-sm font-bold flex items-center">
                    <span className="mr-1">🛡️</span>
                    SHIELD
                  </div>
                </div>
              )}
              {activeEffects.slowmo && (
                <div className="bg-black/70 rounded-lg px-3 py-1 border border-neon-cyan/50 animate-pulse">
                  <div className="text-neon-cyan text-sm font-bold flex items-center">
                    <span className="mr-1">⏱️</span>
                    SLOWMO
                  </div>
                </div>
              )}
              {activeEffects.shrink && (
                <div className="bg-black/70 rounded-lg px-3 py-1 border border-neon-green/50 animate-pulse">
                  <div className="text-neon-green text-sm font-bold flex items-center">
                    <span className="mr-1">🔹</span>
                    SHRUNK
                  </div>
                </div>
              )}
              {activeEffects.turret && (
                <div className="bg-black/70 rounded-lg px-3 py-1 border border-neon-yellow/50 animate-pulse">
                  <div className="text-neon-yellow text-sm font-bold flex items-center">
                    <span className="mr-1">🎯</span>
                    TURRET
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Bottom HUD - Effect Timer Bars */}
      <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-black/60 to-transparent">
        <div className="space-y-2 max-w-md mx-auto">
          {activeEffects.slowmo && activeEffects.slowmoEndTime && (
            <div className="bg-black/60 rounded-full h-3 overflow-hidden border border-neon-cyan/50">
              <div 
                className="h-full bg-gradient-to-r from-neon-cyan to-neon-blue transition-all duration-100 relative"
                style={{
                  width: `${Math.max(0, (activeEffects.slowmoEndTime - Date.now()) / 4000 * 100)}%`
                }}
              >
                <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
              </div>
            </div>
          )}
          
          {activeEffects.shrink && activeEffects.shrinkEndTime && (
            <div className="bg-black/60 rounded-full h-3 overflow-hidden border border-neon-green/50">
              <div 
                className="h-full bg-gradient-to-r from-neon-green to-lime-400 transition-all duration-100 relative"
                style={{
                  width: `${Math.max(0, (activeEffects.shrinkEndTime - Date.now()) / 6000 * 100)}%`
                }}
              >
                <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
              </div>
            </div>
          )}

          {activeEffects.turret && activeEffects.turretEndTime && (
            <div className="bg-black/60 rounded-full h-3 overflow-hidden border border-neon-yellow/50">
              <div 
                className="h-full bg-gradient-to-r from-neon-yellow to-amber-400 transition-all duration-100 relative"
                style={{
                  width: `${Math.max(0, (activeEffects.turretEndTime - Date.now()) / 8000 * 100)}%`
                }}
              >
                <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
              </div>
            </div>
          )}
        </div>
        
        {/* Control hints */}
        <div className="text-center mt-4">
          <div className="text-xs text-medium-text font-medium uppercase tracking-wider">
            P: Pause • ESC: Menu • WASD/Arrows: Move
          </div>
        </div>
      </div>
    </div>
  );
};

export default GameHUD;