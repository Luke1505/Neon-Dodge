# 🎮 Neon Dodge - Web Game

A vibrant neon-themed dodge game built with React, Next.js, and TypeScript. Originally converted from a Python/pygame version to run in the browser with enhanced features and modern web technologies.

![Neon Dodge Main Menu](https://github.com/user-attachments/assets/4edf2d44-fbf7-4cb1-bca8-915135ac8211)

![Neon Dodge Gameplay](https://github.com/user-attachments/assets/6dece58b-4591-4409-8f44-fc0f1da6b73a)

## 🌟 Features

### Core Gameplay
- **Dodge Mechanics**: Navigate through colorful obstacles using smooth controls
- **Power-up System**: Collect 6 different power-ups with unique abilities
- **Combo System**: Build combos by dodging consecutive obstacles for higher scores
- **Progressive Difficulty**: Game speed and obstacle density increase over time
- **Lives System**: Start with 3 lives, collect extra lives via power-ups

### Power-ups
- 🛡️ **Shield** (Green): One-hit protection
- ⏱️ **SlowMo** (Yellow): Slows obstacles for 5 seconds
- 💥 **Bomb** (Magenta): Clears all obstacles from screen
- 🔹 **Shrink** (Purple): Player becomes smaller and faster for 10 seconds
- 💚 **Extra Life** (Blue): Grants an additional life
- 🎯 **Turret** (Grey): Auto-shoots obstacles for 10 seconds

### Visual Effects
- **Neon Glow**: All game elements have vibrant neon glow effects
- **Starfield Background**: Dynamic scrolling starfield
- **Particle System**: Explosion effects when obstacles are destroyed
- **Pulsing Power-ups**: Power-ups pulse to attract attention
- **Invincibility Flashing**: Player flashes when invincible

### Modern Features
- **Responsive Design**: Works on desktop and mobile devices
- **Touch Controls**: Full touch support for mobile gaming
- **Local High Scores**: Persistent leaderboard stored in browser
- **Achievements**: Visual badges for different accomplishments
- **Statistics**: Track best scores, combos, and averages

## 🎯 How to Play

### Controls
- **Movement**: Arrow Keys or WASD
- **Pause**: P key
- **Menu**: ESC key
- **Touch**: Tap and hold to move on mobile devices

### Objective
Survive as long as possible by dodging obstacles and collecting power-ups to achieve the highest score!

### Scoring System
- **Survival Time**: +1 point per 0.1 seconds
- **Power-ups**: +10 points + combo bonus
- **Combo Bonus**: Additional points based on consecutive dodges
- **Shooting Obstacles**: +15 points per obstacle destroyed

## 🛠️ Technology Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom neon effects
- **Rendering**: HTML5 Canvas with 2D Context
- **Game Loop**: RequestAnimationFrame for smooth 60fps gameplay
- **State Management**: React hooks with TypeScript
- **Persistence**: localStorage for high scores

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Luke1505/Neon-Dodge.git
   cd Neon-Dodge
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
npm start
```

## 📱 Mobile Support

The game is fully optimized for mobile devices with:
- Touch controls for player movement
- Responsive UI that adapts to screen size
- Optimized performance for mobile browsers
- PWA-ready for installation on mobile devices

## 🎨 Design Philosophy

### Neon Aesthetic
- High contrast colors for visibility
- Glowing effects for immersion
- Dark space background for focus
- Vibrant color palette inspired by 80s neon

### User Experience
- Intuitive controls
- Clear visual feedback
- Smooth animations
- Accessible design

## 🔧 Development

### Project Structure
```
src/
├── app/                 # Next.js app router
├── components/          # React components
│   ├── Game.tsx        # Main game component
│   ├── GameCanvas.tsx  # Canvas rendering
│   ├── MainMenu.tsx    # Menu screens
│   └── ...
├── hooks/              # Custom React hooks
├── lib/                # Game engine and utilities
├── types/              # TypeScript type definitions
└── styles/             # Global styles
```

### Game Engine
The game engine (`src/lib/gameEngine.ts`) handles:
- Game loop and state updates
- Collision detection
- Rendering pipeline
- Input handling (keyboard + touch)
- Physics simulation

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📈 Performance

- **60 FPS** gameplay on modern devices
- **Optimized rendering** with canvas 2D context
- **Efficient collision detection** 
- **Memory management** for particles and game objects
- **Mobile optimization** for touch devices

## 🎵 Future Enhancements

- [ ] Sound effects and background music
- [ ] Online leaderboards
- [ ] Multiple game modes
- [ ] Custom themes and skins
- [ ] Achievement system
- [ ] Social sharing features
- [ ] Gamepad support

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original Python/pygame version inspiration
- Neon aesthetic inspired by retro arcade games
- Built with modern web technologies for maximum compatibility

## 🐛 Bug Reports

If you find any bugs or have suggestions for improvements, please open an issue on GitHub.

---

**Enjoy playing Neon Dodge! 🎮✨**