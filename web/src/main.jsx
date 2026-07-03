import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Brain,
  ChevronLeft,
  ChevronRight,
  FileText,
  History,
  Loader2,
  PenLine,
  Search,
  Trash2,
  XCircle,
} from "lucide-react";
import "./styles.css";

const API_BASE = "http://127.0.0.1:8000";

const STAGES = [
  { key: "searching", label: "Searching...", icon: Search },
  { key: "reading", label: "Reading Sources...", icon: FileText },
  { key: "writing", label: "Writing Report...", icon: PenLine },
  { key: "critiquing", label: "Critiquing Report...", icon: Brain },
  { key: "completed", label: "Completed", icon: Brain },
];

const initialStageStatuses = Object.fromEntries(STAGES.map((stage) => [stage.key, "pending"]));

function App() {
  const [topic, setTopic] = useState("");
  const [historyOpen, setHistoryOpen] = useState(true);
  const [historyItems, setHistoryItems] = useState([]);
  const [selectedReportId, setSelectedReportId] = useState(null);
  const [loadedReport, setLoadedReport] = useState(null);
  const [result, setResult] = useState(null);
  const [sources, setSources] = useState([]);
  const [progress, setProgress] = useState(0);
  const [stageStatuses, setStageStatuses] = useState(initialStageStatuses);
  const [progressMessage, setProgressMessage] = useState("");
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    const response = await fetch(`${API_BASE}/api/history`);
    setHistoryItems(await response.json());
  }

  async function loadReport(reportId) {
    setError("");
    setResult(null);
    setSelectedReportId(reportId);
    const response = await fetch(`${API_BASE}/api/history/${reportId}`);
    if (!response.ok) {
      setError("That saved report could not be loaded.");
      await loadHistory();
      return;
    }
    setLoadedReport(await response.json());
  }

  async function deleteSelectedReport() {
    if (!selectedReportId) return;
    await fetch(`${API_BASE}/api/history/${selectedReportId}`, { method: "DELETE" });
    setSelectedReportId(null);
    setLoadedReport(null);
    await loadHistory();
  }

  async function deleteAllHistory() {
    await fetch(`${API_BASE}/api/history`, { method: "DELETE" });
    setSelectedReportId(null);
    setLoadedReport(null);
    await loadHistory();
  }

  async function runResearch(event) {
    event.preventDefault();
    const trimmedTopic = topic.trim();
    if (!trimmedTopic || running) return;

    setRunning(true);
    setError("");
    setResult(null);
    setLoadedReport(null);
    setSelectedReportId(null);
    setSources([]);
    setProgress(0);
    setStageStatuses(initialStageStatuses);
    setProgressMessage("Preparing the research agents...");

    try {
      const response = await fetch(`${API_BASE}/api/research`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic }),
      });

      if (!response.ok || !response.body) {
        throw new Error("Research could not be started.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.trim()) continue;
          handleStreamEvent(JSON.parse(line));
        }
      }

      await loadHistory();
    } catch (caughtError) {
      setError(caughtError.message || "Research stopped unexpectedly.");
    } finally {
      setRunning(false);
    }
  }

  function handleStreamEvent(event) {
    if (event.type === "progress") {
      setProgress(event.progress || 0);
      setProgressMessage(event.message || "Pipeline is running...");
      setStageStatuses((current) => {
        const next = { ...current };
        if (event.stage === "completed") {
          STAGES.forEach((stage) => {
            next[stage.key] = "success";
          });
        } else {
          next[event.stage] = event.status;
        }
        return next;
      });
      return;
    }

    if (event.type === "complete") {
      setResult({ topic: event.topic, ...event.state });
      setSources(event.sources || []);
      setSelectedReportId(event.reportId);
      setProgress(100);
      setProgressMessage("Completed");
      return;
    }

    if (event.type === "error") {
      setError(event.message || "Research stopped unexpectedly.");
    }
  }

  const activeReport = useMemo(() => {
    if (result) {
      return {
        topic: result.topic,
        report: result.report,
        feedback: result.feedback,
        search_results: result.search_results,
        scraped_content: result.scraped_content,
        sources,
      };
    }

    if (loadedReport) {
      return {
        topic: loadedReport.topic,
        report: loadedReport.final_report,
        feedback: loadedReport.critic_feedback,
        timestamp: loadedReport.timestamp,
        sources: loadedReport.sources || [],
      };
    }

    return null;
  }, [loadedReport, result, sources]);

  return (
    <div className="app-shell">
      <button
        className="history-toggle"
        type="button"
        onClick={() => setHistoryOpen((open) => !open)}
        aria-label={historyOpen ? "Close research history" : "Open research history"}
      >
        {historyOpen ? <ChevronLeft size={18} /> : <History size={18} />}
      </button>

      <aside className={`history-panel ${historyOpen ? "open" : "closed"}`}>
        <div className="history-heading">
          <div>
            <p>Saved Reports</p>
            <h2>Research History</h2>
          </div>
          <button type="button" onClick={() => setHistoryOpen(false)} aria-label="Close history">
            <ChevronLeft size={18} />
          </button>
        </div>

        <div className="history-list">
          {historyItems.length === 0 ? (
            <p className="empty-history">Completed research reports will appear here.</p>
          ) : (
            historyItems.map((item) => (
              <button
                className={`history-item ${selectedReportId === item.id ? "active" : ""}`}
                key={item.id}
                type="button"
                onClick={() => loadReport(item.id)}
              >
                <span>{item.topic}</span>
                <small>{item.timestamp}</small>
              </button>
            ))
          )}
        </div>

        <div className="history-actions">
          <button type="button" disabled={!selectedReportId} onClick={deleteSelectedReport}>
            <Trash2 size={16} />
            Delete Report
          </button>
          <button type="button" disabled={historyItems.length === 0} onClick={deleteAllHistory}>
            <XCircle size={16} />
            Delete All
          </button>
        </div>
      </aside>

      <main className={`main-content ${historyOpen ? "with-history" : ""}`}>
        <section className="hero">
          <div className="hero-badge">
            <Brain size={14} />
            Multi-Agent AI System
          </div>
          <h1>ResearchIQ</h1>
          <p>Enter any topic. Four specialized AI agents search, scrape, write, and critique a full research report automatically.</p>
        </section>

        <section className="pipeline">
          {STAGES.slice(0, 4).map((stage, index) => {
            const Icon = stage.icon;
            return (
              <React.Fragment key={stage.key}>
                <div className={`agent-node ${stage.key}`}>
                  <div>
                    <Icon size={24} />
                  </div>
                  <span>{stage.label.replace("...", "").replace(" Sources", "")}</span>
                </div>
                {index < 3 ? <ChevronRight className="pipeline-arrow" size={18} /> : null}
              </React.Fragment>
            );
          })}
        </section>

        <form className="search-row" onSubmit={runResearch}>
          <input
            value={topic}
            onChange={(event) => setTopic(event.target.value)}
            placeholder="e.g. impact of AI on healthcare, quantum computing, PCOS treatment..."
          />
          <button type="submit" disabled={running}>
            {running ? <Loader2 className="spin" size={18} /> : null}
            Research
            <ChevronRight size={18} />
          </button>
        </form>

        {(running || progress > 0 || error) && (
          <ProgressTracker
            progress={progress}
            message={progressMessage}
            stageStatuses={stageStatuses}
            error={error}
          />
        )}

        {activeReport ? <ReportView report={activeReport} /> : null}
      </main>
    </div>
  );
}

