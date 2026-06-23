from __future__ import annotations

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate(system_prompt: str, user_input: str) -> str:
    """Generate a single response from the Groq chat completion API."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7,
        max_tokens=2048,
    )
    return response.choices[0].message.content or ""

