import requests
import json
from datetime import datetime

def llama_intent_parser(user_input):
    today = datetime.today().strftime('%Y-%m-%d')

    prompt = f"""
You are a smart trend analysis assistant.

Your task is to extract the following fields from the user's message as a valid JSON object:
- intent (e.g., "trend")
- category (e.g., "products", "machines"). If unclear, default to "products".
- timeframe (e.g., "last month", "this week", "today", "between May and July"). Leave empty only if no time is mentioned.
- start_date (in YYYY-MM-DD format, or empty string if no timeframe). Use today's date {today} and timeframe to calculate real dates if needed.
- end_date (in YYYY-MM-DD format, or empty string if no timeframe). Use today's date {today} and timeframe to calculate real dates if needed.
- quantity if singular(e.g.,"product","machine") use 1,if plural with number mentioned(e.g.,"best 5","6 products") then use that number.if no number and plural(e.g.,"products","machines")use 3 as default.
⏳ Timeframe rules:
- If timeframe is empty → start_date and end_date must be empty.
- If timeframe is not empty → start_date and/or end_date must be provided.
- For example:(if today is 2025-07-17)
  - "this month" → start_date = 2025-07-01, end_date = 2025-07-17 
  - "last month" → start_date = 2025-06-01, end_date = 2025-06-30 
  - "last 2 weeks" → start_date = 2025-07-03, end_date = 2025-07-17

🔢 quantity rules:
- If user says a number, use that number.
- If  plural (like "products", "machines") and no number is mentioned → top_n = 3
- If  singular (like "product", "machine") or vague → top_n = 1.
examples:
🔹 Input: Trend now
📤 Parsed Output: 'intent': 'trend', 'category': 'products', 'timeframe': '', 'start_date': '', 'end_date': '', 'quantity': 1

🔹 Input: Give me trending products today
📤 Parsed Output: 'intent': 'trend', 'category': 'products', 'timeframe': 'today', 'start_date': '2025-07-17', 'end_date': '2025-07-17', 'quantity': 3

🔹 Input: I need popular 7 items after March
📤 Parsed Output: ('intent': 'trend', 'category': 'products', 'timeframe': 'after march', 'start_date': '2025-03-01', 'end_date': '', 'quantity': 7)

🔹 Input: Show 4 trend before November
📤 Parsed Output: ('intent': 'trend', 'category': 'products', 'timeframe': 'before november', 'start_date': '', 'end_date': '2025-11-30', 'quantity': 4)

Return only a JSON object. No explanation or markdown.
If the input message is irrelevant or not about trending products/machines (e.g., “hi”, “how are you”), return this:
( "intent": "none" )




User: "{user_input}"
"""

    # response = requests.post(
    #     "http://localhost:11434",
    #     json={
    #         "model": "gemma3",
    #         "prompt": prompt,
    #         "stream": False
    #     }
    # )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3",
            "prompt": prompt,
            "stream": False
        }
    )

    try:
        output_text = response.json()["response"].strip()

        # Clean markdown if accidentally returned
        if output_text.startswith("```json"):
            output_text = output_text.replace("```json", "").replace("```", "").strip()

        return json.loads(output_text)

    except Exception as e:
        print("❌ Error:", e)
        print("📦 Raw output:", output_text)
        return None