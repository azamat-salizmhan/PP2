# Practice 9 – Pygame Games

Three classic Pygame mini-projects:

| Project | Description |
|---------|-------------|
| `mickeys_clock/` | Analogue clock with Mickey Mouse-style hands |
| `music_player/`  | Keyboard-controlled music player |
| `moving_ball/`   | Red ball that moves with arrow keys |

## Setup

```bash
pip install -r requirements.txt
```

## Run each project

```bash
# Mickey's Clock
cd mickeys_clock && python main.py

# Music Player
cd music_player && python main.py

# Moving Ball
cd moving_ball && python main.py
```

## Repository Structure

```
Practice9/
├── mickeys_clock/
│   ├── main.py
│   ├── clock.py
│   ├── images/
│   │   └── mickey_hand.png
│   └── README.md
├── music_player/
│   ├── main.py
│   ├── player.py
│   ├── music/           ← put your .mp3/.wav/.ogg files here
│   └── README.md
├── moving_ball/
│   ├── main.py
│   ├── ball.py
│   └── README.md
├── requirements.txt
└── README.md
```

## GitHub

```bash
git add .
git commit -m "Add Practice9 - Pygame games: Mickey's clock, music player, moving ball"
git push origin main
```
