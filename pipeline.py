from typing import Callable, Optional

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

ProgressCallback = Callable[[str, str, int, Optional[str]], None]


def format_agent_error(error: Exception) -> str:
    error_text = str(error)

    if "rate_limit_exceeded" in error_text or "Rate limit reached" in error_text:
        retry_message = ""
        marker = "Please try again in "
        if marker in error_text:
            retry_after = error_text.split(marker, 1)[1].split(" Need", 1)[0].rstrip(".")
            retry_message = f" Try again in {retry_after}."

        return (
            "The model provider rate limit was reached, so the research run stopped."
            f"{retry_message}"
        )

    if "api_key" in error_text.lower() or "authentication" in error_text.lower():
        return "The model provider rejected the API credentials. Check your API key and try again."

    if "timeout" in error_text.lower():
        return "The agent request timed out. Please try again in a moment."

    return error_text


def _notify(
    callback: Optional[ProgressCallback],
    stage: str,
    status: str,
    progress: int,
    message: Optional[str] = None,
) -> None:
    if callback:
        callback(stage, status, progress, message)


def run_research_pipeline(topic: str, progress_callback: Optional[ProgressCallback] = None) -> dict:

    state = {}

    # search agent working

    _notify(progress_callback, "searching", "running", 10, "Searching for reliable sources...")
    try:
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["search_results"] = search_result['messages'][-1].content
        _notify(progress_callback, "searching", "success", 25, "Search completed.")
    except Exception as exc:
        clean_error = format_agent_error(exc)
        _notify(progress_callback, "searching", "error", 10, clean_error)
        raise RuntimeError(f"Search agent failed: {clean_error}") from exc



    # step 2 - reader agent

    _notify(progress_callback, "reading", "running", 35, "Reading and scraping source content...")
    try:
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state['scraped_content'] = reader_result['messages'][-1].content
        _notify(progress_callback, "reading", "success", 50, "Sources read successfully.")
    except Exception as exc:
        clean_error = format_agent_error(exc)
        _notify(progress_callback, "reading", "error", 35, clean_error)
        raise RuntimeError(f"Reader agent failed: {clean_error}") from exc



    # step 3 - writer agent

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    _notify(progress_callback, "writing", "running", 65, "Writing the research report...")
    try:
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })
        _notify(progress_callback, "writing", "success", 75, "Report draft completed.")
    except Exception as exc:
        clean_error = format_agent_error(exc)
        _notify(progress_callback, "writing", "error", 65, clean_error)
        raise RuntimeError(f"Writer agent failed: {clean_error}") from exc



    # critic report

    _notify(progress_callback, "critiquing", "running", 88, "Critiquing the final report...")
    try:
        state["feedback"] = critic_chain.invoke({
            "report": state['report']
        })
        _notify(progress_callback, "critiquing", "success", 95, "Critique completed.")
    except Exception as exc:
        clean_error = format_agent_error(exc)
        _notify(progress_callback, "critiquing", "error", 88, clean_error)
        raise RuntimeError(f"Critic agent failed: {clean_error}") from exc



    _notify(progress_callback, "completed", "success", 100, "Completed")
    return state

if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)
