"""
LLM 模型初始化模块

负责从环境变量加载配置并初始化 LangChain 聊天模型实例。
"""
from dotenv import load_dotenv, find_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

# 加载环境变量
load_dotenv(find_dotenv())


def _get_required_env(key: str, default: str = "") -> str:
    """获取必需的环境变量，缺失时给出明确提示。"""
    value = os.getenv(key, default)
    if not value:
        raise ValueError(f"环境变量 {key} 未配置，请检查 .env 文件")
    return value


def create_chat_model() -> BaseChatModel:
    """
    创建并返回聊天模型实例。

    Returns:
        BaseChatModel: 配置好的 LangChain 聊天模型

    Raises:
        ValueError: 当必需的环境变量缺失时
    """
    model_name = _get_required_env("LLM_QWEN_PLUS")
    api_key = _get_required_env("DASHSCOPE_API_KEY")
    base_url = _get_required_env("DASHSCOPE_BASE_URL")

    return init_chat_model(
        model=model_name,
        model_provider="openai",
        api_key=api_key,
        base_url=base_url,
    )


# 全局模型实例（模块加载时初始化）
try:
    model = create_chat_model()
except ValueError as e:
    # 延迟到实际使用时再报错，避免导入阶段就崩溃
    model = None
    _init_error = str(e)
else:
    _init_error = None


if __name__ == "__main__":
    if model is None:
        print(f"模型初始化失败: {_init_error}")
    else:
        print(model.invoke("你是谁"))