import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path(__file__).with_name("research_history.db")
URL_PATTERN = re.compile(r"https?://[^\s\]\)\}\"'<>]+")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS research_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                final_report TEXT NOT NULL,
                critic_feedback TEXT NOT NULL,
                sources TEXT NOT NULL
            )
            """
        )


def extract_sources(*texts):
    sources = []
    seen = set()

    for text in texts:
        if not text:
            continue

        for match in URL_PATTERN.findall(text):
            source = match.rstrip(".,;:")
            if source not in seen:
                seen.add(source)
                sources.append(source)

    return sources


def save_research(topic, final_report, critic_feedback, sources):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO research_history (
                topic,
                timestamp,
                final_report,
                critic_feedback,
                sources
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                topic,
                timestamp,
                final_report,
                critic_feedback,
                json.dumps(sources),
            ),
        )
        return cursor.lastrowid


def list_reports():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, topic, timestamp
            FROM research_history
            ORDER BY datetime(timestamp) DESC, id DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]


def get_report(report_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, topic, timestamp, final_report, critic_feedback, sources
            FROM research_history
            WHERE id = ?
            """,
            (report_id,),
        ).fetchone()

    if row is None:
        return None

    report = dict(row)
    report["sources"] = json.loads(report["sources"] or "[]")
    return report


def delete_report(report_id):
    with get_connection() as connection:
        connection.execute("DELETE FROM research_history WHERE id = ?", (report_id,))


def delete_all_reports():
    with get_connection() as connection:
        connection.execute("DELETE FROM research_history")
