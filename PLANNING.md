# Project Planning Documentation & Development Roadmap

## 1. Problem Statement
Manually reviewing A lot of University lecture slide decks, where some of them reach well over 80 slides per chapter, sure is time-consuming. It becomes an even bigger problem when all your teachers decided to assign so much to read and you're left wondering where to even start since passive re-reading yields poor retention. Existing AI study tools require paid subscriptions and uploading copyrighted course materials to cloud servers. Your professors might not be cool with uploading their slides for AI to read over and analze. 
 
## 2. Project Objectives
* **Automate Study Guides:** Prevent and completely eliminate the need to maually create flashcards, because this would involve reading EVERYTHING.
* **Imporove Content retention** By answering questions as if someone is testing you  it helps the information stich better
* **Better Privacy and Accessibility** By having everything run offline and locally on a user's machine allows accessibility even without internet connection
* **Engaging Feedback** The AI model and chosen persona will respond to you in various ways depending which setting you choose and how you feel like being treated that day. 

## 3. Functional Requirements
* **FR-1 - AutomatedPDF Ingestion:** The system will scan any PDF files placed into the `slides/` directory and extract raw text across the pages using `pypdf`.
* **FR-2 - Structured Flashcard Generator** Using `ollama` and `pydantic` the system will generate Q&A flashcards and save them to `flashcards/deck.json`
* **FR-3 - Leitner Spaced-Repetition** each flashcard tracks mastery in a `box` (those being levels `1` to level `3`) using weighted random sampling to prioritize weaker known topics
* **Multi-Persona AI Grading:** users can select from four distinct grader personas, those being: `Supportive Teacher`,`Strict professor`,`Unsure Classmate`, and `Clueless Classmate` that evaluate a users answers with a referenced answer using a `correct`/`incorrect` prefix
* **FR-5 Live Streaming and State Persistence:** Feedback will be streamed token-by-token to the terminal in real-time, and the updated box promotions/resets will be saved automatically to `flashcards/deck.json` after every question.

## 4. System Features
* **Offline PDF-to-JSON Pipeline `(generate_cards.py)`:** Converts PDF files into flashcards
* **3-Box Leitner mastery System `(quiz.py)`:** Automatically promote correct answers up to level 3 and reset incorrect answers to level 1.
* **4 Selectable AI Personas** Tailors grading tone and strictness through a temperature value 
* **Deterministic Input Guardrails:** deals with blank inputs or uncertainty such as `"idk"`or `"skip"` in python before even calling the LLM to prevent false partial credit or unnecessary computation
* **Error Handling:** Catches missing folders, empty decks, and unreadable PDF files without crashing. 

## 5. Software Design
Build a lightweight, modular two-stage CLI pipeline in Python backed by a local `llama3.2` model via Ollama:
1. **Stage 1 (`generate_cards.py`):** Batch-processes PDF slides into structured JSON flashcards validated with Pydantic models.
2. **Stage 2 (`quiz.py`):** Implements a 3-box Leitner spaced-repetition loop with selectable AI grader personas and real-time token streaming to quiz you on provided slides.


---

## 6. Technology Stack
* **Programming Language:** Python 3.11
* **Local LLM Runtime & Model:** Ollama locally running `llama3.2`
* **PDF Parsing Library:** `pypdf`
* **Data Validation and Structured Outputs:** `pydantic`
* **Storage Format:** Local JSON (`flashcards/deck.json`)
* **Development Environment:** Visual Studio Code on Windows 11 

## 7. Milestone Breakdown & Timeline

| Phase | Target Date | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **Phase 1: Environment & Feasibility** | Nov 16–17, 2026 | Install Ollama (`llama3.2`), verify local Python SDK (`test.py`–`test4.py`), and benchmark structured JSON output vs. streaming chat. | Completed |
| **Phase 2: Core Pipeline Implementation** | Nov 17–18, 2026 | Implement `generate_cards.py` (`pypdf` + `pydantic` structured outputs) and `quiz.py` (Leitner box weights + 4 grader personas). | Completed |
| **Phase 3: Verification & Edge-Case Testing** | Nov 18, 2026 | Validate end-to-end execution using Computer Networks lecture PDFs as a sample (`CNI6e Ch 18`, `CNI6e Ch 20`), verify box promotion/demotion, and capture terminal screenshots. | Completed |
| **Phase 4: Documentation & Repository Cleanup** | Nov 18–19, 2026 | Author `requirements.md`, `PLANNING.md`, `AI_USAGE_LOG.md`, `README.md`, and `requirements.txt`; archive prototype scripts and clear out `slides/` for uploading to GitHub. | Completed |

---

## 8. Key Technical Decisions & Trade-offs
* **Decoupled Two-Script Architecture:** Separating card generation from quizzing ensures students only experience the LLM generation latency once per PDF chapter, allowing instant startup during repeated study sessions.
* **Pydantic Structured Outputs:** Enforcing `Deck(BaseModel)` guarantees valid JSON fields (`chapter`, `question`, `answer`, `box`) without fragile regex parsing of raw LLM text.
* **Context Window Truncation (`text[:12000]`):** Capping initial ingestion at 12,000 characters keeps generation fast (~10–15 seconds per PDF) on consumer laptop hardware while capturing core definitions.
* **Short-Circuit Input Validation:** Intercepting unsure answers like `"idk"`, `"skip"`, or ultra-short inputs in Python before invoking `ollama.chat()` saves compute and prevents hallucinated partial credit where the AI might mistakenly display your answer as correct even though it actually might not be. 