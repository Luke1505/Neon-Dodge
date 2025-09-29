'use client';

import React from 'react';

interface InstructionsScreenProps {
  onBack: () => void;
}

const InstructionsScreen: React.FC<InstructionsScreenProps> = ({ onBack }) => {
  return (
    <div className="flex flex-col items-center justify-center h-full bg-deep-space-black text-white p-8 overflow-y-auto">
      <h1 className="text-4xl font-bold mb-8 text-neon-cyan neon-glow">
        INSTRUCTIONS
      </h1>

      <div className="max-w-2xl space-y-6 text-center">
        {/* Objective */}
        <div className="bg-accent-dark-blue/30 border border-neon-blue rounded-lg p-4">
          <h2 className="text-2xl font-bold text-neon-yellow mb-3">🎯 Objective</h2>
          <p className="text-light-text text-lg">
            Dodge incoming obstacles, collect power-ups, and survive as long as possible to set high scores!
          </p>
        </div>

        {/* Controls */}
        <div className="bg-accent-dark-blue/30 border border-neon-green rounded-lg p-4">
          <h2 className="text-2xl font-bold text-neon-green mb-3">🎮 Controls</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
            <div>
              <p className="text-neon-blue font-semibold">Movement:</p>
              <p className="text-light-text">Arrow Keys or WASD</p>
            </div>
            <div>
              <p className="text-neon-blue font-semibold">Pause/Resume:</p>
              <p className="text-light-text">P key</p>
            </div>
            <div>
              <p className="text-neon-blue font-semibold">Menu:</p>
              <p className="text-light-text">ESC key</p>
            </div>
            <div>
              <p className="text-neon-blue font-semibold">Touch Support:</p>
              <p className="text-light-text">Mobile friendly!</p>
            </div>
          </div>
        </div>

        {/* Power-ups */}
        <div className="bg-accent-dark-blue/30 border border-neon-purple rounded-lg p-4">
          <h2 className="text-2xl font-bold text-neon-purple mb-3">⚡ Power-ups</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-neon-green rounded"></div>
                <span className="text-neon-green font-semibold">Shield</span>
              </div>
              <p className="text-sm text-light-text ml-6">One-hit protection</p>
              
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-neon-yellow rounded"></div>
                <span className="text-neon-yellow font-semibold">SlowMo</span>
              </div>
              <p className="text-sm text-light-text ml-6">Slows obstacles for 5 seconds</p>
              
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-neon-magenta rounded"></div>
                <span className="text-neon-magenta font-semibold">Bomb</span>
              </div>
              <p className="text-sm text-light-text ml-6">Clears all obstacles</p>
            </div>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-neon-purple rounded"></div>
                <span className="text-neon-purple font-semibold">Shrink</span>
              </div>
              <p className="text-sm text-light-text ml-6">Smaller & faster for 10 seconds</p>
              
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-neon-blue rounded"></div>
                <span className="text-neon-blue font-semibold">Extra Life</span>
              </div>
              <p className="text-sm text-light-text ml-6">Grants an additional life</p>
              
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-medium-text rounded"></div>
                <span className="text-medium-text font-semibold">Turret</span>
              </div>
              <p className="text-sm text-light-text ml-6">Auto-shoots obstacles for 10 seconds</p>
            </div>
          </div>
        </div>

        {/* Combo System */}
        <div className="bg-accent-dark-blue/30 border border-neon-orange rounded-lg p-4">
          <h2 className="text-2xl font-bold text-neon-orange mb-3">🔥 Combo System</h2>
          <p className="text-light-text text-lg mb-2">
            Dodge obstacles without getting hit to build your combo multiplier!
          </p>
          <p className="text-medium-text">
            Higher combos = Higher scores. Combo resets if you get hit or take too long between dodges.
          </p>
        </div>

        {/* Scoring */}
        <div className="bg-accent-dark-blue/30 border border-neon-cyan rounded-lg p-4">
          <h2 className="text-2xl font-bold text-neon-cyan mb-3">🏆 Scoring</h2>
          <div className="grid grid-cols-2 gap-4 text-left">
            <div>
              <p className="text-neon-blue font-semibold">Survival:</p>
              <p className="text-light-text">+1 per 0.1 seconds</p>
            </div>
            <div>
              <p className="text-neon-blue font-semibold">Power-ups:</p>
              <p className="text-light-text">+10 + combo bonus</p>
            </div>
            <div>
              <p className="text-neon-blue font-semibold">Obstacle Dodge:</p>
              <p className="text-light-text">Combo bonus</p>
            </div>
            <div>
              <p className="text-neon-blue font-semibold">Shooting:</p>
              <p className="text-light-text">+15 per obstacle</p>
            </div>
          </div>
        </div>
      </div>

      <button
        onClick={onBack}
        className="mt-8 neon-button px-8 py-3 rounded text-lg font-semibold transition-all hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-blue"
      >
        BACK TO MENU (ESC)
      </button>
    </div>
  );
};

export default InstructionsScreen;