import os
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

# 加载 .env 文件中的环境变量
load_dotenv()


class LLMClient:
    """大语言模型客户端。

    用于调用任何兼容 OpenAI 接口的模型服务，默认以流式方式返回结果。
    """

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        """初始化客户端。

        参数优先使用显式传入的值；未传入时回退到环境变量。

        Args:
            model: 模型 ID，缺省读取 ``LLM_MODEL_ID``。
            api_key: API 密钥，缺省读取 ``LLM_API_KEY``。
            base_url: 兼容 OpenAI 的服务地址，缺省读取 ``LLM_BASE_URL``。
            timeout: 请求超时秒数，缺省读取 ``LLM_TIMEOUT``（默认 60）。
        """
        model = model or os.getenv("LLM_MODEL_ID")
        api_key = api_key or os.getenv("LLM_API_KEY")
        base_url = base_url or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))

        if not model or not api_key or not base_url:
            raise ValueError("模型 ID、API 密钥和服务地址必须通过参数传入或在 .env 文件中配置。")

        # 经过校验后三者均非空，类型收窄为 str
        self.model: str = model
        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)

    def think(self, messages: List[ChatCompletionMessageParam], temperature: float = 0) -> Optional[str]:
        """调用大语言模型进行推理，并返回完整响应文本。

        Args:
            messages: 对话消息列表（OpenAI 消息格式）。
            temperature: 采样温度，默认 0 以获得更稳定的输出。

        Returns:
            模型生成的完整文本；调用失败时返回 ``None``。
        """
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )

            print("✅ 大语言模型响应成功：")
            collected_content: List[str] = []
            for chunk in response:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()  # 流式输出结束后换行
            return "".join(collected_content)

        except Exception as e:  # noqa: BLE001 - 演示项目统一兜底，避免中断主流程
            print(f"❌ 调用 LLM API 时发生错误：{e}")
            return None
