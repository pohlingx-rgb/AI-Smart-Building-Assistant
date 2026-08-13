import json
import os
from datetime import datetime

HISTORY_FILE = "data/question_history.json"

def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

def append_history(module, question, answer, session_state):
    """Append a new Q&A entry to history and persist to disk."""
    if "question_history" not in session_state:
        session_state.question_history = []

    entry = {
        "module": module,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "answer": answer
    }
    session_state.question_history.append(entry)
    save_history(session_state.question_history)
