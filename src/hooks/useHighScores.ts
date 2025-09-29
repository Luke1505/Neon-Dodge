'use client';

import { useState, useEffect, useCallback } from 'react';
import { HighScore } from '@/types/game';

const HIGH_SCORE_CONFIG = {
  STORAGE_KEY: 'neon-dodge-high-scores',
  MAX_ENTRIES: 10,
};

export const useHighScores = () => {
  const [highScores, setHighScores] = useState<HighScore[]>([]);

  // Load high scores from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(HIGH_SCORE_CONFIG.STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        setHighScores(Array.isArray(parsed) ? parsed : []);
      }
    } catch (error) {
      console.error('Failed to load high scores:', error);
      setHighScores([]);
    }
  }, []);

  // Save high scores to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem(HIGH_SCORE_CONFIG.STORAGE_KEY, JSON.stringify(highScores));
    } catch (error) {
      console.error('Failed to save high scores:', error);
    }
  }, [highScores]);

  const addHighScore = useCallback((newScore: HighScore) => {
    setHighScores(prev => {
      const updated = [...prev, newScore];
      // Sort by score (descending), then by combo (descending)
      updated.sort((a, b) => {
        if (a.score !== b.score) {
          return b.score - a.score;
        }
        return (b.combo || 0) - (a.combo || 0);
      });
      // Keep only top scores
      return updated.slice(0, HIGH_SCORE_CONFIG.MAX_ENTRIES);
    });
  }, []);

  const getTopScore = useCallback((): number => {
    return highScores.length > 0 ? highScores[0].score : 0;
  }, [highScores]);

  const isHighScore = useCallback((score: number): boolean => {
    if (highScores.length < HIGH_SCORE_CONFIG.MAX_ENTRIES) {
      return true;
    }
    return score > highScores[highScores.length - 1].score;
  }, [highScores]);

  const clearHighScores = useCallback(() => {
    setHighScores([]);
  }, []);

  return {
    highScores,
    addHighScore,
    getTopScore,
    isHighScore,
    clearHighScores,
  };
};