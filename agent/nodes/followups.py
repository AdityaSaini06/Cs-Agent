import json
import re

from langchain_core.messages import HumanMessage

from agent.state import AgentState
from agent.llm import get_llm

FOLLOW_UP_COUNT = 3

DEFAULT_FALLBACK_TEMPLATE = [
    "How does this concept apply in real systems?",
    "What are common interview questions on {subject_label}?",
    "What are the trade-offs involved?",
]


def generate_follow_ups(state: AgentState) -> dict:
    llm = get_llm()

    prompt = (
        f"Based on this CS question about {state['subject_label']}:\n"
        f'"{state["question"]}"\n\n'
        f"Suggest exactly {FOLLOW_UP_COUNT} follow-up questions a student should "
        f"explore next.\n"
        f"Return ONLY a JSON array of {FOLLOW_UP_COUNT} strings. No other text.\n"
        f'Example: ["What is X?", "How does Y differ from Z?", "Explain W"]'
    )

    follow_ups = _try_generate(llm, prompt)
    if not follow_ups:
        follow_ups = [
            template.format(subject_label=state["subject_label"])
            for template in DEFAULT_FALLBACK_TEMPLATE
        ]

    return {
        "follow_ups": follow_ups,
        "steps_log": [f"**Generated** {len(follow_ups)} follow-up questions"],
    }


def _try_generate(llm, prompt: str) -> list[str]:
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        match = re.search(r"\[.*?\]", response.content, re.DOTALL)
        if not match:
            return []
        return json.loads(match.group())
    except (json.JSONDecodeError, AttributeError, Exception):
        return []