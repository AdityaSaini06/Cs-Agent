from agent.state import AgentState
from agent.tools import wikipedia_search

MAX_CONTEXT_CHARS = 3000
MIN_USEFUL_CONTEXT_CHARS = 300


def retrieve_context(state: AgentState) -> dict:
    search_query = f"{state['question']} {state['subject_label']}"
    context = wikipedia_search(search_query)

    if len(context) < MIN_USEFUL_CONTEXT_CHARS:
        context += "\n\n" + wikipedia_search(state["subject_label"])

    log_message = (
        f"**Wikipedia Retrieved**: {len(context)} chars of context"
        if context else
        "**Wikipedia**: No context found, relying on model knowledge"
    )

    return {
        "wiki_context": context[:MAX_CONTEXT_CHARS],
        "steps_log": [log_message],
    }