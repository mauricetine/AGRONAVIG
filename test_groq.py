import os
from groq import Groq
from dotenv import load_dotenv

# Charger le .env du backend
env_path = os.path.join('agronavig-backend', '.env')
load_dotenv(env_path)

api_key = os.getenv('GROQ_API_KEY')
model = os.getenv('GROQ_MODEL')

print(f"Testing Groq with model: {model}")
print(f"API Key starts with: {api_key[:10]}...")

try:
    client = Groq(api_key=api_key)
    # Test simple sans reasoning_effort pour verifier la connectivite de base
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Bonjour, es-tu pret ?",
            }
        ],
        model=model,
    )
    print("SUCCESS: Response received")
    print(f"Response: {chat_completion.choices[0].message.content}")
except Exception as e:
    print(f"ERROR: {e}")
