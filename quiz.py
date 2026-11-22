# Import built-in module for working with file paths and checking if files exist
import os
# Import built-in module for reading and writing JSON flashcard data
import json
# Import built-in module for weighted random card selection
import random
# Import the local Ollama Python client to communicate with the local LLM server
import ollama

# Define the path to the generated flashcard deck inside the flashcards/ folder
DECK_FILE = os.path.join("flashcards", "deck.json")

# Helper function to safely load the list of flashcard dictionaries from disk
def load_deck():
    # Verify that flashcards/deck.json exists before trying to open it
    if not os.path.exists(DECK_FILE):
        print(f"Error: '{DECK_FILE}' not found. Run 'python generate_cards.py' first to build your deck!")
        return []
    try:
        # Open flashcards/deck.json in read mode with UTF-8 encoding
        with open(DECK_FILE, "r", encoding="utf-8") as f:
            # Parse the JSON file contents back into a Python list of dictionaries
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        # Handle corrupted JSON or file permission errors gracefully without crashing
        print(f"Error reading '{DECK_FILE}': {e}")
        return []

# Helper function to persist updated flashcard box levels back to disk
def save_deck(deck):
    # Ensure the flashcards/ folder exists before writing
    os.makedirs(os.path.dirname(DECK_FILE), exist_ok=True)
    # Open flashcards/deck.json in write mode with UTF-8 encoding
    with open(DECK_FILE, "w", encoding="utf-8") as f:
        # Serialize the Python list to formatted JSON (2-space indentation)
        json.dump(deck, f, indent=2)

# Select the next flashcard using weighted random sampling (Leitner-style spaced repetition)
def pick_card(deck):
    # Assign higher weight to lower box numbers (Box 1 = weight 3, Box 2 = weight 2, Box 3 = weight 1)
    weights = [max(1, 4 - card.get("box", 1)) for card in deck]
    # Pick and return one card dictionary based on the calculated probability weights
    return random.choices(deck, weights=weights, k=1)[0]

# Return the grading persona prompt and few-shot examples based on the user's chosen difficulty level
def get_persona_prompt(level):
    # Match the user's menu selection against levels 1 through 4
    match level:
        case "1":
            return (
                "Persona: Warm, encouraging teacher speaking directly to the user ('you'). "
                "Be generous if they get the core concept right (CORRECT:), and gentle if they miss it (INCORRECT:).\n"
                "Example CORRECT: CORRECT: Awesome job! You nailed the main idea.\n"
                "Example INCORRECT: INCORRECT: Good guess, you're on the right track, but the key detail here is a bit different!"
            )
        case "2":
            return (
                "Persona: Strict, demanding professor speaking directly to 'you'. "
                "Mark incomplete answers INCORRECT: if key terms or details are missing.\n"
                "Example CORRECT: CORRECT: Exact and thorough—you covered every required detail.\n"
                "Example INCORRECT: INCORRECT: You are missing several key details required for a complete answer."
            )
        case "3":
            return (
                "Persona: Nervous, unsure classmate studying with 'you'. Grade accurately, but sound hesitant.\n"
                "Example CORRECT: CORRECT: Uh, yeah, sounds about right to me! Pretty sure that's what the notes said.\n"
                "Example INCORRECT: INCORRECT: Hmm, I don't think that's quite it... didn't the material say something else?"
            )
        case "4":
            return (
                "Persona: Totally clueless classmate who didn't study at all.\n"
                "Example CORRECT: CORRECT: I have no idea, but sounds legit to me though!\n"
                "Example INCORRECT: INCORRECT: Honestly I have zero clue, Ha! you might be right or wrong!"
            )
        # Fallback persona if the user enters anything outside 1-4
        case _:
            return "Persona: Fair study partner speaking directly to 'you'."

