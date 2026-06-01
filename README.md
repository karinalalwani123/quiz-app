# QuizMaster Pro — Flask Edition 🎮

A full-stack quiz game built with **Python + Flask**, using Jinja2 templates, sessions, and server-side routing.

## Tech Stack
- **Backend**: Python 3 + Flask
- **Templates**: Jinja2 (HTML)
- **Styling**: CSS3 (custom dark theme)
- **State**: Flask sessions (server-side)
- **Data**: Python dict (questions.py)

## Project Structure
```
quiz_flask/
├── app.py              ← Flask routes & game logic
├── questions.py        ← Question bank (60 questions, 6 categories)
├── requirements.txt    ← Python dependencies
├── templates/
│   ├── base.html       ← Base layout (Jinja2 inheritance)
│   ├── home.html       ← Category selection screen
│   ├── quiz.html       ← Question screen with timer
│   └── result.html     ← Score, review, leaderboard
└── static/
    ├── css/style.css   ← All styles
    └── js/main.js      ← Client-side utilities
```

## How to Run

### 1. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python app.py
```

### 4. Open in browser
```
http://127.0.0.1:5000
```

## Flask Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home / category selection |
| `/start` | POST | Start quiz (picks 10 random questions) |
| `/quiz` | GET | Show current question |
| `/answer` | POST | Submit answer, update session |
| `/result` | GET | Show final score & leaderboard |
| `/reset` | GET | Clear session and restart |

## Key Flask Concepts Used
- `session` — stores quiz state server-side (questions, score, current index)
- `render_template` — Jinja2 templating with template inheritance
- `redirect` + `url_for` — PRG (Post/Redirect/Get) pattern to prevent form resubmission
- `request.form` — handles POST data from answer submissions

## Internship Demo Talking Points
- Demonstrates **MVC-like separation**: routes in app.py, data in questions.py, views in templates/
- Uses **Flask sessions** for stateful game flow without a database
- Implements **PRG pattern** — industry-standard pattern for form handling
- Clean **Jinja2 template inheritance** with base.html
- **Server-side scoring** — score calculated in Python, not manipulatable by client
