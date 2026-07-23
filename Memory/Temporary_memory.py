from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from model.ollamaInit import model2,model
#1.内存级记忆，单线程有用
checkpoint=InMemorySaver()
agent=create_agent(
    model=model,
    tools=[],
    #引入
    checkpointer=checkpoint,
)
config={
    "configurable":{
        "thread_id":"1"
    }
}
print("\n第一轮对话：")
response1 = agent.invoke({
    "messages": [HumanMessage("我叫张三")]},
    config=config  # 传入 config
)
print(f"Agent: {response1['messages'][-1].content}")
print("\n第二轮对话：")
response2 = agent.invoke({
    "messages": [HumanMessage("我叫什么？")]},
    config=config  # 使用相同的 thread_id
)
print(f"Agent: {response2['messages'][-1].content}")
