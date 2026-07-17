from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy, ToolStrategy, AutoStrategy, \
    MultipleStructuredOutputsError, StructuredOutputValidationError
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from rich import print as rprint
load_dotenv()

def custom_error_handler(error:Exception) -> str :
    """自定义异常处理器"""
    error_str=str(error)
    print(f"捕获异常错误类型为:{type(error).__name__}")
    print(f"错误详情{error_str}")
    if isinstance(error, MultipleStructuredOutputsError):
        return "检测到多个响应，请选择最相关的一个方案"
    elif isinstance(error, StructuredOutputValidationError):
        return "数据格式有误，请检查字段"
    else:
        return f"Error:{error_str}"


model = init_chat_model(
    model="qwen3.6:27b",          # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)

class contractInfo(BaseModel):
    """用户联系方式"""
    name: str=Field(description="用户姓名")
    email: str = Field(description="用户邮箱")
    phone: str = Field(description="用户电话")
agent=create_agent(
    model=model,
    response_format=ToolStrategy(
        contractInfo,
        tool_message_content="格式化完成",
#handle_errors异常处理 True为默认捕获所有异常 False不捕获
        # handle_errors=True,
        # 可自定义字符串返回
        # handle_errors="请检查输入数据"
        #指定特定类型异常
        # handle_errors=(MultipleStructuredOutputsError,StructuredOutputValidationError)
        #自定义异常处理
        handle_errors=custom_error_handler
        )
)

response=agent.invoke({
    "messages":[
        HumanMessage("请从以下文本提取用户信息，小明邮箱为xiaoming@king.com，电话为12345678")
    ]
})

rprint(response)