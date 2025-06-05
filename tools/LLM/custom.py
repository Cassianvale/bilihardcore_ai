import requests
from typing import Dict, Any, Optional
from config.config import PROMPT, load_model_config, load_api_key
from time import time

class APIUtils:
    @staticmethod
    def format_api_url(base_url: str) -> str:
        """
        格式化 API URL

        /结尾忽略v1版本，#结尾强制使用输入地址
        
        Args:
            base_url: 基础 API URL
            
        Returns:
            str: 格式化后的完整 API URL
        """
        if not base_url:
            return ""
            
        if base_url.endswith('/'):
            return f"{base_url}chat/completions"
        elif base_url.endswith('#'):
            return base_url.replace('#', '')
        else:
            return f"{base_url}/v1/chat/completions"

class CustomAPI:
    def __init__(self):
        # 始终从文件重新加载最新配置，确保获取到用户在GUI中最新保存的设置
        config = load_model_config('custom')
        
        self.base_url = config['base_url']
        self.model = config['model']
        # 同样从文件实时加载API密钥
        self.api_key = load_api_key('custom')
        
        # 添加调试信息，帮助用户确认配置是否正确
        print(f"[DEBUG] CustomAPI 配置加载:")
        print(f"  - base_url: '{self.base_url}'")
        print(f"  - model: '{self.model}'")
        print(f"  - api_key: '{'*' * min(8, len(self.api_key)) if self.api_key else '(空)'}'")
        
        if not self.base_url:
            raise ValueError("自定义模型的base_url为空，请在GUI设置中配置正确的API基础URL")
        if not self.model:
            raise ValueError("自定义模型的model为空，请在GUI设置中配置正确的模型名称")
        if not self.api_key:
            raise ValueError("自定义模型的API密钥为空，请在GUI设置中配置正确的API密钥")

    def ask(self, question: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        """根据API格式自动判断使用不同的API格式"""
        if 'dashscope' in self.base_url.lower() or 'aliyuncs' in self.base_url.lower():
            return self.ask_dashscope_format(question, timeout)
        else:
            # 默认使用OpenAI兼容格式
            return self.ask_openai_format(question, timeout)

    def ask_openai_format(self, question: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        """使用OpenAI格式的API调用"""
        # 使用新的URL格式化逻辑
        url = APIUtils.format_api_url(self.base_url)
        
        # 添加调试信息
        print(f"[DEBUG] ask_openai_format:")
        print(f"  - 原始base_url: '{self.base_url}'")
        print(f"  - 格式化后URL: '{url}'")
        
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
            raise Exception(f"自定义模型API请求失败: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"解析API响应失败: {str(e)}，请检查模型配置是否正确")

    def ask_dashscope_format(self, question: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        """使用阿里云DashScope API格式的调用"""
        # 确保URL正确指向chat/completions端点
        url = f"{self.base_url}/compatible-mode/v1/chat/completions"
        
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
            raise Exception(f"阿里云DashScope API请求失败: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"解析API响应失败: {str(e)}，请检查模型配置是否正确")

    def ask_custom_format(self, question: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        """使用自定义格式的API调用，适配其他格式的模型API"""
        url = f"{self.base_url}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # 通用数据格式，可根据实际API调整
        data = {
            "model": self.model,
            "prompt": PROMPT.format(time(), question)
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=timeout
            )
            response.raise_for_status()
            
            # 尝试通用的响应解析，根据实际情况可能需要调整
            result = response.json()
            if "choices" in result and isinstance(result["choices"], list) and len(result["choices"]) > 0:
                if "message" in result["choices"][0]:
                    return result["choices"][0]["message"]["content"]
                elif "text" in result["choices"][0]:
                    return result["choices"][0]["text"]
            elif "response" in result:
                return result["response"]
            elif "content" in result:
                return result["content"]
            elif "answer" in result:
                return result["answer"]
            elif "output" in result:
                return result["output"]
            elif "result" in result:
                return result["result"]
            else:
                # 如果找不到标准格式，返回整个响应，让用户自己查看
                return str(result)
        except requests.exceptions.RequestException as e:
            raise Exception(f"自定义模型API请求失败: {str(e)}")
        except Exception as e:
            raise Exception(f"解析API响应失败: {str(e)}，请检查模型配置是否正确") 