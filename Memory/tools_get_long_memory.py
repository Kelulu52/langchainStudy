from typing import NotRequired

from langchain.agents import create_agent, AgentState
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from langgraph.store.memory import InMemoryStore
from model.ollamaInit import model2,model
store=InMemoryStore()
#自定义类
class CustomState(AgentState):
    user_id:NotRequired[str]

@tool(parse_docstring=True)
def save_user_info(name:str,runtime:ToolRuntime)->str:
    """
    将用户信息保存在长期记忆

    Args:
        name:用户名字
        runtime:工具的运行时环境

    Returns:
        str:保存的状态
    """
    namespace=("users",)
    key=runtime.state["user_id"]
    value={"name":name}
    runtime.store.put(namespace,key,value)
    return "saved"
@tool(parse_docstring=True)
def get_user_info(runtime:ToolRuntime)->str:
    """
    从长期记忆中读取用户信息

    Returns:
        str: 用户信息
    """
    namespace=("users",)
    key=runtime.state["user_id"]
    item=runtime.store.get(namespace,key)
    return str(item.value) if item else "unkonwn"

agent=create_agent(
    model=model,
    tools=[get_user_info, save_user_info],
    store=store,
    #state存储结构
    state_schema=CustomState,
    system_prompt="用户提及个人信息时，可以使用工具保存个人信息到长期记忆，如果用户询问个人信息也可以调用工具获取"

)
print("=" * 30, '-> 第一个会话（线程） <-', "=" * 30)
response1 = agent.invoke({
    "messages": [HumanMessage("你好，很高兴认识你，我是小花")],
    "user_id": "user-1"
})
for msg in response1["messages"]:
    msg.pretty_print()
print("=" * 30, '-> 第二个会话（线程） <-', "=" * 30)
response2 = agent.invoke({
    "messages": [HumanMessage("我是谁")],
    "user_id": "user-1"
})
for msg in response2["messages"]:
    msg.pretty_print()