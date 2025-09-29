'use client';

import { useEffect, useRef, useCallback } from 'react';
import { GameState } from '@/types/game';
import { gameEngine } from '@/lib/gameEngine';

export const useGameLoop = (gameState: GameState, canvasRef: React.RefObject<HTMLCanvasElement | null>) => {
  const animationFrameRef = useRef<number>();
  const lastTimeRef = useRef<number>(0);

  const gameLoop = useCallback((currentTime: number) => {
    const deltaTime = currentTime - lastTimeRef.current;
    lastTimeRef.current = currentTime;

    if (canvasRef.current && gameState.gameRunning && !gameState.gamePaused) {
      const ctx = canvasRef.current.getContext('2d');
      if (ctx) {
        gameEngine.update(gameState, deltaTime);
        gameEngine.render(ctx, gameState);
      }
    }

    animationFrameRef.current = requestAnimationFrame(gameLoop);
  }, [gameState, canvasRef]);

  useEffect(() => {
    if (gameState.gameRunning) {
      animationFrameRef.current = requestAnimationFrame(gameLoop);
    }

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [gameState.gameRunning, gameLoop]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, []);
};