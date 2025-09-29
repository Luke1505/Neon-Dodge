export interface GameSettings {
  WIDTH: number;
  HEIGHT: number;
  PLAYER_SPEED: number;
  OBSTACLE_BASE_SPEED: number;
  POWERUP_SPAWN_INTERVAL: number;
}

export interface Position {
  x: number;
  y: number;
}

export interface Size {
  width: number;
  height: number;
}

export interface GameObject extends Position, Size {
  color: string;
  speed?: number;
}

export interface Player extends GameObject {
  lives: number;
  invincible: boolean;
  invincibleEndTime: number;
  shrunk: boolean;
  shrinkEndTime: number;
}

export interface Obstacle extends GameObject {
  generation: number;
  canSplit: boolean;
  numSplits: number;
}

export interface PowerUp extends GameObject {
  type: PowerUpType;
}

export type PowerUpType = 'shield' | 'slowmo' | 'bomb' | 'shrink' | 'extralife' | 'turret';

export interface Particle extends Position {
  velocityX: number;
  velocityY: number;
  life: number;
  maxLife: number;
  color: string;
  size: number;
}

export interface Bullet extends GameObject {
  isCompanion?: boolean;
}

export interface ActiveEffects {
  shield: boolean;
  bombReady: boolean;
  pickupMessage: string;
  slowmo: boolean;
  slowmoEndTime: number;
  turretActive: boolean;
  turretEndTime: number;
}

export interface GameTimers {
  spawnObstacle: number;
  spawnPowerup: number;
  pickupMessageEndTime: number;
}

export interface GameState {
  gameRunning: boolean;
  gamePaused: boolean;
  gameOver: boolean;
  score: number;
  player: Player;
  obstacles: Obstacle[];
  powerups: PowerUp[];
  bullets: Bullet[];
  particles: Particle[];
  activeEffects: ActiveEffects;
  timers: GameTimers;
  combo: number;
  maxCombo: number;
  lastObstacleTime: number;
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