import requests, json
from openai import OpenAI

class GPTClient:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def generate_report(self, prompt, report):        
        messages = [
            {
                "role": "user",
                "content": prompt + report
            }
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_completion_tokens=2000
        )
        gpt_answer = response.choices[0].message.content.strip()
    
        return self.parse_gpt_response(gpt_answer)

    def parse_gpt_response(self, gpt_answer):
        # Markdownのコードブロックを除去
        if gpt_answer.startswith("```json"):
            gpt_answer = gpt_answer.lstrip("```json").rstrip("```").strip()

        print(f"gpt_answer: {gpt_answer!r}")

        try:
            # JSON形式かどうかを確認し、パース
            parsed_response = json.loads(gpt_answer)
        except json.JSONDecodeError:
            # JSONでない場合、エラーを返す
            print(gpt_answer)
            return {"error": "Invalid JSON format"}

        # 必要なキーが存在するかを確認
        required_keys = {"subject", "body", "dall-e_prompt"}
        if not required_keys.issubset(parsed_response.keys()):
            return {"error": "Missing required keys: subject, body, dall-e_prompt"}

        # エラーがなければ 'noerror' を設定
        parsed_response["error"] = "noerror"
        return parsed_response

    def generate_image(self, prompt):
        response = self.client.images.generate(
            prompt=prompt,
            size = '256x256'
        )
        return response.data[0].url
