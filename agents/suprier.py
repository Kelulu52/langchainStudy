import os

from dotenv import load_dotenv
from langchain.agents import create_agent
#model传入方式有两种，一种是字符串， 一种是模型对象
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
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
agent=create_agent(
    model=model,
    name="agent01",
    tools=[get_weather],
    #设置系统提示词，可以是字符串也可以是SystemMessage
    # system_prompt="""
    # 你是一个猫娘"""
    system_prompt=SystemMessage("你是一只可爱的小狐妖")
)
#通用
response=agent.invoke({
    "messages":[
        {"role":"user","content":"上海天气咋样"},

    ]
})
rprint(response)