# Grade the user's typed response using local Ollama and stream feedback token-by-token
def stream_grade(question, correct_answer, user_answer, persona_instruction, level):
    # Define common non-answer phrases to catch immediately without calling the LLM
    idk_phrases = ("idk", "don't know", "dont know", "no idea", "skip")
    # Short-circuit blank or "I don't know" inputs (unless Clueless Classmate mode is active)
    if level != "4" and (len(user_answer) < 4 or any(p in user_answer.lower() for p in idk_phrases)):
        msg = "INCORRECT: No answer provided."
        print(f"\n{msg}")
        return msg

    # Build a randomized guessing prompt if Clueless Classmate mode (level 4) is active
    if level == "4":
        prompt = f"""{persona_instruction}
Question: {question}
User Answer: {user_answer}

Start with either CORRECT: or INCORRECT: at random, followed by 1 short sentence in character talking to 'you'."""
    # Otherwise build a fact-checking prompt comparing the user's answer against the reference answer
    else:
        prompt = f"""{persona_instruction}

Question: {question}
Reference Answer: {correct_answer}
User Answer: {user_answer}

Rules:
- Fact-check the User Answer against the Reference Answer (jokes, nonsense, or wrong facts MUST start with INCORRECT:).
- Start your reply with ONLY 'CORRECT:' or 'INCORRECT:' followed by 1-2 sentences in your exact Persona voice, speaking directly to 'you'."""

    # Use high temperature (0.9) for unpredictable guesses in level 4, or 0.4 for consistent grading with natural tone
    temp = 0.9 if level == "4" else 0.4

    try:
        # Send the grading prompt to the local llama3.2 model with streaming enabled
        stream = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": temp},
            stream=True,
        )

        # Print a blank line before streaming the AI's reply
        print()
        # Accumulate the complete response string so we can check whether it starts with CORRECT or INCORRECT
        full_reply = ""
        # Iterate over each streamed response chunk as Ollama generates tokens
        for chunk in stream:
            # Extract the text token from the current chunk
            token = chunk["message"]["content"]
            # Print the token immediately without a newline and flush stdout so it appears live
            print(token, end="", flush=True)
            # Append the token to the full reply string
            full_reply += token
        # Print a final newline once the stream finishes
        print()
        # Return the cleaned, complete feedback text
        return full_reply.strip()
    except Exception as e:
        # Handle Ollama connection errors cleanly without crashing the quiz session
        msg = f"INCORRECT: Could not reach local Ollama server ({e})."
        print(f"\n{msg}")
        return msg

# Main interactive quiz loop
def main():
    # Load all flashcards from flashcards/deck.json into memory
    deck = load_deck()
    # Exit early if the deck failed to load or is empty
    if not deck:
        return

    # Display how many cards were loaded and show the persona selection menu
    print(f"Loaded {len(deck)} flashcards.\n")
    print("Choose your grader persona:")
    print("  1 - Supportive Teacher")
    print("  2 - Strict Professor")
    print("  3 - Unsure Classmate")
    print("  4 - Clueless Classmate")

    # Read the user's persona choice, defaulting to "1" if they press Enter
    level = input("\nSelect level (1-4) [default 1]: ").strip() or "1"
    # Retrieve the matching persona prompt instructions
    persona_instruction = get_persona_prompt(level)
    print("\nType 'quit' anytime to exit.\n")

    # Loop continuously until the user types 'quit' or 'exit'
    while True:
        # Pick a weighted-random flashcard from the deck
        card = pick_card(deck)
        # Display the card's topic/chapter, current spaced-repetition box, and question
        print(f"[{card['chapter']} | Box {card['box']}] {card['question']}")
        # Prompt the user to type their answer
        user_answer = input("Your answer: ").strip()

        # Check if the user wants to end the study session
        if user_answer.lower() in ("quit", "exit"):
            print("Progress saved. Good luck studying!")
            break

        # Stream the AI's grading feedback to the terminal and capture the full text
        feedback = stream_grade(card["question"], card["answer"], user_answer, persona_instruction, level)
        # Display the reference answer underneath so the user can compare
        print(f"Reference: {card['answer']}\n")

        # Promote the card up one box (up to Box 3) if graded CORRECT
        if feedback.upper().startswith("CORRECT"):
            card["box"] = min(3, card["box"] + 1)
        # Otherwise reset the card back to Box 1 so it appears more frequently
        else:
            card["box"] = 1

        # Save the updated box progress back to flashcards/deck.json after every question
        save_deck(deck)

# Standard Python entry-point check so main() only runs when executed directly
if __name__ == "__main__":
    main()

