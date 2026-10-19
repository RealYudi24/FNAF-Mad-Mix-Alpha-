# 🎮 FNAF Mad Mix

### *A Five Nights at Freddy's Fan Game*

**Created by The Orange Guy** 🟠

Welcome to **FNAF Mad Mix**, an unofficial FNAF fan game built with Python and Pygame!

Enter the office, monitor security cameras, keep track of the animatronics, and survive the night. Stay alert, because you never know what might be waiting in the next room...

> 🚧 **Development Status: ALPHA**
>
> This project is a work in progress. Features, mechanics, and content may change as development continues.

---

## 📖 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [How to Play](#-how-to-play)
- [Controls](#-controls)
- [Project Structure](#-project-structure)
- [AI Disclosure](#-ai-disclosure)
- [Credits](#-credits)
- [Disclaimer](#-disclaimer)

---

## ✨ Features

- 📹 **Security Cameras** — Monitor different rooms and follow animatronic movements.
- 🤖 **Animatronics** — Encounter familiar characters, each with their own place in the game.
- 👻 **Animated Jumpscares** — Experience animated jumpscares and sudden surprises.
- 🔊 **Audio Effects** — Sound effects and music help bring the experience to life.
- 🖥️ **Office Gameplay** — Keep an eye on the cameras and try to survive.
- 🧪 **Testing Shortcuts** — Trigger certain jumpscares using keyboard shortcuts during gameplay.

More features may be introduced as development progresses.

## 🛠️ Requirements

The game was developed using **Python 3.10**.

### Python modules and libraries

| Module / Library | Purpose |
|---|---|
| `pygame` | Game window, graphics, keyboard input, and audio |
| `Pillow` (`PIL`) | Image processing |
| `random` | Random-number generation |
| `os` | Operating-system and file-path utilities |

`random` and `os` are included in Python's standard library and do not require separate installation.

`pygame` and `Pillow` are third-party packages that must be installed.

Python 3.10 is the development version used for this project. Other Python versions may work, but compatibility has not necessarily been tested.

## 🚀 Installation

### 1. Install Python

Download Python 3.10 from the official website:

https://www.python.org/downloads/release/python-3100/

During installation on Windows, enable **Add Python to PATH**.

### 2. Download the Repository

Download the repository as a ZIP file from GitHub and extract it.

Alternatively, clone it using Git:

```bash
git clone https://github.com/RealYudi24/FNAF-Mad-Mix-Alpha-
```


### 3. Install the Dependencies

Open a terminal inside the project folder and run:

```bash
python -m pip install pygame Pillow
```

### 4. Launch the Game

Run the following command from the project directory:

```bash
python main.py
```

That's it! You're ready to play. 🎉

**Important:** Keep the required images, audio files, and `assets` folder in their original locations. The game uses relative file paths, so moving or renaming required files may prevent it from launching correctly.

## 🕹️ How to Play

Your objective is simple: **survive the night.**

### 1. Start Your Shift

- Launch the game using the installation instructions.
- Click the **Start** button on the main menu.
- Wait for the night introduction to finish.

### 2. Check the Cameras

- Press `SPACE` to open or close the camera monitor.
- Use the number keys `1`–`9` to select camera feeds while the monitor is open.
- Check different rooms to keep track of animatronic movements.

### 3. Stay Alert

- Monitor the rooms regularly.
- Pay attention to visual changes and audio cues.
- Be ready for unexpected encounters!

### 4. Use Balloon Boy's Ability

Press `J` to activate Balloon Boy's ability during gameplay. The ability has a cooldown.

### 5. Survive Until Morning

Keep monitoring the situation and try to make it through the night. If an animatronic catches you, the game ends in a jumpscare.

> **Note:** This is an Alpha build. Some mechanics may be incomplete or change in later versions.

## 🎮 Controls

| Input | Action |
|---|---|
| Mouse click | Start the game using the Start button |
| `SPACE` | Open or close the camera monitor |
| `1`–`9` | Switch camera feeds while the monitor is open |
| `J` | Activate Balloon Boy's ability |
| `Z` | Test Ballora's jumpscare |
| `X` | Test Mangle's jumpscare |
| `C` | Test Springtrap's jumpscare |
| `V` | Test Toy Bonnie's jumpscare |
| `B` | Test Toy Chica's jumpscare |
| `N` | Test Toy Freddy's jumpscare |
| `G` | Test Golden Freddy's jumpscare |

### 🧪 Testing Shortcuts

The jumpscare shortcuts are intended for testing and work during gameplay when the camera monitor is closed. They are not necessary for normal gameplay.

## 📁 Project Structure

The repository is organized approximately as follows:

```text
FNAF-Mad-Mix/
├── main.py
├── jj.jpg
├── menu.ogg
├── op.png
├── start.mp3
└── assets/
    ├── office.jpg
    ├── ANIM/
    │   └── Animatronic images
    ├── audio/
    │   └── Sound effects and audio
    ├── jumpscares/
    │   └── Jumpscare animations
    └── MAP/
        ├── Bathroom/
        ├── Dining Area/
        ├── Entrance/
        ├── Kid's Cove/
        ├── Kitchen/
        ├── Party Room/
        ├── Prize Corner/
        ├── Spare/
        └── Stage/
```

*The directory tree above is simplified for readability; the folders contain the actual game assets.*

## 🤖 AI Disclosure

AI tools were used as assistants during the development of FNAF Mad Mix.

Depending on the component, AI-assisted work may include coding support, debugging assistance, development guidance, or help with assets.

The project combines original development work with AI-assisted contributions. AI involvement may vary between individual components.

## 👨‍💻 Credits

**Creator and Developer:** The Orange Guy 🟠

**Game Engine:** Pygame

**Programming Language:** Python

**Image Processing:** Pillow

Additional assets may have their own respective creators and rights holders. See the disclaimer below.

## ⚠️ Disclaimer

FNAF Mad Mix is an **unofficial, fan-made project** and is not affiliated with, endorsed by, or an official product of Scott Cawthon or the official Five Nights at Freddy's rights holders.

Five Nights at Freddy's, its characters, names, and associated intellectual property belong to their respective rights holders.

Third-party images, music, sound effects, and other assets may be owned by their respective creators. Their inclusion in this project does not imply ownership. Please verify the applicable permissions and licenses before redistributing the game or its assets.

## 🚧 Future Development

FNAF Mad Mix is currently in Alpha. Bugs, incomplete mechanics, and changes are expected.

This repository documents the development of the project as it grows.

Thanks for checking out **FNAF Mad Mix**!

## QUICK NOTE
You can change ai levels and all from the code only (well i think ya'll knew but still its my job to tell :D)

**— The Orange Guy 🟠**
