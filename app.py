from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from questions import QUESTIONS, CATEGORIES
from datetime import datetime
import random
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///quiz.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.jinja_env.globals.update(enumerate=enumerate)


# ── Model ──
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    score = db.Column(db.Integer)
    correct = db.Column(db.Integer)
    wrong = db.Column(db.Integer)
    played_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()


# ── Routes ──
@app.route("/")
def home():
    return render_template("home.html", categories=CATEGORIES)


@app.route("/start", methods=["POST"])
def start():
    category = request.form.get("category", "science")
    pool = QUESTIONS.get(category, [])
    selected = random.sample(pool, min(10, len(pool)))

    session["questions"] = selected
    session["category"] = category
    session["current"] = 0
    session["score"] = 0
    session["correct"] = 0
    session["wrong"] = 0
    session["answers"] = []

    return redirect(url_for("quiz"))


@app.route("/quiz")
def quiz():
    if "questions" not in session:
        return redirect(url_for("home"))

    current = session["current"]
    questions = session["questions"]

    if current >= len(questions):
        return redirect(url_for("result"))

    question = questions[current]
    total = len(questions)
    progress = int((current / total) * 100)
    cat_info = next((c for c in CATEGORIES if c["id"] == session["category"]), CATEGORIES[0])

    return render_template("quiz.html",
        question=question,
        current=current + 1,
        total=total,
        score=session["score"],
        progress=progress,
        category=cat_info,
        options=list(enumerate(question["options"])),
        labels=["A", "B", "C", "D"]
    )


@app.route("/answer", methods=["POST"])
def answer():
    if "questions" not in session:
        return redirect(url_for("home"))

    selected = request.form.get("answer", type=int)
    time_taken = request.form.get("time_taken", 15, type=int)
    current = session["current"]
    question = session["questions"][current]
    correct_index = question["answer"]

    is_correct = selected == correct_index
    points = 0

    if is_correct:
        time_bonus = round((max(0, 15 - time_taken) / 15) * 50)
        points = 100 + time_bonus
        session["score"] += points
        session["correct"] += 1
    else:
        session["wrong"] += 1

    session["answers"] = session.get("answers", []) + [{
        "question": question["q"],
        "selected": selected,
        "correct": correct_index,
        "options": question["options"],
        "is_correct": is_correct,
        "points": points
    }]

    session["current"] += 1
    session.modified = True

    return redirect(url_for("quiz"))


@app.route("/result")
def result():
    if "questions" not in session:
        return redirect(url_for("home"))

    answers = session.get("answers", [])
    correct = session.get("correct", 0)
    wrong = session.get("wrong", 0)
    score = session.get("score", 0)
    total = len(session.get("questions", []))
    cat_info = next((c for c in CATEGORIES if c["id"] == session.get("category", "")), CATEGORIES[0])

    pct = correct / total if total else 0
    if pct >= 0.9:   emoji, title = "🏆", "Brilliant!"
    elif pct >= 0.7: emoji, title = "🎯", "Well Done!"
    elif pct >= 0.5: emoji, title = "👍", "Not Bad!"
    elif pct >= 0.3: emoji, title = "📚", "Keep Studying!"
    else:            emoji, title = "😅", "Try Again!"

    # Save to DB
    db.session.add(Score(category=cat_info["label"], score=score, correct=correct, wrong=wrong))
    db.session.commit()

    # Fetch top 5 from DB
    leaderboard = Score.query.order_by(Score.score.desc()).limit(5).all()

    return render_template("result.html",
        score=score,
        correct=correct,
        wrong=wrong,
        total=total,
        emoji=emoji,
        title=title,
        category=cat_info,
        answers=answers,
        leaderboard=[{"score": e.score, "category": e.category, "correct": e.correct} for e in leaderboard],
        pct=round(pct * 100)
    )


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG", "False").lower() == "true")