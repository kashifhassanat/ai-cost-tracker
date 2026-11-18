import json
import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from groq import Groq

# Load API keys and model names
load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
groq_model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

# Checking if any API key is missing
if not gemini_key:
    print("Error: GEMINI_API_KEY is missing in your .env file!")
    sys.exit(1)

if not groq_key:
    print("Error: GROQ_API_KEY is missing in your .env file!")
    sys.exit(1)

# Geting the prompt from the terminal command
if len(sys.argv) < 2:
    print('Usage: uv run tracker.py "Your prompt here"')
    sys.exit(1)

prompt = sys.argv[1]

# Send the prompt to Google Gemini
gemini_client = genai.Client()
start_time = time.time()
gemini_response = gemini_client.models.generate_content(
    model=gemini_model, contents=prompt
)
gemini_seconds = round(time.time() - start_time, 2)

gemini_reply = gemini_response.text
gemini_input = gemini_response.usage_metadata.prompt_token_count
gemini_output = gemini_response.usage_metadata.candidates_token_count

# Calculate Gemini cost
gemini_in_price = 0.075
gemini_out_price = 0.30
gemini_cost = (gemini_input * gemini_in_price / 1000000) + (
    gemini_output * gemini_out_price / 1000000
)

# Sending same prompt to Groq
groq_client = Groq()
start_time = time.time()
groq_response = groq_client.chat.completions.create(
    model=groq_model, messages=[{"role": "user", "content": prompt}]
)
groq_seconds = round(time.time() - start_time, 2)

groq_reply = groq_response.choices[0].message.content
groq_input = groq_response.usage.prompt_tokens
groq_output = groq_response.usage.completion_tokens

# Calculate Groq cost
groq_in_price = 0.59
groq_out_price = 0.79
groq_cost = (groq_input * groq_in_price / 1000000) + (
    groq_output * groq_out_price / 1000000
)

# Printing both replies and the comparison table

print("\n--- GEMINI ---")
print(gemini_reply)

print("\n--- GROQ ---")
print(groq_reply)

print("\nProvider | Input | Output | Seconds | Cost (USD)")
print("gemini   |", gemini_input, "|", gemini_output, "|", gemini_seconds, "| $", round(gemini_cost, 6))
print("groq     |", groq_input, "|", groq_output, "|", groq_seconds, "| $", round(groq_cost, 6))

# Save the structured results to results.json
data = [
    {
        "provider": "gemini",
        "model": gemini_model,
        "reply": gemini_reply,
        "input_tokens": gemini_input,
        "output_tokens": gemini_output,
        "input_price_per_m": gemini_in_price,
        "output_price_per_m": gemini_out_price,
        "cost_usd": round(gemini_cost, 8),
    },
    {
        "provider": "groq",
        "model": groq_model,
        "reply": groq_reply,
        "input_tokens": groq_input,
        "output_tokens": groq_output,
        "input_price_per_m": groq_in_price,
        "output_price_per_m": groq_out_price,
        "cost_usd": round(groq_cost, 8),
    },
]

with open("results.json", "w") as file:
    json.dump(data, file, indent=2)