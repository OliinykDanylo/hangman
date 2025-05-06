import random
import os
import platform
from colorama import init, Fore, Style
import pygame
import json

init(autoreset=True)

try:
    pygame.mixer.init()
except Exception as e:
    print(Fore.YELLOW + f"Failed to initialize audio: {e}")

MAX_ATTEMPTS = 6
STATS_FILE = "stats.txt"

HANGMAN_PICS = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    ========="""
]

def play_sound(filename):
    if not pygame.mixer.get_init():
        return
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
    except:
        pass

def colorize_hangman(pic, incorrect_guesses, max_attempts):
    colors = [Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.YELLOW, Fore.RED, Fore.LIGHTRED_EX]
    color = colors[min(incorrect_guesses, len(colors) - 1)]
    return color + pic + Style.RESET_ALL

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def load_words(file_path):
    if not os.path.exists(file_path):
        return ["python", "hangman", "challenge", "programming", "function"]
    with open(file_path, "r") as file:
        words = [line.strip().lower() for line in file if line.strip()]
    return words if words else ["python", "hangman", "challenge", "programming", "function"]

def choose_word(word_list):
    return random.choice(word_list)

def display_word(secret_word, guessed_letters):
    return ' '.join(letter if letter in guessed_letters else '_' for letter in secret_word)

def get_guess(guessed_letters):
    while True:
        guess = input("Enter a letter or full word (or 'exit'): ").lower()
        if guess == "exit":
            print("Exiting game...")
            exit()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("Already guessed.")
            else:
                return guess
        elif guess.isalpha():
            return guess
        else:
            print("Invalid input.")

def select_difficulty():
    difficulties = {
        "easy": ("easy.txt", "easy"),
        "intermediate": ("intermediate.txt", "intermediate"),
        "hard": ("hard.txt", "hard")
    }
    while True:
        choice = input("Select difficulty (easy, intermediate, hard): ").lower()
        if choice in difficulties:
            file_name, level = difficulties[choice]
            return load_words(file_name), level
        print("Invalid difficulty.")

def load_stats():
    if not os.path.exists("stats.txt") or os.path.getsize("stats.txt") == 0:
        return {}
    try:
        with open("stats.txt", "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(Fore.RED + "Corrupted stats.txt file. Starting fresh.")
        return {}

def save_stats(stats):
    with open(STATS_FILE, "w") as file:
        json.dump(stats, file, indent=4)

def login_or_signup():
    stats = load_stats()
    print("If you have played before, enter your username and password.")
    print("If not, create a new profile.")
    while True:
        username = input("Username: ")
        password = input("Password: ")
        user = stats.get(username)
        if user:
            if user["password"] == password:
                print(f"Welcome back, {username}!")
                return username, stats
            else:
                print("Incorrect password.")
        else:
            print("New user. Creating profile...")
            stats[username] = {
                "password": password,
                "easy": {"wins": 0, "losses": 0},
                "intermediate": {"wins": 0, "losses": 0},
                "hard": {"wins": 0, "losses": 0}
            }
            save_stats(stats)
            print(f"Profile created for {username}.")
            return username, stats

def update_stats(stats, username, difficulty, won):
    stats[username][difficulty]["wins" if won else "losses"] += 1
    save_stats(stats)

def play_game(word_list, max_attempts, username, stats, difficulty):
    secret_word = choose_word(word_list)
    guessed_letters = []
    incorrect_guesses = 0

    while incorrect_guesses < max_attempts:
        print(colorize_hangman(HANGMAN_PICS[min(incorrect_guesses, len(HANGMAN_PICS) - 1)], incorrect_guesses, max_attempts))
        print(f"\nWord: {display_word(secret_word, guessed_letters)}")
        print(f"Guessed letters: {' '.join(guessed_letters)}")
        print(f"Remaining attempts: {max_attempts - incorrect_guesses}")

        guess = get_guess(guessed_letters)
        clear_screen()

        if len(guess) == 1:
            guessed_letters.append(guess)
            if guess in secret_word:
                play_sound("correct.wav")
                print(Fore.GREEN + "Correct!")
            else:
                play_sound("wrong.mp3")
                print(Fore.LIGHTRED_EX + "Wrong!")
                incorrect_guesses += 1
        else:
            if guess == secret_word:
                play_sound("correct.wav")
                print(Fore.GREEN + f"You guessed it! The word was: {secret_word}")
                update_stats(stats, username, difficulty, True)
                return
            else:
                play_sound("wrong.mp3")
                print(Fore.LIGHTRED_EX + "Wrong word!")
                incorrect_guesses += 1

        if all(letter in guessed_letters for letter in secret_word):
            print(Fore.GREEN + f"\nYou guessed it! The word was: {secret_word}")
            update_stats(stats, username, difficulty, True)
            return

    print(Fore.LIGHTRED_EX + f"\nGame over! The word was: {secret_word}")
    update_stats(stats, username, difficulty, False)

def main():
    clear_screen()
    username, stats = login_or_signup()
    while True:
        word_list, difficulty = select_difficulty()
        clear_screen()
        play_game(word_list, MAX_ATTEMPTS, username, stats, difficulty)

        replay = input("\nPlay again? (y/n): ").lower()
        if replay != 'y':
            print("Thanks for playing Hangman!")
            break

if __name__ == "__main__":
    main()
