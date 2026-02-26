import os
import string
from difflib import SequenceMatcher


def clean_text(text):
    """Lowercase + remove punctuation"""
    text = text.lower()
    return text.translate(str.maketrans("", "", string.punctuation))


def calculate_similarity(file1, file2):
    base_dir = os.path.dirname(__file__)
    path1 = os.path.join(base_dir, file1)
    path2 = os.path.join(base_dir, file2)

    try:
        with open(path1, "r", encoding="utf-8") as f1, \
             open(path2, "r", encoding="utf-8") as f2:

            data_file1 = clean_text(f1.read())
            data_file2 = clean_text(f2.read())

    except FileNotFoundError as e:
        print(" File not found:", e)
        return

    words1 = data_file1.split()
    words2 = data_file2.split()

    matcher = SequenceMatcher(None, words1, words2)
    similarity_ratio = matcher.ratio() * 100

    print("\n========== Plagiarism Report ==========")
    print(f"File 1: {file1}")
    print(f"File 2: {file2}")
    print(f"\nSimilarity Percentage: {similarity_ratio:.2f}%")

    if similarity_ratio >= 70:
        print(" High chance of plagiarism detected!")
    elif similarity_ratio >= 40:
        print(" Moderate similarity detected.")
    else:
        print("✅ Low similarity. Likely original content.")

    print("\nMatched Text Segments:\n")

    for block in matcher.get_matching_blocks():
        if block.size > 5:  
            matched_words = words1[block.a:block.a + block.size]
            print(" ".join(matched_words))
            print("----------------------------------")


if __name__ == "__main__":
    calculate_similarity("demo.txt", "demo1.txt")