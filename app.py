from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("assessment.db")

QUESTIONS = [
    {"id": 1, "topic": "Python", "type": "mcq",
     "question": "Which Python data type stores key-value pairs?",
     "options": ["list", "tuple", "dict", "set"], "answer": "dict",
     "explanation": "A dictionary stores data as key-value pairs."},
    {"id": 2, "topic": "HTML", "type": "mcq",
     "question": "Which HTML element is used to create a hyperlink?",
     "options": ["<link>", "<a>", "<href>", "<url>"], "answer": "<a>",
     "explanation": "The anchor element <a> creates hyperlinks."},
    {"id": 3, "topic": "JavaScript", "type": "mcq",
     "question": "Which keyword declares a block-scoped variable that can be reassigned?",
     "options": ["var", "let", "const", "static"], "answer": "let",
     "explanation": "let declares a block-scoped variable that can be reassigned."},
    {"id": 4, "topic": "SQL", "type": "mcq",
     "question": "Which SQL clause filters grouped records?",
     "options": ["WHERE", "ORDER BY", "HAVING", "LIMIT"], "answer": "HAVING",
     "explanation": "HAVING filters groups after GROUP BY."},
    {"id": 5, "topic": "CSS", "type": "mcq",
     "question": "Which CSS layout system is designed for one-dimensional layouts?",
     "options": ["Grid", "Flexbox", "Float", "Position"], "answer": "Flexbox",
     "explanation": "Flexbox is primarily a one-dimensional layout system."}
]

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/")
def home():
    return render_template("index.html", questions=QUESTIONS)

@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "Guest").strip()[:80]
    answers = data.get("answers") or {}
    score = sum(1 for q in QUESTIONS if answers.get(str(q["id"])) == q["answer"])
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO attempts (candidate_name, score, total) VALUES (?, ?, ?)",
            (name, score, len(QUESTIONS))
        )
    review = [{
        "id": q["id"], "question": q["question"],
        "selected": answers.get(str(q["id"]), "Not answered"),
        "correct": q["answer"], "is_correct": answers.get(str(q["id"])) == q["answer"],
        "explanation": q["explanation"]
    } for q in QUESTIONS]
    return jsonify({"score": score, "total": len(QUESTIONS), "review": review})

@app.route("/api/attempts")
def attempts():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT candidate_name, score, total, submitted_at FROM attempts ORDER BY id DESC LIMIT 10"
        ).fetchall()
    return jsonify([dict(row) for row in rows])

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
