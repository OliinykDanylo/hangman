# 🎮 Terminal Hangman Game

A colorful, feature-rich Hangman game playable in the terminal. Supports multiple difficulty levels, user login/signup, persistent stats tracking, ASCII art, and sound effects!

---

## 📜 Project Description

This is a terminal-based Hangman game built with Python. It includes:

- 🧠 **Three difficulty levels**: Easy, Intermediate, and Hard — each with its own word list
- 🧍 **User login/signup system** — with username and password
- 📊 **Persistent stats tracking** — per user and difficulty level, stored in `stats.txt`
- 🎨 **Colorful terminal output** — thanks to `colorama`
- 🔊 **Sound effects** — for correct and incorrect guesses (optional)
- 🔡 **Support for full word or letter guessing**
- 🚫 **Handles corrupted or missing files**

---

## ▶️ How to Run the Game

### 1. 🛠️ Install Requirements

Make sure Python 3 is installed, then install the dependencies:

```bash
pip install colorama pygame

2. 📂 Prepare Word Lists

Create the following files (one word per line) in the project directory:
	•	easy.txt
	•	intermediate.txt
	•	hard.txt

If these files are missing or empty, default words will be used.

3. 🔊 Add Optional Sound Files

Place the following sound files in the same directory as game.py:
	•	correct.wav — played when the user guesses correctly
	•	wrong.mp3 — played when the user guesses incorrectly

⚠️ If sound files are missing or cannot be loaded, the game will continue without sound.

4. 🚀 Run the Game

Run the game using:

python game.py

⸻

🌟 Features
	•	✅ User login and signup system (username + password)
	•	✅ Per-user stats saved in stats.txt (in JSON format)
	•	✅ Supports 3 difficulty levels with custom word lists
	•	✅ ASCII art hangman updated with each wrong guess
	•	✅ Colored output for better visual feedback
	•	✅ Sound effects for feedback (optional)
	•	✅ Guess full word or one letter at a time
	•	✅ Graceful handling of corrupted/missing files