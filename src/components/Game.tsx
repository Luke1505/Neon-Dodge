'use client';

import React, { useRef, useEffect, useState, useCallback } from 'react';
import { GameState, GameScreen, MenuState, HighScore } from '@/types/game';
import { GAME_SETTINGS, COLORS } from '@/lib/constants';
import GameCanvas from './GameCanvas';
import MainMenu from './MainMenu';
import GameHUD from './GameHUD';
import PauseMenu from './PauseMenu';
import GameOverScreen from './GameOverScreen';
import InstructionsScreen from './InstructionsScreen';
import HighScoresScreen from './HighScoresScreen';
import { useGameState } from '@/hooks/useGameState';
import { useGameLoop } from '@/hooks/useGameLoop';
import { useHighScores } from '@/hooks/useHighScores';

const Game: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [menuState, setMenuState] = useState<MenuState>({
    currentScreen: 'menu',
    username: '',
    selectedLanguage: 'en',
  });

  const { gameState, initializeGame, resetGame, updatePlayer, togglePause } = useGameState();
  const { highScores, addHighScore, clearHighScores } = useHighScores();
  
  // Game loop
  useGameLoop(gameState, canvasRef);

  const handleStartGame = useCallback((username: string) => {
    setMenuState(prev => ({ ...prev, username, currentScreen: 'game' }));
    initializeGame();
  }, [initializeGame]);

  const handleGameOver = useCallback((finalScore: number) => {
    if (menuState.username && finalScore > 0) {
      addHighScore({
        username: menuState.username,
        score: finalScore,
        combo: gameState.maxCombo,
        timestamp: Date.now(),
      });
    }
    setMenuState(prev => ({ ...prev, currentScreen: 'gameOver' }));
  }, [menuState.username, gameState.maxCombo, addHighScore]);

  const handleBackToMenu = useCallback(() => {
    setMenuState(prev => ({ ...prev, currentScreen: 'menu' }));
    resetGame();
  }, [resetGame]);

  const handlePause = useCallback(() => {
    if (menuState.currentScreen === 'game') {
      togglePause();
      setMenuState(prev => ({ 
        ...prev, 
        currentScreen: gameState.gamePaused ? 'game' : 'paused' 
      }));
    }
  }, [menuState.currentScreen, gameState.gamePaused, togglePause]);

  const handleResume = useCallback(() => {
    setMenuState(prev => ({ ...prev, currentScreen: 'game' }));
    togglePause();
  }, [togglePause]);

  // Keyboard event handling
  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (menuState.currentScreen === 'game' && !gameState.gamePaused) {
        // Game controls are handled in the game loop
        if (event.key === 'p' || event.key === 'P') {
          event.preventDefault();
          handlePause();
        }
      } else if (menuState.currentScreen === 'paused') {
        if (event.key === 'p' || event.key === 'P') {
          event.preventDefault();
          handleResume();
        }
      }
      
      if (event.key === 'Escape') {
        event.preventDefault();
        if (menuState.currentScreen === 'game') {
          handlePause();
        } else if (menuState.currentScreen === 'paused') {
          handleBackToMenu();
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [menuState.currentScreen, gameState.gamePaused, handlePause, handleResume, handleBackToMenu]);

  // Check for game over
  useEffect(() => {
    if (gameState.gameOver && menuState.currentScreen === 'game') {
      handleGameOver(gameState.score);
    }
  }, [gameState.gameOver, gameState.score, menuState.currentScreen, handleGameOver]);

  const renderCurrentScreen = () => {
    switch (menuState.currentScreen) {
      case 'menu':
        return (
          <MainMenu
            onStartGame={handleStartGame}
            onShowInstructions={() => setMenuState(prev => ({ ...prev, currentScreen: 'instructions' }))}
            onShowHighScores={() => setMenuState(prev => ({ ...prev, currentScreen: 'highScores' }))}
            username={menuState.username}
            highScores={highScores}
          />
        );

      case 'instructions':
        return (
          <InstructionsScreen
            onBack={() => setMenuState(prev => ({ ...prev, currentScreen: 'menu' }))}
          />
        );

      case 'highScores':
        return (
          <HighScoresScreen
            highScores={highScores}
            onBack={() => setMenuState(prev => ({ ...prev, currentScreen: 'menu' }))}
            onClearScores={() => {
              clearHighScores();
            }}
          />
        );

      case 'game':
        return (
          <div className="relative w-full h-full">
            <GameCanvas
              ref={canvasRef}
              gameState={gameState}
              width={GAME_SETTINGS.WIDTH}
              height={GAME_SETTINGS.HEIGHT}
            />
            <GameHUD gameState={gameState} username={menuState.username} />
          </div>
        );

      case 'paused':
        return (
          <div className="relative w-full h-full">
            <GameCanvas
              ref={canvasRef}
              gameState={gameState}
              width={GAME_SETTINGS.WIDTH}
              height={GAME_SETTINGS.HEIGHT}
            />
            <PauseMenu
              onResume={handleResume}
              onRestart={() => {
                resetGame();
                initializeGame();
                setMenuState(prev => ({ ...prev, currentScreen: 'game' }));
              }}
              onMainMenu={handleBackToMenu}
            />
          </div>
        );

      case 'gameOver':
        return (
          <GameOverScreen
            score={gameState.score}
            maxCombo={gameState.maxCombo}
            username={menuState.username}
            onPlayAgain={() => {
              resetGame();
              initializeGame();
              setMenuState(prev => ({ ...prev, currentScreen: 'game' }));
            }}
            onMainMenu={handleBackToMenu}
            highScores={highScores}
          />
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-deep-space-black flex items-center justify-center p-4">
      <div 
        className="relative bg-deep-space-black border-2 border-neon-blue rounded-lg overflow-hidden game-container"
        style={{
          width: GAME_SETTINGS.WIDTH + 40,
          height: GAME_SETTINGS.HEIGHT + 40,
          maxWidth: '100vw',
          maxHeight: '100vh',
        }}
      >
        {renderCurrentScreen()}
      </div>
    </div>
  );
};

export default Game;