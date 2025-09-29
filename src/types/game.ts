export interface Position {
  x: number;
  y: number;
}

export interface TrailPoint extends Position {
  alpha: number;
}

export interface Player extends Position {
  size: number;
  color: string;
  trail?: TrailPoint[];
}

export interface Obstacle extends Position {
  size: number;
  speed: number;
  color: string;
  health: number;
}

export interface PowerUp extends Position {
  size: number;
  type: PowerUpType;
  color: string;
  pulsePhase: number;
}

export type PowerUpType = 'shield' | 'slowmo' | 'bomb' | 'shrink' | 'extraLife' | 'turret';

export interface Particle extends Position {
  vx: number;
  vy: number;
  size: number;
  color: string;
  alpha: number;
  life: number;
}

export interface Bullet extends Position {
  speed: number;
  size: number;
  color: string;
}

export interface ActiveEffects {
  shield: boolean;
  slowmo: boolean;
  shrink: boolean;
  turret: boolean;
  shieldEndTime?: number;
  slowmoEndTime?: number;
  shrinkEndTime?: number;
  turretEndTime?: number;
}

export interface GameState {
  gameRunning: boolean;
  gamePaused: boolean;
  gameOver: boolean;
  score: number;
  lives: number;
  timeElapsed: number;
  player: Player;
  obstacles: Obstacle[];
  powerUps: PowerUp[];
  bullets: Bullet[];
  particles: Particle[];
  activeEffects: ActiveEffects;
  combo: number;
  maxCombo: number;
  lastBulletTime?: number;
  powerUpsCollected: number;
}

export interface HighScore {
  username: string;
  score: number;
  combo?: number;
  timestamp?: number;
}

export interface GameStats {
  totalObstaclesDodged: number;
  totalPowerupsCollected: number;
  maxComboAchieved: number;
  timeAlive: number;
}

export type GameScreen = 'menu' | 'game' | 'paused' | 'gameOver' | 'instructions' | 'highScores';

export interface MenuState {
  currentScreen: GameScreen;
  username: string;
  selectedLanguage: string;
}