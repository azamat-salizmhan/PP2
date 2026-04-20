# Practice 11 - Pygame Projects (Extended)

This folder contains extended versions of the Pygame projects from Practice 10.

---

## 1. Racer Game

Extended with weighted coins and enemy speed increase.

### New Features
- **Weighted Coins**: Three types of coins with different values:
  - Bronze (Brown): Weight 1, most common (60%)
  - Silver (Gray): Weight 2, medium (30%)
  - Gold (Yellow): Weight 3, rare (10%)
- **Enemy Speed Boost**: Every N coins collected, enemy speed increases
- **Total Value Display**: Shows cumulative value of collected coins
- **Enemy Speed Display**: Shows current enemy speed

### How to Play
```bash
cd racer
python racer.py
```
- Use **Arrow Keys** or **WASD** to move
- Collect coins (higher weight = more points toward speed boost)
- Enemy speeds up every 5 coins collected
- Press **R** to restart, **ESC** to quit

---

## 2. Snake Game

Extended with weighted food and disappearing food timer.

### New Features
- **Weighted Food**: Three types with different points:
  - Small (Green): 5 points, lasts 10 seconds
  - Medium (Yellow): 10 points, lasts 7 seconds
  - Large (Red): 15 points, lasts 5 seconds
- **Timer Bar**: Visual timer bar above food showing time remaining
- **Food Info**: Displays current food type and remaining time
- Food disappears when timer expires and respawns elsewhere

### How to Play
```bash
cd snake
python snake.py
```
- Use **Arrow Keys** or **WASD** to move
- Eat food before timer runs out
- Higher value food disappears faster
- Press **R** to restart, **ESC** to quit

---

## 3. Paint Application

Extended with new geometric shapes.

### New Features
- **Square Tool**: Draw perfect squares (equal sides)
- **Right Triangle**: Draw right-angled triangles
- **Equilateral Triangle**: Draw triangles with all equal sides
- **Rhombus Tool**: Draw diamond shapes (equal sides, angled corners)
- All shapes maintain proportions while dragging

### Tools Available
1. **Brush**: Freehand drawing
2. **Rectangle**: Regular rectangles
3. **Square**: Perfect squares
4. **Circle**: Circles
5. **Right Triangle**: 90-degree angle triangles
6. **Equilateral Triangle**: 60-degree angle triangles
7. **Rhombus**: Diamond/rhombus shape
8. **Eraser**: Remove drawings
9. **Clear**: Clear entire canvas

### How to Use
```bash
cd paint
python paint.py
```
- Select a tool from the bottom toolbar
- Select a color from the color palette
- Click and drag on canvas to draw shapes
- Press **ESC** to quit

### Shape Drawing Tips
- **Square**: Drag diagonally to set size
- **Circle**: Drag to set radius
- **Triangles**: Drag to set base and height
- **Rhombus**: Drag diagonally to set size

---

## Requirements

All projects require Pygame:

```bash
pip install pygame
```

## File Structure

```
practice11/
├── racer/
│   └── racer.py
├── snake/
│   └── snake.py
├── paint/
│   └── paint.py
└── readme.md
```

## Code Comments

All files include detailed comments explaining:
- Class and method purposes
- Game mechanics
- Feature implementations
- Constants and settings

---

*Extended projects for Python programming practice.*
