from typing import Iterator

from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.nodes import (
    classify_subject,
    retrieve_context,
    reason_and_answer,
    generate_follow_ups,
)


def build_cs_agent():
    graph = StateGraph(AgentState)

    graph.add_node("classify", classify_subject)
    graph.add_node("retrieve", retrieve_context)
    graph.add_node("answer", reason_and_answer)
    graph.add_node("follow_ups", generate_follow_ups)

    graph.set_entry_point("classify")
    graph.add_edge("classify", "retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", "follow_ups")
    graph.add_edge("follow_ups", END)

    return graph.compile()


def run_cs_agent(question: str) -> Iterator[dict]:
    graph = build_cs_agent()

    initial_state: AgentState = {
        "question": question,
        "subject": "",
        "subject_label": "",
        "wiki_context": "",
        "answer": "",
        "follow_ups": [],
        "steps_log": [f"**Question received**: _{question}_"],
    }

    yield from graph.stream(initial_state)