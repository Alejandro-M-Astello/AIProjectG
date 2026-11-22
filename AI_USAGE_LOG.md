# AI Usage Log

**Project:** Local AI Study & Flashcard Assistant (`AIProjectG`)  
**AI Tool Used:** Google Gemini  

---

## Entry 1: Project Ideation & Scope Definition
1. **Prompt submitted to the AI tool:**  
   *[Attached screenshot of the AI Assistant assignment PDF]*  
   "So I'm doing this project for one of my classes. Any suggestions for an idea?"
2. **AI-generated response:**  
   > "Since you want to build a practical AI application without dealing with paid API keys or uploading copyrighted lecture slides to cloud servers, a great option is a Local AI Study & Flashcard Assistant built in Python using Ollama (`llama3.2`), `pypdf` for PDF ingestion, `pydantic` schemas for clean JSON flashcards, and a second CLI script that quizzes you on the saved cards."
3. **Student modifications or refinements:**  
   Well, I reviewed the suggested ideas against my class requirements and decided on a simple offline CLI application tailored to the pdf instructions.
4. **Final implementation result:**  
   Established the core concept and privacy-first local design for the project.

---

## Entry 2: Local LLM Environment Setup (Ollama)
1. **Prompt submitted to the AI tool:**  
   "Ok, since I don't want to use any external API keys let's stick to ollama so that everything is ran locally. So, what even is ollama and how do I download it."
2. **AI-generated response:**  
   > "Ollama is a free, open-source runtime engine that lets you download and run Large Language Models (like Meta's `llama3.2`) directly on your own computer instead of sending data to cloud servers. Download `OllamaSetup.exe` from ollama.com/download/windows, install it, and run `ollama pull llama3.2` followed by `ollama run llama3.2` in your terminal."
3. **Student modifications or refinements:**  
   I downloaded the Windows installer, pulled the `llama3.2` (3B) model locally via PowerShell, and verified it responded offline using `/bye` to exit.
4. **Final implementation result:**  
   Confirmed `llama3.2` runs locally on `http://localhost:11434` without external API keys or internet access.

---

## Entry 3: Selecting the Study Tool & Installing Dependencies
1. **Prompt submitted to the AI tool:**  
   "Ok, I went ahead and installed ollama and verified that it worked already. I'd say for the project let's just do something simple like the flashcard study guide thing since it seems like it would be useful since I'm still a student."
2. **AI-generated response:**  
   > "Separating the project into two clean Python scripts (`generate_cards.py` and `quiz.py`) will keep it easy to test and debug. Open your terminal in VS Code and install the three libraries needed: `pip install ollama pypdf pydantic`."
3. **Student modifications or refinements:**  
   Installed `ollama`, `pypdf`, and `pydantic` in my Python environment and verified each package imported cleanly.
4. **Final implementation result:**  
   All required Python dependencies were installed and ready for development.

---

## Entry 4: System Architecture & Folder Design
1. **Prompt submitted to the AI tool:**  
   "Ok, so our design is: Create an empty slides file where a user puts their slides (but in PDF format), create a flashcard generator file that incorporates ollama to read the slides file and stores it in a JSON folder/file, and create a quiz file that then reads the JSON folder/file for the flashcards and quizzes the user."
2. **AI-generated response:**  
   > "Decoupling card generation from quizzing means you only have to parse PDFs and run generation once per chapter, while `quiz.py` can load `deck.json` instantaneously. Organize the workspace into `slides/`, `flashcards/deck.json`, `generate_cards.py`, and `quiz.py`."
3. **Student modifications or refinements:**  
   Created the `slides/` and `flashcards/` directories in VS Code and added a sample lecture PDF (`CNI6e Ch 18.pdf`) to `slides/` for testing.
4. **Final implementation result:**  
   Finalized the modular two-script pipeline and directory layout.

---

## Entry 5: Incremental Component Testing
1. **Prompt submitted to the AI tool:**  
   "Sure, let's run a few tests."
2. **AI-generated response:**  
   > "Breaking the build down into small, isolated test scripts (`test.py` through `test4.py`) before combining everything verifies each piece works on your machine: testing the Ollama chat connection, `pypdf` text extraction, `pydantic` structured JSON enforcement, and saving output to `flashcards/deck.json`."
3. **Student modifications or refinements:**  
   Ran each isolated test script individually against my lecture PDF to verify character extraction counts and valid Pydantic schema parsing before deleting the temporary test files.
4. **Final implementation result:**  
   Verified end-to-end data flow from PDF text extraction to structured JSON disk storage.

---

## Entry 6: Building `generate_cards.py` and `quiz.py`
1. **Prompt submitted to the AI tool:**  
   "Ok, let's take all of this and actually create our two py files, being quiz.py and generate_cards.py."
