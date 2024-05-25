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
                "content": [
                    {"type": "text", "text": prompt + report}
                ]
            }
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.5,
            messages=messages,
            max_tokens=1000,
            response_format={ "type": "json_object" }
        )
        gpt_answer = response.choices[0].message.content.strip()
    
        return self.parse_gpt_response(gpt_answer)

    def parse_gpt_response(self, gpt_answer):
        try:
            # JSON形式かどうかを確認
            parsed_response = json.loads(gpt_answer)
            
            # 必要なキーが存在するかを確認
            required_keys = {"subject", "body", "dall-e_prompt"}
            if not required_keys.issubset(parsed_response.keys()):
                return {"error": "Missing required keys: subject, body, prompt"}

            parsed_response["error"] = "noerror"
            return parsed_response

        except json.JSONDecodeError:
            print(gpt_answer)
            return {"error": "Response is not valid JSON"}

    def generate_image(self, prompt):
        response = self.client.images.generate(
            prompt=prompt,
            size = '256x256'
        )
        return response.data[0].url
