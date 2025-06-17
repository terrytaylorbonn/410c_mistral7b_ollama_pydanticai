# find_files_with_phrase.py

# CPLT51
import os
import requests
import json

def find_files_with_phrase(directory, phrase):
    matches = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".txt", ".md", ".py", ".json")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if phrase.lower() in content.lower():
                            matches.append(path)
                except Exception as e:
                    print(f"Error reading {path}: {e}")
    return matches

def summarize_with_ollama(text, phrase, word_count):
    prompt = f"Summarize the following document in about {word_count} words, focusing on the topic: '{phrase}'.\n\n{text}"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt},
        stream=True
    )
    summary = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                summary += data.get("response", "")
            except Exception:
                continue
    return summary if summary else "[No summary returned]"

if __name__ == "__main__":
    search_phrase = input("Enter the word or phrase to search for: ")
    word_count = input("Enter the desired number of words for the summary (e.g., 50): ")
    try:
        word_count = int(word_count)
    except ValueError:
        word_count = 50
    directory = "./data"
    result = find_files_with_phrase(directory, search_phrase)
    if result:
        print("\nFiles containing the phrase:")
        for path in result:
            print(path)
        print("\nSummaries:")
        for path in result:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            summary = summarize_with_ollama(content[:4000], search_phrase, word_count)  # Truncate if too long
            print(f"\n--- {path} ---\n{summary}\n")
    else:
        print("No files found containing the phrase.")
