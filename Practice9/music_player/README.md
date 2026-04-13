# Music Player with Keyboard Controller

A Pygame music player that supports full keyboard control.

## How to Run

```bash
pip install pygame
python main.py
```

## Adding Your Own Music
Place `.mp3`, `.wav`, or `.ogg` files in the `music/` folder.  
If the folder is empty, three short demo sine-wave tones are generated automatically.

## Keyboard Controls

| Key | Action |
|-----|--------|
| **P** | Play current track |
| **S** | Stop playback |
| **N** | Next track |
| **B** | Previous (Back) track |
| **Q** | Quit |

## Features
- Auto-advances to next track when a track ends
- Playlist display with current track highlighted
- Playing / Stopped status indicator
- Playback position timer
- Demo tracks auto-generated if music folder is empty