function ProgressTracker({ progress, message, stageStatuses, error }) {
  return (
    <section className="progress-card">
      <div className="progress-topline">
        <div>
          <h2>Research progress</h2>
          <p>{error || message}</p>
        </div>
        <strong>{progress}%</strong>
      </div>
      <div className="stage-grid">
        {STAGES.map((stage) => {
          const status = stageStatuses[stage.key] || "pending";
          return (
            <div className={`stage-card ${status}`} key={stage.key}>
              <span>{stage.label}</span>
              <small>{status === "success" ? "Done" : status === "running" ? "Running" : status === "error" ? "Error" : "Waiting"}</small>
            </div>
          );
        })}
      </div>
      <div className="progress-track">
        <div style={{ width: `${Math.min(progress, 100)}%` }} />
      </div>
    </section>
  );
}

function ReportView({ report }) {
  const [tab, setTab] = useState("report");
  const tabs = [
    ["report", "Final Report"],
    ["feedback", "Critic Feedback"],
    ["sources", "Sources"],
    ["search", "Search Results"],
    ["scraped", "Scraped Content"],
  ];

  return (
    <section className="report-card">
      <div className="report-heading">
        <div>
          <p>{report.timestamp ? `Saved ${report.timestamp}` : "Latest research"}</p>
          <h2>{report.topic}</h2>
        </div>
      </div>

      <div className="tabs">
        {tabs.map(([key, label]) => (
          <button className={tab === key ? "active" : ""} key={key} type="button" onClick={() => setTab(key)}>
            {label}
          </button>
        ))}
      </div>

      <div className="tab-panel">
        {tab === "report" ? <MarkdownText text={report.report || "No report generated."} /> : null}
        {tab === "feedback" ? <MarkdownText text={report.feedback || "No critic feedback saved."} /> : null}
        {tab === "sources" ? <SourceList sources={report.sources || []} /> : null}
        {tab === "search" ? <PreText text={report.search_results || "Search results are only available for newly completed runs."} /> : null}
        {tab === "scraped" ? <PreText text={report.scraped_content || "Scraped content is only available for newly completed runs."} /> : null}
      </div>
    </section>
  );
}

function MarkdownText({ text }) {
  return <div className="markdown-text">{text}</div>;
}

function PreText({ text }) {
  return <pre className="pre-text">{text}</pre>;
}

function SourceList({ sources }) {
  if (!sources.length) {
    return <p className="muted">No source URLs were found in this report.</p>;
  }

  return (
    <ol className="source-list">
      {sources.map((source) => (
        <li key={source}>
          <a href={source} target="_blank" rel="noreferrer">
            {source}
          </a>
        </li>
      ))}
    </ol>
  );
}

createRoot(document.getElementById("root")).render(<App />);
