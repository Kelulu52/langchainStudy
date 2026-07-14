from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pyexpat.errors import messages

model = init_chat_model(
    model="qwen3.6:27b",          # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
# messages=[{"role": "system", "content":"你是一个数学老师"},
#           {"role": "user", "content":"帮我解释一下庞加莱回归"}]
#多轮对话
messages=[{"role": "system", "content":"你是一个数学老师"},
          {"role": "user", "content":"1+1=？"},
          {"role": "assistant", "content":"2"},
          {"role": "user", "content":"我刚才问了什么问题"}]
#记忆

conversation=[{"role": "system", "content":"你是一个可爱的喵娘大模型，说话喜欢在末尾带喵"},
          {"role": "user", "content":"你好我是小明"}]
response1=model.invoke(conversation)
#print(f"Ai回复：{response1.content}")
conversation.append({"role": "assistant", "content":response1.content})
conversation.append({"role": "user", "content":"我的名字叫什么"})
#print((model.invoke(conversation)).content)
#消息输入
message3=[
    SystemMessage(content="你是一个可爱的喵娘大模型，说话喜欢在末尾带喵"),
    HumanMessage(content="你好我是小明")
]
#print(model.invoke(message3).content)
#记忆传输
conversation2=[
    SystemMessage(content="你是一个可爱的喵娘大模型，说话喜欢在末尾带喵"),
    HumanMessage(content="你好我是小明")
]
respse2=model.invoke(conversation2)
print(respse2.content)
conversation2.append(
    AIMessage(content=respse2.content)
)
conversation2.append(
    HumanMessage(content="我的名字叫什么"))
print(model.invoke(conversation2).content)