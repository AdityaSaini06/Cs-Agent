import os
from langchain_groq import ChatGroq


def get_llm(temperature: float = 0.3) -> ChatGroq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "Set 'GROQ_API_KEY' environment variable or pass it via the UI."
        )

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=temperature,
    )