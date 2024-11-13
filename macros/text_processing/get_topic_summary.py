from openai import OpenAI

def get_topic_summary(text):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system", 
                "content": "Generate a very brief topic that captures the main theme of the text."
            },
            {
                "role": "user",
                "content": f"Generate a brief topic for this text: {text}"
            }
        ],
        temperature=0.3,
        max_tokens=20
    )
    return response.choices[0].message.content.strip() 