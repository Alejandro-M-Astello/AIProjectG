# Import the built-in module for working with folders and file paths
import os

# Import for writing structured JSON files
import json

# Import the local Ollama Python client to communicate with the local LLM server
import ollama

# Import PdfReader from pypdf to extract raw text from PDF pages
from pypdf import PdfReader

# Import BaseModel from pydantic to enforce a strict JSON schema on the AI's output
from pydantic import BaseModel

# Define the input folder where users place their PDF lecture slides or notes
SLIDES_DIR = "slides"
# Define the output folder where generated flashcard decks are stored
FLASHCARDS_DIR = "flashcards"
# Define the full path to the generated JSON flashcard deck file
DECK_FILE = os.path.join(FLASHCARDS_DIR, "deck.json")

# Define the structure of a single flashcard (requires a question string and an answer string)
class Flashcard(BaseModel):
    question: str
    answer: str

# Define the wrapper structure expected from the AI (a list of Flashcard objects)
class Deck(BaseModel):
    cards: list[Flashcard]

# Helper function that opens a PDF file and combines the extracted text from every page
def read_pdf(filepath):
    try:
        # Load the PDF document from the given file path
        reader = PdfReader(filepath)
        # Loop through every page, extract its text (defaulting to "" if blank), and join with newlines
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        # Print a clear error message if a PDF is corrupted or unreadable and return empty text
        print(f"Error reading {filepath}: {e}")
        return ""

# Main function that reads all PDFs in slides/ and generates flashcards/deck.json
def main():
    # Create the 'slides' and 'flashcards' folders automatically if they do not exist yet
    os.makedirs(SLIDES_DIR, exist_ok=True)
    os.makedirs(FLASHCARDS_DIR, exist_ok=True)

    # Find all files in the slides/ folder ending with '.pdf' (case-insensitive)
    pdf_files = [f for f in os.listdir(SLIDES_DIR) if f.lower().endswith(".pdf")]
    # Stop early with a helpful message if no PDFs have been added to slides/ yet
    if not pdf_files:
        print(f"No PDF files found in '{SLIDES_DIR}/'. Drop your PDFs there and run this script again!")
        return

    # Initialize an empty list to store all generated flashcards across every PDF
    all_cards = []
    # Loop through each PDF filename found in slides/
    for filename in pdf_files:
        # Remove the '.pdf' extension so the filename serves as the topic/chapter label
        topic_name = os.path.splitext(filename)[0]
        # Build the full file path (e.g., "slides/Chapter1.pdf")
        full_path = os.path.join(SLIDES_DIR, filename)
        # Print progress feedback so the user sees which PDF is being read
        print(f"Reading {filename}...")

        # Extract all text content from the current PDF
        text = read_pdf(full_path)
        # Skip the file if no text could be extracted (for example, image-only scans)
        if not text.strip():
            print(f"Skipping {filename} (no readable text found).")
            continue

        # Print progress feedback before calling the local LLM
        print(f"Generating flashcards for {topic_name}...")
        try:
            # Send the extracted text to local llama3.2 and request structured flashcards
            response = ollama.chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "user",
                        # Prompt the model using the first 12,000 characters to stay within context limits
                        "content": f"Create 5 concise exam-level study flashcards covering the key concepts from this document:\n\n{text[:12000]}",
                    }
                ],
                # Force Ollama to reply strictly in the JSON format defined by the Deck schema
                format=Deck.model_json_schema(),
                # Set temperature to 0 for factual, deterministic JSON output
                options={"temperature": 0},
            )

            # Parse and validate the JSON response string into a Python Deck object
            deck = Deck.model_validate_json(response["message"]["content"])
            # Loop through each validated Flashcard object returned for this PDF
            for card in deck.cards:
                # Append a dictionary formatted for quiz.py starting at spaced-repetition Box 1
                all_cards.append({
                    "chapter": topic_name,
                    "question": card.question,
                    "answer": card.answer,
                    "box": 1,
                })
        except Exception as e:
            # Catch Ollama connection or parsing errors without crashing the entire batch
            print(f"Error generating flashcards for {filename}: {e}")

    # Open (or create) flashcards/deck.json in write mode with UTF-8 encoding
    with open(DECK_FILE, "w", encoding="utf-8") as f:
        # Save the complete list of flashcards as formatted JSON
        json.dump(all_cards, f, indent=2)

    # Print a final summary showing how many cards were created and saved
    print(f"\nDone! Saved {len(all_cards)} flashcards to {DECK_FILE}.")

# Standard Python entry-point check so main() only runs when executed directly
if __name__ == "__main__":
    main()
