from typing import Any

from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import before_model, after_model, before_agent, after_agent, AgentMiddleware
from langchain_core.messages import HumanMessage
from langgraph.runtime import Runtime
from model.ollamaInit import model2,model

#基于装饰器的编写
@before_model
def before_model_middleware(state:AgentState,runtime:Runtime) ->dict[str,Any]| None:
    state['messages'][-1].content+="------->before_model<--------"
    return None
@after_model
def after_model_middleware(state:AgentState,runtime:Runtime) ->dict[str,Any]| None:
    state['messages'][-1].content+="------->after_model<--------"
    return None
@before_agent
def before_agent_middleware(state:AgentState,runtime:Runtime) ->dict[str,Any]| None:
    state['messages'][-1].content+="------->before_agent<--------"
    return None
@after_agent
def after_agent_middleware(state:AgentState,runtime:Runtime) ->dict[str,Any]| None:
    state['messages'][-1].content+="------->after_agent<--------"
    return None

#基于类定义
class MyMiddleware(AgentMiddleware):
    def before_model(self,state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        state['messages'][-1].content += "------->before_model<--------"
        return None
    def after_model(self,state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        state['messages'][-1].content += "------->after_model<--------"
        return None
    def before_agent(self,state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        state['messages'][-1].content += "------->before_agent<--------"
        return None
    def after_agent(self,state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        state['messages'][-1].content += "------->after_agent<--------"
        return None
my_middleware = MyMiddleware()
agent=create_agent(
    model=model,
    middleware=[my_middleware],
    # middleware=[
    #     before_model_middleware,
    #     after_model_middleware,
    #     before_agent_middleware,
    #     after_agent_middleware,],
)
response=agent.invoke({
    "messages":[HumanMessage("你好")]
})
for msg in response["messages"]:
    msg.pretty_print()