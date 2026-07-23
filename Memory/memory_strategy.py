from typing import Any

from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model, after_model
from langchain_core.messages import HumanMessage, RemoveMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.runtime import Runtime

from model.ollamaInit import model2,model
#消息裁剪策略
@before_model
def trim_messages(state:AgentState,runtime:Runtime)->dict[str,Any] |None:
    messages = state["messages"]
    if len(messages)<=3:
        return None
    first_message = messages[0]
    recent_messages = messages[-3:] if len(messages)%2==0 else messages[-4:]
    new_messages = [first_message] + recent_messages
    return {
        "messages":[
            RemoveMessage(id=REMOVE_ALL_MESSAGES),
            *new_messages
        ],
    }
#消息删除策略
#还可以用摘要中间件
@after_model
def delete_old_messages(state: AgentState, runtime: Runtime) -> dict | None:
    messages = state["messages"]
    # 保持最近的 5 条消息
    if len(messages) > 5:
    # 框架中通常使用 RemoveMessage 来标记删除，并返回更新状态。
        to_delete = len(messages) - 5
        return {"messages": [RemoveMessage(id=m.id) for m in
                         messages[:to_delete]]}
    return None
agent = create_agent(
    model=model,
    # middleware=[trim_messages],
    middleware=[delete_old_messages],
    checkpointer=InMemorySaver(),
)
config: RunnableConfig = {"configurable": {"thread_id": "1"}}
agent.invoke({"messages": [HumanMessage("你好，我是老王")]}, config)
agent.invoke({"messages": [HumanMessage("从现在起，你叫小王")]}, config)
agent.invoke({"messages": [HumanMessage("今天天气不错")]}, config)
final_response = agent.invoke({"messages": [HumanMessage("告诉我，你是谁？我是谁？")]}, config)
for msg in final_response["messages"]:
    msg.pretty_print()