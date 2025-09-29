'use client';

import React from 'react';

interface InstructionsScreenProps {
  onBack: () => void;
}

const InstructionsScreen: React.FC<InstructionsScreenProps> = ({ onBack }) => {
  return (
    <div className="flex flex-col items-center h-full bg-gradient-to-br from-deep-space-black via-cyan-900/10 to-deep-space-black text-white p-8 overflow-y-auto relative">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-16 left-8 w-1.5 h-1.5 bg-neon-cyan rounded-full animate-pulse"></div>
        <div className="absolute top-32 right-12 w-1 h-1 bg-neon-blue rounded-full animate-pulse delay-1000"></div>
        <div className="absolute bottom-32 left-16 w-2 h-2 bg-neon-green rounded-full animate-pulse delay-2000"></div>
        <div className="absolute bottom-16 right-8 w-1 h-1 bg-neon-purple rounded-full animate-pulse delay-3000"></div>
      </div>

      <div className="z-10 w-full max-w-4xl mx-auto slide-in">
        {/* Title */}
        <div className="text-center mb-8">
          <h1 className="game-title text-5xl font-black mb-4 neon-glow text-neon-cyan pulse-neon">
            INSTRUCTIONS
          </h1>
          <div className="h-1 w-32 mx-auto bg-gradient-to-r from-transparent via-neon-cyan to-transparent rounded-full glow-pulse"></div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Objective */}
          <div className="bg-gradient-to-br from-black/80 to-black/60 border-2 border-neon-blue rounded-xl p-6 neon-border hover:scale-105 transition-transform duration-300">
            <h2 className="game-title text-2xl font-bold text-neon-yellow mb-4 flex items-center">
              <span className="mr-3 text-3xl">🎯</span>
              OBJECTIVE
            </h2>
            <p className="text-light-text text-lg leading-relaxed">
              Dodge incoming obstacles, collect power-ups, and survive as long as possible to set high scores in this 
              <span className="text-neon-pink font-semibold"> neon-futuristic</span> adventure!
            </p>
          </div>

          {/* Controls */}
          <div className="bg-gradient-to-br from-black/80 to-black/60 border-2 border-neon-green rounded-xl p-6 neon-border hover:scale-105 transition-transform duration-300">
            <h2 className="game-title text-2xl font-bold text-neon-green mb-4 flex items-center">
              <span className="mr-3 text-3xl">🎮</span>
              CONTROLS
            </h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-neon-blue font-semibold">Movement:</span>
                <span className="text-light-text bg-black/50 px-3 py-1 rounded font-mono">WASD / Arrows</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-neon-blue font-semibold">Pause:</span>
                <span className="text-light-text bg-black/50 px-3 py-1 rounded font-mono">P</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-neon-blue font-semibold">Menu:</span>
                <span className="text-light-text bg-black/50 px-3 py-1 rounded font-mono">ESC</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-neon-blue font-semibold">Mobile:</span>
                <span className="text-light-text">Touch Support ✓</span>
              </div>
            </div>
          </div>

          {/* Power-ups */}
          <div className="bg-gradient-to-br from-black/80 to-black/60 border-2 border-neon-purple rounded-xl p-6 neon-border hover:scale-105 transition-transform duration-300 lg:col-span-2">
            <h2 className="game-title text-2xl font-bold text-neon-purple mb-6 flex items-center">
              <span className="mr-3 text-3xl">⚡</span>
              POWER-UPS
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="bg-gradient-to-r from-neon-blue/20 to-neon-cyan/20 rounded-lg p-4 border border-neon-blue/50">
                <div className="flex items-center space-x-3 mb-2">
                  <div className="w-6 h-6 bg-neon-blue rounded-full glow-pulse"></div>
                  <span className="text-neon-blue font-bold">SHIELD</span>
                </div>
                <p className="text-sm text-light-text">Protects from one obstacle hit</p>
              </div>
              
              <div className="bg-gradient-to-r from-neon-cyan/20 to-neon-blue/20 rounded-lg p-4 border border-neon-cyan/50">
                <div className="flex items-center space-x-3 mb-2">
                  <div className="w-6 h-6 bg-neon-cyan rounded-full glow-pulse"></div>
                  <span className="text-neon-cyan font-bold">SLOW MO</span>
                </div>
                <p className="text-sm text-light-text">Slows obstacles for 4 seconds</p>
              </div>
              
              <div className="bg-gradient-to-r from-neon-red/20 to-neon-orange/20 rounded-lg p-4 border border-neon-red/50">
                <div className="flex items-center space-x-3 mb-2">
                  <div className="w-6 h-6 bg-neon-red rounded-full glow-pulse"></div>
                  <span className="text-neon-red font-bold">BOMB</span>
                </div>
                <p className="text-sm text-light-text">Clears all obstacles</p>
              </div>
              
              <div className="bg-gradient-to-r from-neon-green/20 to-lime-500/20 rounded-lg p-4 border border-neon-green/50">
                <div className="flex items-center space-x-3 mb-2">
                  <div className="w-6 h-6 bg-neon-green rounded-full glow-pulse"></div>
                  <span className="text-neon-green font-bold">SHRINK</span>
                </div>
                <p className="text-sm text-light-text">Smaller player for 6 seconds</p>
              </div>
              
              <div className="bg-gradient-to-r from-neon-pink/20 to-neon-purple/20 rounded-lg p-4 border border-neon-pink/50">
                <div className="flex items-center space-x-3 mb-2">
                  <div className="w-6 h-6 bg-neon-pink rounded-full glow-pulse"></div>
                  <span className="text-neon-pink font-bold">EXTRA LIFE</span>
                </div>
                <p className="text-sm text-light-text">Grants an additional life</p>
              </div>
              
              <div className="bg-gradient-to-r from-neon-yellow/20 to-neon-orange/20 rounded-lg p-4 border border-neon-yellow/50">
                <div className="flex items-center space-x-3 mb-2">
                  <div className="w-6 h-6 bg-neon-yellow rounded-full glow-pulse"></div>
                  <span className="text-neon-yellow font-bold">TURRET</span>
                </div>
                <p className="text-sm text-light-text">Auto-shoots for 8 seconds</p>
              </div>
            </div>
          </div>

          {/* Combo System */}
          <div className="bg-gradient-to-br from-black/80 to-black/60 border-2 border-neon-orange rounded-xl p-6 neon-border hover:scale-105 transition-transform duration-300">
            <h2 className="game-title text-2xl font-bold text-neon-orange mb-4 flex items-center">
              <span className="mr-3 text-3xl">🔥</span>
              COMBO SYSTEM
            </h2>
            <p className="text-light-text text-lg mb-3 leading-relaxed">
              Dodge obstacles consecutively to build your combo multiplier!
            </p>
            <div className="bg-neon-orange/10 rounded-lg p-3 border border-neon-orange/30">
              <p className="text-medium-text text-sm">
                Higher combos = Higher scores. Combo resets if you get hit.
              </p>
            </div>
          </div>

          {/* Scoring */}
          <div className="bg-gradient-to-br from-black/80 to-black/60 border-2 border-neon-yellow rounded-xl p-6 neon-border hover:scale-105 transition-transform duration-300">
            <h2 className="game-title text-2xl font-bold text-neon-yellow mb-4 flex items-center">
              <span className="mr-3 text-3xl">🏆</span>
              SCORING
            </h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-neon-blue font-semibold">Survival:</span>
                <span className="text-light-text">+1 per frame</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-neon-blue font-semibold">Power-ups:</span>
                <span className="text-light-text">+50 points</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-neon-blue font-semibold">Bullet Hits:</span>
                <span className="text-light-text">+100 + combo</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-neon-blue font-semibold">Bomb Clear:</span>
                <span className="text-light-text">+200 bonus</span>
              </div>
            </div>
          </div>
        </div>

        {/* Back Button */}
        <div className="text-center">
          <button
            onClick={onBack}
            className="neon-button px-12 py-4 rounded-lg text-lg font-bold transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-neon-cyan gpu-accelerated group"
          >
            <span className="flex items-center justify-center">
              <span className="mr-3 group-hover:-translate-x-1 transition-transform duration-300">←</span>
              BACK TO MENU
              <span className="ml-3 text-sm opacity-70">(ESC)</span>
            </span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default InstructionsScreen;