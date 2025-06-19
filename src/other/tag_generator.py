import random
import nltk

# Download word list if you haven't before
nltk.download('words')

from nltk.corpus import words

def generate_words_file(filename, word_count=100000):
    word_list = words.words()
    with open(filename, 'w') as f:
        for _ in range(word_count):
            choice = random.choice(word_list)
            if len(choice) > 3 and len(choice) < 10:
                # Ensure the word is at least 4 characters long
                f.write(choice.lower() + '\n')
            

if __name__ == "__main__":
    generate_words_file("random_words.txt")
    print("Generated 'random_words.txt' with 10,000 random real English words.")
