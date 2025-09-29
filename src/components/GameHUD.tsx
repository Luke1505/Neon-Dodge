'use client';

import React from 'react';
import { GameState } from '@/types/game';

interface GameHUDProps {
  gameState: GameState;
  username: string;
}

const GameHUD: React.FC<GameHUDProps> = ({ gameState, username }) => {
  const { player, score, combo, maxCombo, activeEffects } = gameState;

  return (
    <div className="absolute top-0 left-0 right-0 p-4 bg-gradient-to-b from-black/70 to-transparent pointer-events-none">
      {/* Top Row */}
      <div className="flex justify-between items-start text-white">
        {/* Left Side - Player Info */}
        <div className="space-y-1">
          <div className="text-neon-blue text-lg font-semibold">
            Player: {username}
          </div>
          <div className="text-neon-yellow text-lg">
            Score: {score}
          </div>
          <div className="text-neon-red text-lg">
            Lives: {player.lives}
          </div>
        </div>

        {/* Right Side - Combo & Effects */}
        <div className="text-right space-y-1">
          {combo > 0 && (
            <div className="text-neon-orange text-lg font-bold animate-pulse">
              Combo: {combo}x
            </div>
          )}
          {maxCombo > 0 && (
            <div className="text-neon-purple text-sm">
              Best: {maxCombo}x
            </div>
          )}
          
          {/* Active Effects */}
          <div className="space-y-1">
            {activeEffects.shield && (
              <div className="text-neon-green text-sm font-semibold animate-pulse">
                🛡️ SHIELD
              </div>
            )}
            {activeEffects.slowmo && (
              <div className="text-neon-yellow text-sm font-semibold animate-pulse">
                ⏱️ SLOWMO
              </div>
            )}
            {player.shrunk && (
              <div className="text-neon-magenta text-sm font-semibold animate-pulse">
                🔹 SHRUNK
              </div>
            )}
            {activeEffects.turretActive && (
              <div className="text-medium-text text-sm font-semibold animate-pulse">
                🎯 TURRET
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Pickup Message */}
      {activeEffects.pickupMessage && (
        <div className="mt-4 text-center">
          <div className="inline-block bg-neon-yellow/20 border border-neon-yellow px-4 py-2 rounded text-neon-yellow font-bold animate-bounce">
            {activeEffects.pickupMessage}
          </div>
        </div>
      )}

      {/* Effect Timer Bars */}
      <div className="mt-4 space-y-2">
        {activeEffects.slowmo && (
          <div className="bg-accent-dark-blue rounded-full h-2 overflow-hidden">
            <div 
              className="h-full bg-neon-yellow transition-all duration-100"
              style={{
                width: `${Math.max(0, (activeEffects.slowmoEndTime - Date.now()) / 5000 * 100)}%`
              }}
            />
          </div>
        )}
        
        {player.shrunk && (
          <div className="bg-accent-dark-blue rounded-full h-2 overflow-hidden">
            <div 
              className="h-full bg-neon-magenta transition-all duration-100"
              style={{
                width: `${Math.max(0, (player.shrinkEndTime - Date.now()) / 10000 * 100)}%`
              }}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default GameHUD;