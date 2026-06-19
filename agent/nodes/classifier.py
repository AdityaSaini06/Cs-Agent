from langchain_core.messages import HumanMessage

from agent.state import AgentState
from agent.llm import get_llm
from agent.subjects import SUBJECTS, SUBJECT_KEYWORDS


def classify_subject(state: AgentState) -> dict:
    question_lower = state["question"].lower()

    best_subject = _score_by_keywords(question_lower)

    if best_subject is None:
        best_subject = _classify_with_llm(state["question"])

    label = SUBJECTS[best_subject]

    return {
        "subject": best_subject,
        "subject_label": label,
        "steps_log": [f"**Subject Detected**: {label}"],
    }

def _score_by_keywords(question_lower: str) -> str | None:
    scores = {subject: 0 for subject in SUBJECTS}

    for subject, keywords in SUBJECT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in question_lower:
                scores[subject] += 1

    best_subject = max(scores, key=scores.get)
    return best_subject if scores[best_subject] > 0 else None

def _classify_with_llm(question: str) -> str:
    llm = get_llm()
    subjects_list = "\n".join(f"- {key}: {label}" for key, label in SUBJECTS.items())

    response = llm.invoke([HumanMessage(content=(
        f"Classify this CS question into exactly one subject key.\n"
        f"Subjects:\n{subjects_list}\n\n"
        f"Question: {question}\n\n"
        f"Reply with ONLY the subject key (e.g. 'os' or 'ml')."
    ))])

    detected = response.content.strip().lower().strip('"\'')
    return detected if detected in SUBJECTS else "unknown"