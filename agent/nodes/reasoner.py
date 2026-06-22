from langchain_core.messages import HumanMessage

from agent.state import AgentState
from agent.llm import get_llm


SYSTEM_INSTRUCTIONS = """You are an expert CS professor specializing in {subject_label}.
Your job is to give clear, accurate, exam-ready answers to CS students.

Guidelines:
- Structure answers: concept explanation → how it works → example → why it matters
- Use analogies to make hard concepts click
- Include formulas or algorithms where relevant
- Use **bold** for key terms
- Do NOT say "based on the Wikipedia context" — just answer naturally"""


def reason_and_answer(state: AgentState) -> dict:
    llm = get_llm()

    system_prompt = SYSTEM_INSTRUCTIONS.format(subject_label=state["subject_label"])
    user_prompt = _build_user_prompt(state)

    response = llm.invoke([HumanMessage(content=system_prompt + "\n\n" + user_prompt)])

    return {
        "answer": response.content,
        "steps_log": ["**LLM Reasoned** and generated answer"],
    }


def _build_user_prompt(state: AgentState) -> str:
    context = state["wiki_context"] or "Not available"
    return (
        f"Wikipedia Context (use if relevant):\n{context}\n\n"
        f"━━━\n"
        f"Student Question ({state['subject_label']}):\n{state['question']}\n\n"
        f"Give a complete, well-structured answer."
    )