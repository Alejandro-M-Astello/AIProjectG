# System Requirements & Design Specification

## 1. Project Overview
**AI Student Study Assistant** is a fully offline, command-line study tool powered by a local Model called (`llama3.2` via Ollama). It automates flashcard creation from academic PDF lecture slides and conducts interactive, persona-driven spaced-repetition quiz sessions without sending student materials to external cloud APIs or without the interent.

---

## 2. Functional Requirements
* **FR-1 — Automated PDF Ingestion:** The system shall scan the `slides/` directory for `.pdf` files and extract raw text across all pages using `pypdf`.
* **FR-2 — Structured Flashcard Generation:** Using `ollama` and `pydantic` schema validation, the system shall synthesize concise, exam-level question-and-answer flashcards from extracted lecture text and save them to `flashcards/deck.json`.
* **FR-3 — Leitner Spaced-Repetition Scheduling:** Each flashcard shall track a mastery `box` level (`1` through `3`). Weighted random sampling shall prioritize lower-box cards (`Box 1` weight = 3, `Box 2` weight = 2, `Box 3` weight = 1).
* **FR-4 — Multi-Persona AI Grading:** Users shall select from four distinct grader personas (`1 - Supportive Teacher`, `2 - Strict Professor`, `3 - Unsure Classmate`, `4 - Clueless Classmate`) that evaluate free-text user answers against reference answers using a `CORRECT:` / `INCORRECT:` prefix.
* **FR-5 — Live Token Streaming & Persistence:** Grading feedback shall stream token-by-token to the terminal in real time, and updated box promotions/resets shall persist to `flashcards/deck.json` after every question.

---

## 3. Non-Functional Requirements
* **NFR-1 — Privacy & Offline Execution:** All PDF parsing, LLM inference, and flashcard storage must run 100% locally on the user's machine.
* **NFR-2 — Fault Tolerance:** Missing folders (`slides/`, `flashcards/`), missing decks, blank user inputs, corrupted PDFs, and Ollama server connection issues must be handled gracefully with clear terminal messages rather than unhandled exceptions.
* **NFR-3 — Maintainability & Modularity:** Data generation (`generate_cards.py`) and interactive quizzing (`quiz.py`) are decoupled via a human-readable JSON schema (`flashcards/deck.json`).

---

## 4. System Architecture & Data Schema
```text
AIProjectG/
├── slides/                 # Input folder for lecture PDFs
├── flashcards/             # Output folder for generated JSON decks
│   └── deck.json           # Persistent flashcard state & Leitner box tracking
├── generate_cards.py       # PDF extraction + Pydantic-validated LLM card generator
├── quiz.py                 # Interactive CLI quizzer + streaming persona grader
└── requirements.txt        # Python package dependencies
```

### Flashcard JSON Schema (`flashcards/deck.json`)
```json
[
  {
    "chapter": "CNI6e Ch 20",
    "question": "What is the motivation for internetworking?",
    "answer": "Each network technology is designed to fit a specific set of constraints...",
    "box": 1
  }
]
```

---

## 5. Hardware & Software Environment
* **Operating System:** Windows 11 (compatible with macOS and Linux)
* **Python Version:** Python 3.11+
* **Local Inference Runtime:** Ollama with `llama3.2` pulled locally
* **Python Dependencies:** `ollama`, `pypdf`, `pydantic`