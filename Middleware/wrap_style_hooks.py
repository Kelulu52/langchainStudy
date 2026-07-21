from typing import Callable, Any

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse, AgentMiddleware, wrap_tool_call
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command

from model.ollamaInit import model2,model
@tool
def get_weather(city: str, is_forcast: bool) -> str:
    """
    获取当日特定城市的天气

    Args:
    city: 城市名称
    is_forcast: 是否包含明天的天气预报
    """
    res = f"{city}今天天气不错"
    if is_forcast:
        res += "\n明天天气也很好"
    return res
#基于类的实现
class wrapModelCallMiddleware(AgentMiddleware):
    def wrap_model_call(
            self,
            request: ModelRequest,
            handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse | None:
        request.messages[-1].content += " -----> wrap_model_call_before <----- "

        response = handler(request)
        response.result[0].content += " -> wrap_model_call_after <- "

        return response

class wrapToolCallMiddleware(AgentMiddleware):
    def wrap_tool_call(
            self,
            request: ToolCallRequest,
            handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]]
    ) -> ToolMessage | Command[Any]:
        result = handler(request)
        print(f"原始参数：{request.tool_call['args']}")
        print(f"原始参数调用结果： {result}")

        request.tool_call["args"]["is_forcast"] = True
        result = handler(request)

        print(f"更新后的参数：{request.tool_call['args']}")
        print(f"更新参数调用结果： {result}")
        return result
#基于装饰器
@wrap_model_call
def wrap_model_call_middleware(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse | None:
    request.messages[-1].content += " -----> wrap_model_call_before <----- "
    # 将修改后的请求传递给 handler，真正去调用大模型（或者流转到下一个拦截器）
    response = handler(request)
    # 大模型返回响应后，在将响应交付给 Agent 状态机之前，对其内容进行直接篡改
    # `response.result` 是一个消息列表，修改其第一条返回消息的内容
    # 典型应用：做底层的文本敏感词过滤、输出格式强行格式化、或是统一添加某些后处理标记。
    response.result[0].content += " -> wrap_model_call_after <- "
    # 将修改完的响应体返回，继续维持 Agent 生命周期流转
    return response
@wrap_tool_call
def wrap_tool_call_middleware(
        request:ToolCallRequest,
        handler:Callable[[ToolCallRequest],ToolMessage | Command[Any]]
) -> ToolMessage | Command[Any]:
    result = handler(request)
    print(f"原始参数：{request.tool_call['args']}")
    print(f"原始参数调用结果： {result}")

    request.tool_call["args"]["is_forcast"] = True
    result=handler(request)

    print(f"更新后的参数：{request.tool_call['args']}")
    print(f"更新参数调用结果： {result}")
    return result
agent=create_agent(
    model=model,
    tools=[get_weather],
    # middleware=[wrap_model_call_middleware]
    # middleware=[wrapModelCallMiddleware()]
    # middleware=[wrap_tool_call_middleware]
    middleware=[wrapToolCallMiddleware()]
)
response=agent.invoke(
    {
        # "messages":[HumanMessage("nihao")]
        "messages":[HumanMessage("帮我查一下今天北京天气怎么样？")]
    }
)
for msg in response["messages"]:
    msg.pretty_print()