import sqlite3
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash

from helpers import analyze_code

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "codetutor.db"

app = Flask(__name__)
# Use of AI - line --> 15
app.secret_key = "dev-secret-change-me"


def get_conn() -> sqlite3.Connection:
    """Open SQLite connection with row factory"""
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    """Create tables if they don't exist"""
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                language TEXT NOT NULL,
                code TEXT NOT NULL
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_id INTEGER NOT NULL,
                error_type TEXT NOT NULL,
                message TEXT NOT NULL,
                explanation TEXT NOT NULL,
                suggestion TEXT NOT NULL,
                line INTEGER,
                severity TEXT NOT NULL,
                FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE
            );
        """)


@app.before_request
def _ensure_db():
    init_db()


@app.route("/", methods=["GET"])
def index():
    sample_code = """import os

def greet(name)
    print("Hello", name)

x = 10
"""
    return render_template("index.html", code=sample_code)


@app.route("/analyze", methods=["POST"])
def analyze():
    code = request.form.get("code", "")
    language = "python"

    if not code.strip():
        flash("Paste some code first — empty input cant be analyzed.", "warning")
        return redirect(url_for("index"))

    issues = analyze_code(code)
    created_at = datetime.now().isoformat(timespec="seconds")

    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO analyses (created_at, language, code) VALUES (?, ?, ?)",
            (created_at, language, code),
        )
        # Use of AI - line --> 91
        analysis_id = cur.lastrowid

        for it in issues:
            conn.execute("""
                INSERT INTO issues (
                    analysis_id, error_type, message, explanation, suggestion, line, severity
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                analysis_id,
                it.error_type,
                it.message,
                it.explanation,
                it.suggestion,
                it.line,
                it.severity,
            ))

    return redirect(url_for("report", analysis_id=analysis_id))


# Use of AI - line --> 113
@app.route("/report/<int:analysis_id>", methods=["GET"])
def report(analysis_id: int):
    with get_conn() as conn:
        analysis = conn.execute(
            "SELECT * FROM analyses WHERE id = ?",
            (analysis_id,)
        ).fetchone()

        if analysis is None:
            flash("That report doesn't exist.", "warning")
            return redirect(url_for("index"))

        issues = conn.execute("""
            SELECT * FROM issues
            WHERE analysis_id = ?
            ORDER BY
              CASE severity
                WHEN 'error' THEN 0
                WHEN 'warning' THEN 1
                ELSE 2
              END,
              COALESCE(line, 999999) ASC
        """, (analysis_id,)).fetchall()

    return render_template("report.html", analysis=analysis, issues=issues)


@app.route("/history", methods=["GET"])
def history():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT id, created_at, language, length(code) AS size
            FROM analyses
            ORDER BY id DESC
            LIMIT 50
        """).fetchall()
        # Use of AI - line --> 147

    return render_template("history.html", rows=rows)


# Use of AI - line --> 153
@app.route("/delete/<int:analysis_id>", methods=["POST"])
def delete(analysis_id: int):
    """Optional: delete a saved analysis from history."""
    with get_conn() as conn:
        conn.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
    flash(f"Deleted report #{analysis_id}.", "info")
    return redirect(url_for("history"))

