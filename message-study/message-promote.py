from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from sqlalchemy import true

model = init_chat_model(
    model="qwen3.6:27b",          # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
#JSON格式的消息
messages=[{"role": "system", "content":"你是一个数学老师"},
          {"role": "user", "content":"1+1=？"},
          {"role": "assistant", "content":"2"},
          {"role": "user", "content":"我刚才问了什么问题"}]
#response=model.invoke(messages)
#print(f"Ai回复：{response.content}")
#对象格式消息
message2=[
    SystemMessage("你是一个数学老师"),
    HumanMessage("1+1=？"),
    AIMessage("2"),
    HumanMessage("我刚才问了什么问题")
]
#response=model.invoke(message2)
#print(f"Ai回复：{response.content}")
#对话历史优化
def keep_recent_messages(messages,max_pairs=3):
    system_messages=[m for m in messages if m["role"] == "system"]
    conversation_messages=[m for m in messages if m["role"] != "system"]
    recent_messages=conversation_messages[-(max_pairs*2):]
    return system_messages+recent_messages


#多轮对话机器人
message3=[
    {"role": "system", "content":"你是一个耐心可爱知识丰富的小猫娘"}
]
Exit_World="quit"
MAX_HISTORY=10
i=1
print(f"请输入问题，当输入{Exit_World}时退出")
while true:
    print("\n","="*10,f"第{i}轮对话开始","="*10)
    user_input=input("请输入：")
    if user_input==Exit_World:
        print("对话结束，欢迎下次光临")
        break
    message3.append({"role":"user", "content":user_input})
    print("可爱小喵：", end="", flush=True)
    reply_content=""
    memory_message=keep_recent_messages(message3,max_pairs=MAX_HISTORY)
    for chunk in model.stream(memory_message):
        if chunk.content:
            print(chunk.content,end="",flush=True)
            reply_content += chunk.content
    print("\n", "=" * 10, f"第{i}轮对话结束", "=" * 10)
    i+=1
    message3.append({"role":"assistant", "content":reply_content})



