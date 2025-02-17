from openai import OpenAI,RateLimitError
import os
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

try:
    completion = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages=[
            {"role": "system", "content": "You are Claude, the notorius crab from Peggle."},
            {"role": "user", "content": "Write a haiku about recursion in programming."}
            ]
        )
    print(completion.choices[0].message)

except RateLimitError as e:
    print(e)
    print(type(e))

