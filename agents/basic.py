import os

from dotenv import load_dotenv
from langchain.agents import create_agent
#model传入方式有两种，一种是字符串， 一种是模型对象
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from rich import print as rprint
load_dotenv()
model = init_chat_model(
    model="qwen3.6:27b",          # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
#自定义工具
@tool
def get_weather(city:str):
    """
    查询天气工具

    Args:
        city:具体城市
    """
    return f"{city}天气晴朗"
#内置工具
web_search=TavilySearch(
    max_results=2,
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
)
agent=create_agent(
    model=model,
    tools=[get_weather,web_search],
)
#通用
response=agent.invoke({
    "messages":[
        {"role":"system","content":"你是一只可爱的小猫娘"},
        {"role":"user","content":"请帮我查一下2024年诺贝尔物理学奖得主是谁"},

    ]
})
rprint(response)
