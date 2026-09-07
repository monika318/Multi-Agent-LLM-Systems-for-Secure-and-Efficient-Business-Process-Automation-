"""
Thin wrapper around the OpenAI client. Every agent calls
client.chat(system_prompt, user_prompt) and gets back raw text, which the
agent then parses as JSON via extract_json().
"""
import json
import os
from openai import OpenAI


class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        self._client = OpenAI()  # reads OPENAI_API_KEY from environment
        self._model = model
        self.call_count = 0

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        self.call_count += 1
        response = self._client.chat.completions.create(
            model=self._model,
            max_tokens=500,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content


def extract_json(text: str) -> dict:
    """Best-effort extraction of a single JSON object from an LLM response,
    tolerant of ```json fences and any leading/trailing prose."""
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"No JSON object found in LLM response: {text[:200]!r}")
    return json.loads(text[start:end + 1])