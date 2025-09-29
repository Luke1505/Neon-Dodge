'use client';

import React from 'react';

interface PauseMenuProps {
  onResume: () => void;
  onRestart: () => void;
  onMainMenu: () => void;
}

const PauseMenu: React.FC<PauseMenuProps> = ({ onResume, onRestart, onMainMenu }) => {
  return (
    <div className="absolute inset-0 bg-black/80 flex items-center justify-center">
      <div className="bg-deep-space-black border-2 border-neon-blue rounded-lg p-8 text-center">
        <h2 className="text-4xl font-bold text-neon-cyan mb-8">PAUSED</h2>
        
        <div className="space-y-4">
          <button
            onClick={onResume}
            className="neon-button px-8 py-3 rounded text-lg font-semibold transition-all hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue w-full"
          >
            RESUME (P)
          </button>
          
          <button
            onClick={onRestart}
            className="neon-button px-8 py-3 rounded text-lg font-semibold transition-all hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue w-full"
          >
            RESTART (R)
          </button>
          
          <button
            onClick={onMainMenu}
            className="neon-button px-8 py-3 rounded text-lg font-semibold transition-all hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue w-full"
          >
            MAIN MENU (ESC)
          </button>
        </div>
        
        <div className="mt-6 text-sm text-medium-text">
          <p>Use WASD or Arrow Keys to move</p>
          <p>Collect power-ups to gain abilities</p>
        </div>
      </div>
    </div>
  );
};

export default PauseMenu;