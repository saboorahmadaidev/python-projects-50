import random

words = ["PYTHON", "HANGMAN", "DEVELOPER", "PROGRAMMING", "COMPUTER", "KEYBOARD"]
word = random.choice(words)

total_chances = 6
guessed_letters = ["_"] * len(word)
used_letters = set()

print("🎮 Welcome to Hangman!")
print("Word:", " ".join(guessed_letters))

while total_chances > 0 and "_" in guessed_letters:
    
    letter = input("Guess a letter: ").upper()

    if len(letter) != 1 or not letter.isalpha():
        print("⚠️ Please enter a single alphabet letter.")
        continue

    if letter in used_letters:
        print("⚠️ You already guessed that letter.")
        continue

    used_letters.add(letter)

    if letter in word:
        print("✅ Correct guess!")
        for i in range(len(word)):
            if word[i] == letter:
                guessed_letters[i] = letter
    else:
        total_chances -= 1
        print(f"❌ Wrong guess! {total_chances} chances left.")

    print("Word:", " ".join(guessed_letters))
    print("Used letters:", ", ".join(sorted(used_letters)))
    print("-" * 30)

if "_" not in guessed_letters:
    print("🎉 Congratulations! You guessed the word:", word)
else:
    print("💀 You lost! The word was:", word)
