from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_tool
from pydantic import BaseModel, Field

model = init_chat_model(
    model="qwen3.6:27b",          # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
class WeatherSchema(BaseModel):
    city: str=Field(default="上海",description="具体的城市")
    force:bool=Field(default=False,description="是否包含明天的预报")
@tool(description="获取当日城市天气以及明天的预报",args_schema=WeatherSchema)
def get_weather(city:str,force:bool):
    res=f"{city}今天天气不错"
    if force:
        res+="\n明天会下雨"
    return res

#docstring方式 严格注意规范
@tool(parse_docstring=True)
def get_weather2(city:str,force:bool):
    """
   获取当日城市天气以及明天的预报

   Args:
       city:具体的城市
       force:是否包含明天的预报
    """
    res=f"{city}今天天气不错"
    if force:
        res+="\n明天会下雨"
    return res
#print(convert_to_openai_tool(get_weather))
# print(convert_to_openai_tool(get_weather2))

#bind_tools有tool_choice参数
# 分别取值"auto"自主选择一个或多个  "none"不调工具  "required"必需要工具
#也可以指定工具名强制调用该工具
model_bind_tools = model.bind_tools([get_weather2])
messages=[HumanMessage("今天杭州天气怎么样？明天呢？")]
#多工具调用要在此处加while True循环 配合下面判断退出循环
response=model_bind_tools.invoke(messages)
messages.append(response)
# if not response.tool_calls:
#     print("没有工具调用，直接返回答案")
#     break;
tool_calls= response.tool_calls
for tool_call in tool_calls:
    if tool_call["name"]=="get_weather2":
        #调用工具
        tool_message=get_weather2.invoke(tool_call)
        messages.append(tool_message)

final_response = model.invoke(messages)
messages.append(final_response)
for msg in messages:
    msg.pretty_print()
