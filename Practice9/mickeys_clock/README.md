# Mickey's Clock

A Pygame clock that uses Mickey Mouse-style animated hands.

## How to Run

```bash
pip install pygame
python main.py
```

## Features
- Real-time clock synced to system time
- Right hand (minutes) and left hand (seconds) rotate smoothly
- Classic analogue face with tick marks and numbers
- Mickey Mouse body decoration at centre
- Digital time display at the bottom
- Press **Q** to quit

## Notes
- Minutes hand: smooth sweep (includes seconds contribution)
- Seconds hand: ticks every second
- Rotation uses `pygame.transform.rotate()` with pivot-correct blitting
