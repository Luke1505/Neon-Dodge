'use client';

import React from 'react';

interface PauseMenuProps {
  onResume: () => void;
  onRestart: () => void;
  onMainMenu: () => void;
}

const PauseMenu: React.FC<PauseMenuProps> = ({ onResume, onRestart, onMainMenu }) => {
  return (
    <div className="absolute inset-0 bg-black/90 backdrop-blur-sm flex items-center justify-center slide-in">
      <div className="bg-gradient-to-br from-black/95 to-black/80 border-2 border-neon-cyan rounded-xl p-10 text-center neon-border max-w-md w-full mx-4 hover:scale-105 transition-transform duration-300">
        {/* Pause Icon */}
        <div className="text-6xl mb-6 animate-pulse">⏸️</div>
        
        {/* Title */}
        <h2 className="game-title text-4xl font-black text-neon-cyan mb-8 neon-glow pulse-neon">
          PAUSED
        </h2>
        
        {/* Menu Buttons */}
        <div className="space-y-4 mb-6">
          <button
            onClick={onResume}
            className="w-full neon-button px-8 py-4 rounded-lg text-lg font-bold transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-cyan gpu-accelerated group"
          >
            <span className="flex items-center justify-center">
              <span className="mr-3">▶️</span>
              RESUME
              <span className="ml-3 text-sm opacity-70">(P)</span>
            </span>
          </button>
          
          <button
            onClick={onRestart}
            className="w-full neon-button px-8 py-4 rounded-lg text-lg font-bold transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue gpu-accelerated"
          >
            <span className="flex items-center justify-center">
              <span className="mr-3">🔄</span>
              RESTART
            </span>
          </button>
          
          <button
            onClick={onMainMenu}
            className="w-full neon-button px-8 py-4 rounded-lg text-lg font-bold transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue gpu-accelerated"
          >
            <span className="flex items-center justify-center">
              <span className="mr-3">🏠</span>
              MAIN MENU
              <span className="ml-3 text-sm opacity-70">(ESC)</span>
            </span>
          </button>
        </div>
        
        {/* Quick Tips */}
        <div className="bg-gradient-to-r from-neon-cyan/10 to-neon-blue/10 rounded-lg p-4 border border-neon-cyan/30">
          <h3 className="text-neon-cyan font-bold mb-2 text-sm uppercase tracking-wider">
            Quick Tips
          </h3>
          <div className="text-light-text text-sm space-y-1">
            <p>• Collect power-ups for special abilities</p>
            <p>• Build combos for higher scores</p>
            <p>• Watch out for increasing difficulty!</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PauseMenu;