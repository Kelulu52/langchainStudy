from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from model.ollamaInit import model2
load_dotenv(verbose=True)
model = init_chat_model(
    model="qwen3.6:27b",   # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    profile={"max_input_tokens": 128_000}, #128KB
    base_url="http://10.20.62.52:11434"
)
messages = [
    SystemMessage("你是个非常友好的AI助手"),
    HumanMessage("你好啊，我是老王，你是谁？"),
    AIMessage("你好老王，我是小王"),
    HumanMessage("好的小王，很高兴认识你"),
    AIMessage("你高兴得太早了"),
    HumanMessage("呵呵，你什么意思")
]
agent=create_agent(
    model=model2,
    middleware=[
        #使用子模型对历史记录进行总结
        SummarizationMiddleware(
            model=model,
            trigger=[
                ("tokens",100),
                ("messages",6),
                ("fraction",0.001)

            ],
            keep=("messages",2),
            summary_prompt="对历史消息摘要，消息列表如下\n{messages}"
        )
    ]
)
response=agent.invoke(
    {"messages":messages}
)
for msg in response["messages"]:
    msg.pretty_print()