2. **AI-generated response:**  
   > "Combine the validated components into `generate_cards.py` (scanning `slides/*.pdf`, truncating text to 12,000 characters, and initializing each card with `box: 1`) and `quiz.py` (loading `flashcards/deck.json`, grading answers via `ollama.chat()`, and updating `box` progress)."
3. **Student modifications or refinements:**  
   I Integrated the scripts into my project folder, adjusted the card count and prompt phrasing for my Computer Networks slides, and ran `generate_cards.py` to build my initial `deck.json`.
4. **Final implementation result:**  
   Both core scripts ran end-to-end, generating flashcards from lecture PDFs and grading answers in the terminal.

---

## Entry 7: Adding Token Streaming & Grader Personas
1. **Prompt submitted to the AI tool:**  
   "This code is fine, but I feel like we could improve it. The results are displayed all at once and takes a while to load. We should just stream it word per word and display it as the AI writes the response word per word to not have the user sit around and wait for a whole chunk of text. The AI could also have different personalities that a user could pick between, so something like, supportive teacher, strict professor, unsure classmate, or even a clueless classmate."
2. **AI-generated response:**  
   > "Define a `PERSONAS` dictionary with custom system prompts and temperature settings (`0.3` to `0.9`), and pass `stream=True` to `ollama.chat()` so tokens print immediately with `end=\"\", flush=True` while accumulating `full_response` to check `CORRECT:` vs. `INCORRECT:`."
3. **Student modifications or refinements:**  
   I added the startup persona selection menu with all 4 selcted personas as a prompt for user selction(`1–4`) to `quiz.py` and tuned the system prompts so the classmate personas remained humorous while still grading accurately.
4. **Final implementation result:**  
   `quiz.py` streams responses in real time with four distinct, selectable AI grader personalities.

---

## Entry 8: Debugging Python Indentation & Runtime Errors
1. **Prompt submitted to the AI tool:**  
   *[Showed a screenshot of VS Code terminal displaying an `IndentationError` in `quiz.py`]*  
   "Aww come on, where is this error even coming from?"
2. **AI-generated response:**  
   > "Looks like you've got an `IndentationError` right inside your `while True:` quiz loop in `quiz.py`. Highlight `full_response = \"\"` and `for chunk in stream:` and press `Shift + Tab` once so they line up cleanly at 8 spaces, with the loop body indented at 12 spaces."
3. **Student modifications or refinements:**  
   Adjusted the block indentation in `quiz.py` and re-ran the script to verify the loop executed cleanly. *(Also just a side note, but this entry represents multiple debugging interactions throughout development where terminal tracebacks and code screenshots were shared with Gemini to diagnose and resolve syntax, indentation, and runtime issues.)*
4. **Final implementation result:**  
   Cleared the `IndentationError` and restored clean execution of the streaming quiz loop.

---

## Entry 9: Fixing False Positives on `"idk"` & Uncertain Answers
1. **Prompt submitted to the AI tool:**  
   "Ok, it seems like the program has some oddities. When I type something like idk or express uncertainty the AI still displays it as correct and acts like I got it correct."
2. **AI-generated response:**  
   > "Small 3B models like `llama3.2` tend to be overly polite and start encouraging responses with `CORRECT:`. Catch uncertainty phrases (`idk`, `i don't know`, empty input) in a `SKIP_PHRASES` set before calling `ollama.chat()`, immediately reveal the reference answer, reset `card['box'] = 1`, and add a strict rule to `grading_prompt`."
3. **Student modifications or refinements:**  
   Implemented the `SKIP_PHRASES` short-circuit check in `quiz.py` and tightened the grading prompt instructions so hesitant guesses are graded strictly.
4. **Final implementation result:**  
   Typing `"idk"` or leaving an answer blank immediately reveals the correct answer and resets the card to Box 1 without false positives.

---

## Entry 10: Structuring Final Project Documentation
1. **Prompt submitted to the AI tool:**  
   "Well, after testing and debugging it seems like it's working as intended. Now we just gotta do all this documentation stuff and things."
2. **AI-generated response:**  
   > "Package the repository with four documentation deliverables: `README.md` (overview, setup, and terminal screenshots), `PLANNING.md` (objectives, requirements, architecture, and tech stack), `requirements.txt` (`ollama`, `pypdf`, `pydantic`), and `AI_USAGE_LOG.md` documenting at least 10 prompts with refinements and outcomes."
3. **Student modifications or refinements:**  
   Reviewed the course rubric checklist to ensure all required sections were present, created each Markdown and dependency file in the repository root, and verified formatting in VS Code Markdown Preview.
4. **Final implementation result:**  
   Completed all required project documentation and verified the repository is ready for submission.
