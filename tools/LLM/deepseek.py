import requests
from typing import Dict, Any, Optional
from config.config import PROMPT, load_model_config, load_api_key
from time import time

class DeepSeekAPI:
    def __init__(self):
        # 加载DeepSeek模型配置
        config = load_model_config('deepseek')
        self.base_url = config['base_url']
        self.model = config['model']
        self.api_key = load_api_key('deepseek')

    def ask(self, question: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": PROMPT.format(time(), question)
                }
            ]
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"DeepSeek API request failed: {str(e)}")