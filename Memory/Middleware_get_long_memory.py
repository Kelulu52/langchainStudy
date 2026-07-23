
from typing import Any, Callable

from langchain.agents.middleware import ModelRequest, ModelResponse
from langchain.agents.middleware.types import ResponseT, ExtendedModelResponse
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from langgraph.types import StateT, Command
from langgraph.typing import ContextT
# Node-style hooks中访问
#通过runtime.store在中间件中访问长期记忆。
def before_model(self, state: StateT, runtime: Runtime[ContextT]) -> dict[str, Any] | None:

# Wrap-style hooks中访问
#以通过request.runtime.store访问长期记忆。
def wrap_model_call(
        self,
        request: ModelRequest[ContextT],
        handler: Callable[[ModelRequest[ContextT]], ModelResponse[ResponseT]],
) -> ModelResponse[ResponseT] | AIMessage | ExtendedModelResponse[ResponseT]:

#wrap_tool_call
#通过request.runtime.store 访问长期记忆。
def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]],
) -> ToolMessage | Command[Any]: