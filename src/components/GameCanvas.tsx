'use client';

import React, { forwardRef } from 'react';
import { GameState } from '@/types/game';

interface GameCanvasProps {
  gameState: GameState;
  width: number;
  height: number;
}

const GameCanvas = forwardRef<HTMLCanvasElement, GameCanvasProps>(
  ({ gameState, width, height }, ref) => {
    return (
      <canvas
        ref={ref}
        width={width}
        height={height}
        className="game-canvas border border-neon-blue"
        style={{
          imageRendering: 'pixelated',
          background: 'radial-gradient(circle at center, #1a1a3e 0%, #0a0a1e 100%)',
        }}
      />
    );
  }
);

GameCanvas.displayName = 'GameCanvas';

export default GameCanvas;