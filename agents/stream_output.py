from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from rich import print as rprint
load_dotenv(verbose=True)
model = init_chat_model(
    model="qwen3.6:27b",
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
customer_agent=create_agent(
    model=model,
    )
for chunk in customer_agent.stream(
    {
    "messages":[
        HumanMessage("你好"),
    ]},
    #以下多模式可以混合使用
    #values 每个步骤结束输出完整的状态信息
    # stream_mode="values"
    #updates 每次输出增加了的信息 默认设置
    # stream_mode="updates"
    #messages 可用作模拟deepseek会话类似的输出效果
    # stream_mode="messages"
    #tasks 输出任务开始和结束的时间
    # stream_mode="tasks"
    #debug 比tasks多一些步骤，时间戳，task类型
    # stream_mode="debug"
    # stream_mode="checkpoints"
    #在工具里自定义
    # stream_mode="custom"
):
    # print(chunk[0].content,end="",flush=True)
    rprint(chunk)
    print("-"*50)
