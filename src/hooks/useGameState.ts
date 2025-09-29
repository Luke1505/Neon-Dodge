'use client';

import { useState, useCallback } from 'react';
import { GameState, Player, ActiveEffects, GameTimers } from '@/types/game';
import { PLAYER_CONFIG, GAME_SETTINGS, COLORS } from '@/lib/constants';

const createInitialPlayer = (): Player => ({
  x: GAME_SETTINGS.WIDTH / 2 - PLAYER_CONFIG.WIDTH / 2,
  y: GAME_SETTINGS.HEIGHT - 60,
  width: PLAYER_CONFIG.WIDTH,
  height: PLAYER_CONFIG.HEIGHT,
  color: PLAYER_CONFIG.COLOR,
  lives: PLAYER_CONFIG.INITIAL_LIVES,
  invincible: false,
  invincibleEndTime: 0,
  shrunk: false,
  shrinkEndTime: 0,
});

const createInitialEffects = (): ActiveEffects => ({
  shield: false,
  bombReady: false,
  pickupMessage: '',
  slowmo: false,
  slowmoEndTime: 0,
  turretActive: false,
  turretEndTime: 0,
});

const createInitialTimers = (): GameTimers => ({
  spawnObstacle: 0,
  spawnPowerup: 0,
  pickupMessageEndTime: 0,
});

const createInitialGameState = (): GameState => ({
  gameRunning: false,
  gamePaused: false,
  gameOver: false,
  score: 0,
  player: createInitialPlayer(),
  obstacles: [],
  powerups: [],
  bullets: [],
  particles: [],
  activeEffects: createInitialEffects(),
  timers: createInitialTimers(),
  combo: 0,
  maxCombo: 0,
  lastObstacleTime: 0,
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
        lastObstacleTime: Date.now(),
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

  const loseLife = useCallback(() => {
    setGameState(prev => {
      const newLives = prev.player.lives - 1;
      if (newLives <= 0) {
        return {
          ...prev,
          player: { ...prev.player, lives: 0 },
          gameRunning: false,
          gameOver: true,
        };
      }
      return {
        ...prev,
        player: {
          ...prev.player,
          lives: newLives,
          invincible: true,
          invincibleEndTime: Date.now() + PLAYER_CONFIG.INVINCIBILITY_DURATION,
        },
        combo: 0, // Reset combo on death
      };
    });
  }, []);

  const activateShield = useCallback(() => {
    setGameState(prev => ({
      ...prev,
      activeEffects: {
        ...prev.activeEffects,
        shield: true,
      },
    }));
  }, []);

  const deactivateShield = useCallback(() => {
    setGameState(prev => ({
      ...prev,
      activeEffects: {
        ...prev.activeEffects,
        shield: false,
      },
    }));
  }, []);

  const activateSlowmo = useCallback((duration: number) => {
    setGameState(prev => ({
      ...prev,
      activeEffects: {
        ...prev.activeEffects,
        slowmo: true,
        slowmoEndTime: Date.now() + duration,
      },
    }));
  }, []);

  const activateTurret = useCallback((duration: number) => {
    setGameState(prev => ({
      ...prev,
      activeEffects: {
        ...prev.activeEffects,
        turretActive: true,
        turretEndTime: Date.now() + duration,
      },
    }));
  }, []);

  const shrinkPlayer = useCallback((duration: number) => {
    setGameState(prev => ({
      ...prev,
      player: {
        ...prev.player,
        shrunk: true,
        shrinkEndTime: Date.now() + duration,
        width: PLAYER_CONFIG.WIDTH * 0.6,
        height: PLAYER_CONFIG.HEIGHT * 0.6,
      },
    }));
  }, []);

  const addBullet = useCallback((bullet: any) => {
    setGameState(prev => ({
      ...prev,
      bullets: [...prev.bullets, bullet],
    }));
  }, []);

  const addParticles = useCallback((particles: any[]) => {
    setGameState(prev => ({
      ...prev,
      particles: [...prev.particles, ...particles],
    }));
  }, []);

  const addObstacle = useCallback((obstacle: any) => {
    setGameState(prev => ({
      ...prev,
      obstacles: [...prev.obstacles, obstacle],
    }));
  }, []);

  const addPowerup = useCallback((powerup: any) => {
    setGameState(prev => ({
      ...prev,
      powerups: [...prev.powerups, powerup],
    }));
  }, []);

  const setPickupMessage = useCallback((message: string, duration: number) => {
    setGameState(prev => ({
      ...prev,
      activeEffects: {
        ...prev.activeEffects,
        pickupMessage: message,
      },
      timers: {
        ...prev.timers,
        pickupMessageEndTime: Date.now() + duration,
      },
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
    loseLife,
    activateShield,
    deactivateShield,
    activateSlowmo,
    activateTurret,
    shrinkPlayer,
    addBullet,
    addParticles,
    addObstacle,
    addPowerup,
    setPickupMessage,
  };
};