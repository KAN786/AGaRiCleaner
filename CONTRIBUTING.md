# Contributing to AGaRiCleaner

Thank you for your interest in contributing to AGaRiCleaner — a FastAPI-based system for processing and evaluating text using AI and Firebase!

---

## Ways to Contribute

- Improve core logic (API endpoints, scoring, filtering)
- Frontend integration (React, Gradio, etc.)
- Report and fix bugs
- Write or improve test cases
- Improve documentation or translations
- Help with CI/CD, Docker, or deployment to Render

---

## Local Setup

1. **Clone the repo**

```bash
git clone https://github.com/ROOM1ghouls/AGaRiCleaner.git
cd agaricleaner
```

2. Set up virtual environment
```
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. set up environment variables
```
FIREBASE_ADMIN_KEY=your_minified_json_key
OPENAI_API_KEY=your_openai_key
ASSISTANT_ID=your_assistant_id
AGARICLEANER_URL=https://gradio.app/...
```
5. Run the app
```
uvicorn app.main:app --reload
```


# Guidelines
- Use snake_case for variables/functions in Python.
- Follow PEP8 standards and format code with black.
- Write clear, descriptive commit messages (e.g., fix: handle timeout errors from Gradio).
- Avoid hardcoding API keys or secrets.


