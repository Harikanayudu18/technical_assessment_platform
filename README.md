# SkillCheck — Technical Assessment Platform

A portfolio demo with two assessment rounds.

## Features
### Round 1: Knowledge check
- Five MCQs across Python, HTML, JavaScript, CSS and SQL
- Automatic scoring and explanations
- Candidate attempt history stored in SQLite

### Round 2: Coding challenge
- Palindrome checker
- Find the largest number in an array
- JavaScript editor with sample test cases
- Test results show pass/fail for each case
- Candidate code is executed locally in the browser and is not sent to Flask

## Tech stack
Python, Flask, SQLite, HTML, CSS and JavaScript.

## Run locally
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

## Important security note
The coding round uses browser-side JavaScript execution for this local learning demo. Do not execute untrusted candidate code directly on a public server. A production assessment platform should use an isolated sandbox with CPU, memory and time limits.

## Resume description (only after you have run and understood it)
**Technical Assessment Platform | Python, Flask, SQLite, HTML, CSS, JavaScript**
- Built a two-round assessment application with technical MCQs and interactive coding challenges.
- Implemented automatic MCQ scoring, answer explanations and SQLite-based attempt history.
- Created a browser-based JavaScript coding editor that evaluates solutions against sample test cases and displays pass/fail results.
