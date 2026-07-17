import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy, ToolStrategy, AutoStrategy
#model传入方式有两种，一种是字符串， 一种是模型对象
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from rich import print as rprint
load_dotenv()
model = init_chat_model(
    model="qwen3.6:27b",          # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
class contractInfo(BaseModel):
    """用户联系方式"""
    name: str=Field(description="用户姓名")
    email: str = Field(description="用户邮箱")
    phone: str = Field(description="用户电话")
agent=create_agent(
    model=model,
    #ProviderStrategy策略 ollama不支持
    # response_format=ProviderStrategy(contractInfo)
    #ToolStrategy策略 普遍支持
    # response_format=ToolStrategy(contractInfo)
    #AutoStrategy策略，底层路由 根据情况调用上面两种之一的策略
    response_format=AutoStrategy(contractInfo)
)
response=agent.invoke({
    "messages":[
        HumanMessage("请从以下文本提取用户信息，小明邮箱为xiaoming@king.com，电话为12345678")
    ]
})
rprint(response)