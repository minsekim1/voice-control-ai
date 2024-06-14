import requests

# @docs https://platform.openai.com/docs/models

class GPT:
    def __init__(self, api_key="sk-proj-y4ONynrZTJlk5YC7tkxYT3BlbkFJRLp3zeGrfZrULgjp2ftz", api_url="https://api.openai.com/v1/chat/completions"):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_chat_completion(self, user_message, max_tokens=150, temperature=0.7):
        # Message format update
        data = {
            "model": "gpt-3.5-turbo",  # Specific model version
            "messages": [
                {"role": "user", "content": user_message}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = requests.post(self.api_url, headers=self.headers, json=data)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]  # Updated to extract message content correctly
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

# # 예제 사용법
# if __name__ == "__main__":
#     api_key = ""
#     gpt4 = GPT(api_key)
    
#     prompt = "Transcription: Hello, how can I help you today?"
#     try:
#         response_text = gpt4.get_completion(prompt)
#         print("GPT-4 Response:", response_text)
#     except Exception as e:
#         print("Error:", e)
