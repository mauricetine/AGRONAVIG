import os
from groq import Groq
from dotenv import load_dotenv

env_path = os.path.join('agronavig-backend', '.env')
load_dotenv(env_path)

api_key = os.getenv('GROQ_API_KEY')
model = os.getenv('GROQ_MODEL')

try:
    client = Groq(api_key=api_key)
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Test"}],
        model=model,
        reasoning_effort="medium"
    )
    print("SUCCESS: reasoning_effort accepted")
except Exception as e:
    print(f"ERROR with reasoning_effort: {e}")
