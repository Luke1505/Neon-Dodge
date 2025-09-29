'use client';

import { useState, useCallback } from 'react';
import { GameState, Player, ActiveEffects } from '@/types/game';
import { GAME_SETTINGS, COLORS, PLAYER_SETTINGS } from '@/lib/constants';

const createInitialPlayer = (): Player => ({
  x: GAME_SETTINGS.WIDTH / 2,
  y: GAME_SETTINGS.HEIGHT / 2,
  size: PLAYER_SETTINGS.SIZE,
  color: PLAYER_SETTINGS.COLOR,
  trail: [],
});

const createInitialEffects = (): ActiveEffects => ({
  shield: false,
  slowmo: false,
  shrink: false,
  turret: false,
});

const createInitialGameState = (): GameState => ({
  gameRunning: false,
  gamePaused: false,
  gameOver: false,
  score: 0,
  lives: GAME_SETTINGS.INITIAL_LIVES,
  timeElapsed: 0,
  player: createInitialPlayer(),
  obstacles: [],
  powerUps: [],
  bullets: [],
  particles: [],
  activeEffects: createInitialEffects(),
  combo: 0,
  maxCombo: 0,
  powerUpsCollected: 0,
});

export const useGameState = () => {
  const [gameState, setGameState] = useState<GameState>(createInitialGameState);

  const initializeGame = useCallback(() => {
    setGameState(createInitialGameState());
    setGameState(prev => ({ ...prev, gameRunning: true }));
  }, []);

  const resetGame = useCallback(() => {
    setGameState(createInitialGameState());
  }, []);

  const updateGameState = useCallback((updater: (state: GameState) => GameState) => {
    setGameState(updater);
  }, []);

  const updatePlayer = useCallback((updater: (player: Player) => Player) => {
    setGameState(prev => ({
      ...prev,
      player: updater(prev.player),
    }));
  }, []);

  const addScore = useCallback((points: number) => {
    setGameState(prev => ({
      ...prev,
      score: prev.score + points,
    }));
  }, []);

  const incrementCombo = useCallback(() => {
    setGameState(prev => {
      const newCombo = prev.combo + 1;
      return {
        ...prev,
        combo: newCombo,
        maxCombo: Math.max(prev.maxCombo, newCombo),
      };
    });
  }, []);

  const resetCombo = useCallback(() => {
    setGameState(prev => ({
      ...prev,
      combo: 0,
    }));
  }, []);

  const togglePause = useCallback(() => {
    setGameState(prev => ({
      ...prev,
      gamePaused: !prev.gamePaused,
    }));
  }, []);

  const setGameOver = useCallback(() => {
    setGameState(prev => ({
      ...prev,
      gameRunning: false,
      gameOver: true,
      gamePaused: false,
    }));
  }, []);

  return {
    gameState,
    initializeGame,
    resetGame,
    updateGameState,
    updatePlayer,
    addScore,
    incrementCombo,
    resetCombo,
    togglePause,
    setGameOver,
  };
};