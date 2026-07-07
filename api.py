import json
import queue
import threading

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from history_db import (
    delete_all_reports,
    delete_report,
    extract_sources,
    get_report,
    init_db,
    list_reports,
    save_research,
)
from pipeline import run_research_pipeline


init_db()

app = FastAPI(title="ResearchIQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    topic: str


def stream_event(payload):
    return f"{json.dumps(payload)}\n"


@app.post("/api/research")
def research(request: ResearchRequest):
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Please enter a research topic.")

    events = queue.Queue()

    def progress_callback(stage, status, progress, message=None):
        events.put(
            {
                "type": "progress",
                "stage": stage,
                "status": status,
                "progress": progress,
                "message": message,
            }
        )

    def worker():
        try:
            state = run_research_pipeline(topic, progress_callback=progress_callback)
            sources = extract_sources(
                state.get("search_results", ""),
                state.get("scraped_content", ""),
                state.get("report", ""),
            )
            report_id = save_research(
                topic,
                state.get("report", ""),
                state.get("feedback", ""),
                sources,
                search_results=state.get("search_results", ""),
                scraped_content=state.get("scraped_content", ""),
            )
            events.put(
                {
                    "type": "complete",
                    "reportId": report_id,
                    "topic": topic,
                    "state": state,
                    "sources": sources,
                }
            )
        except Exception as exc:
            events.put({"type": "error", "message": str(exc)})
        finally:
            events.put(None)

    threading.Thread(target=worker, daemon=True).start()

    def event_generator():
        while True:
            event = events.get()
            if event is None:
                break
            yield stream_event(event)

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")


@app.get("/api/history")
def history():
    return list_reports()


@app.get("/api/history/{report_id}")
def history_item(report_id: int):
    report = get_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found.")
    return report


@app.delete("/api/history/{report_id}")
def delete_history_item(report_id: int):
    delete_report(report_id)
    return {"ok": True}


@app.delete("/api/history")
def clear_history():
    delete_all_reports()
    return {"ok": True}
