# Simple Ai Cost Tracker which uses GEMINI_MODEL (gemini-3.5-flash-lite) and GROQ_MODEL (openai/gpt-oss-20b)

# How to Setup and Run?

1. Setup Envirnment Virables

Copy .env.example to .env and add your Gemini and Groq API keys:

GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
GROQ_MODEL=openai/gpt-oss-20b

2. Run Tracker

uv run tracker.py "Explain AI  in one sentence."

Output:

--- GEMINI ---
Artificial intelligence is the simulation of human thinking processes by computer systems, enabling them to learn, reason, and solve problems autonomously.

--- GROQ ---
Artificial Intelligence is the design of computer systems that can perform tasks normally requiring human intelligence—such as learning, reasoning, and problem‑solving—by using algorithms and data.

Provider | Input | Output | Seconds | Cost (USD)
gemini   | 8 | 25 | 4.58 | $ 8e-06
groq     | 78 | 122 | 0.61 | $ 0.000142

Motivation:

This was my First IEC Assignment which was of creating a Two providercost tracker. I learned how to call two LLM API's from one python script. I also learned how two different models tokenize the exact same prompt differently while keeping secret keys safe using .env and .gitignore.