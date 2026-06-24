# IPTV Modern Player

Modern IPTV Player built with **Python**, **PyQt6**, and **MPV**.

Designed for fast playlist loading, smooth playback, category management, and advanced stream controls with a modern desktop experience.


<img width="948" height="496" alt="Screenshot 2026-06-16 035250" src="https://github.com/user-attachments/assets/55cc78fc-736e-4144-af4f-9e972905e0e3" />


---

## Features

- 📺 Load local M3U playlists
- 🌐 Load remote M3U URLs
- 🎬 Play direct media streams
- 🔍 Real-time channel search
- 🗂 Automatic channel categorization
- ⚡ MPV hardware accelerated playback
- 🎞 Dynamic quality selection for HLS streams
- 📝 Subtitle track support
- 🔊 Audio track switching
- ⛶ Fullscreen mode
- ⌨ Keyboard shortcuts
- 🎨 Modern dark interface
- 🚀 Multi-threaded playlist loading
- 📡 Support for M3U, M3U8, MP4, MKV, AVI, TS and MP3 streams

---

## Why IPTV Modern Player?

Most IPTV players are either outdated, bloated, or lack advanced playback controls.

IPTV Modern Player focuses on:

- Fast startup
- Responsive user interface
- Clean channel organization
- MPV-powered playback reliability
- Easy playlist management
- Modern desktop experience

---

## Requirements

- Python 3.10+
- Windows 10 / Windows 11
- MPV Runtime Libraries

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/IPTV-Modern-Player.git
cd IPTV-Modern-Player
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Dependencies

```txt
PyQt6
python-mpv
requests
urllib3
```

---

## MPV Runtime (Required)

This project uses the Python MPV bindings for media playback.

Required runtime DLL files must be placed next to the executable or source files.

Download MPV runtime files from:

https://github.com/jaseg/python-mpv

or

https://mpv.io

Required files:

```text
mpv-2.dll
libwinpthread-1.dll
```

Example structure:

```text
project/
│
├── main.py
├── mpv-2.dll
├── libwinpthread-1.dll
└── ...
```

For packaged builds:

```text
dist/
│
├── IPTVModernPlayer.exe
├── mpv-2.dll
└── libwinpthread-1.dll
```

---

## Running

Start the application:

```bash
python main.py
```

---

## Usage

### Load Local Playlist

1. Click **Load M3U**
2. Select your playlist file
3. Choose a category
4. Select a channel

### Load Playlist URL

1. Paste playlist URL
2. Click Play
3. Browse channels

### Direct Stream Playback

Supported examples:

```text
https://example.com/live.m3u8
https://example.com/video.mp4
```

---

## Keyboard Shortcuts

| Key | Action |
|-------|----------|
| Space | Play / Pause |
| F | Toggle Fullscreen |
| Esc | Exit Fullscreen |
| → | Next Channel |
| ← | Previous Channel |
| ↑ | Volume Up |
| ↓ | Volume Down |
| M | Mute / Unmute |

---

## Supported Formats

### Playlists

```text
.m3u
.m3u8
```

### Streams

```text
HLS
HTTP
HTTPS
```

### Media

```text
MP4
MKV
AVI
TS
MP3
```

---

## Project Structure

```text
.
├── config/
├── controllers/
├── managers/
├── models/
├── repositories/
├── services/
├── threads/
├── ui/
│   ├── styles/
│   ├── widgets/
│   └── windows/
├── utils/
├── app.py
├── main.py
└── requirements.txt
```

---

## Architecture

```text
Application
│
├── UI Layer
│
├── Controllers
│
├── Services
│
├── Managers
│
├── Repository
│
└── MPV Engine
```

### Controllers

- PlayerController
- PlaylistController
- SearchController
- SettingsController
- FullscreenController
- KeyboardController

### Services

- PlaylistService
- ParserService
- NetworkService
- SubtitleService

### Managers

- MPVManager
- ThreadManager

### Repository

- PlaylistRepository

---

## Building

Create a standalone executable using PyInstaller:

```bash
pyinstaller --noconfirm --onefile --windowed main.py
```

Output:

```text
dist/
└── IPTVModernPlayer.exe
```

Place MPV runtime DLL files beside the executable before distribution.

---

## Roadmap

- [x] M3U Playlist Support
- [x] HLS Stream Playback
- [x] Subtitle Support
- [x] Audio Track Selection
- [x] Quality Switching
- [x] Fullscreen Mode
- [x] Channel Search
- [ ] Favorites System
- [ ] Playlist History
- [ ] EPG Support
- [ ] Multi-language Interface

---

## Credits

### MPV

https://mpv.io

### Python MPV

https://github.com/jaseg/python-mpv

### PyQt6

https://www.riverbankcomputing.com/software/pyqt/

---

## License

MIT License

---

## Support

If you find this project useful, consider giving it a ⭐ on GitHub.
