from openai import OpenAI
import asyncio

class DeepSeekClient:
    """DeepSeek API客户端封装"""
    
    def __init__(self):
        """初始化API客户端
        Args:
            api_key: DeepSeek API密钥
        """
        self.client = OpenAI(
            api_key="sk-33683be52d6c4433adb41c439e553c37",
            base_url="https://api.deepseek.com"
        )
    
    def chat_completion(self, messages: list, content: str = "You are a helpful assistant", **kwargs):
        """统一DeepSeek聊天API调用
        Args:
            messages: 消息列表
            response_format: 响应格式要求
            **kwargs: 其他API参数
        Returns:
            API响应内容
        """

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": content},
                {"role": "user", "content": messages},
            ],
            stream=False
        )
        return response.choices[0].message.content


# async def run():
#     llm = DeepSeekClient()
#     res = await llm.chat_completion("你是谁？")
#     print(res)


# if __name__=="__main__":
#     asyncio.run(run())

