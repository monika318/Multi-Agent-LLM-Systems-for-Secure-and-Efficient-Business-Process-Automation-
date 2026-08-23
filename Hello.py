import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # reads .env into environment variables

key = os.environ.get("OPENAI_API_KEY", "")
print(f"Key length: {len(key)}, starts with: {key[:8]!r}")

client = OpenAI()  # picks up OPENAI_API_KEY automatically

response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=200,
    messages=[
        {"role": "user", "content": "In one sentence, what is segregation of duties?"}
    ],
)

print(response.choices[0].message.content)