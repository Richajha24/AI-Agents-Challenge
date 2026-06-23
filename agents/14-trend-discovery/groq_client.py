from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def _get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    return Groq(api_key=api_key)


def generate(system_prompt: str, user_input: str) -> str:
    """Generate a trend discovery report using Groq chat completions."""

    client = _get_client()

    # Using a chat-style completion.
    # Model choice can be changed without affecting the rest of the agent.
    resp = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        temperature=float(os.getenv("GROQ_TEMPERATURE", "0.4")),
    )

    # Groq SDK response shape is compatible with OpenAI-style.
    content = resp.choices[0].message.content
    return content.strip() if content else ""

