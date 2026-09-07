from dotenv import load_dotenv
load_dotenv()

from src.llm_client import LLMClient, extract_json

client = LLMClient()

system_prompt = """You classify a facility ticket. Respond ONLY with JSON:
{"category": string, "urgency": "low"|"medium"|"high"|"critical"}
"""

user_prompt = "Ticket: Rooftop chiller unit 3 tripped on high pressure fault."

raw_text = client.chat(system_prompt, user_prompt)
print("RAW RESPONSE:")
print(raw_text)
print()

parsed = extract_json(raw_text)
print("PARSED JSON:")
print(parsed)
print("Category:", parsed["category"])
print("Urgency:", parsed["urgency"])