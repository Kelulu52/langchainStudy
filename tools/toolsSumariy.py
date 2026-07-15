#工具的调用方式
from typing import Literal

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.utils.function_calling import convert_to_openai_tool
from pydantic import BaseModel, Field

model = init_chat_model(
    model="qwen3.6:27b",          # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
#pydantic方式
#另外一个方式是json schema
class WeatherInput(BaseModel):
    city: str=Field(
        description="具体城市",
        default="上海",
    )
    #限定取值 enum
    unit:Literal["摄氏度","华氏度"]
#推荐该方式定义tool
#必须提供description
#name_or_callable起别名
@tool(name_or_callable="getWeather")
def getweather(city:str)->str:
    """获取指定城市的天气信息，返回天气状况和温度。"""
    return city+"晴天 22度"
#与上面等价 可同时出现 以注释中的为主
#@tool(parse_docstring=True) 可以将description中的参数识别，不加则识别会出错
#加上后docstring不合法会报错
@tool(description="获取指定城市的天气信息，返回天气状况和温度。")
def getweather(city:str)->str:
    return city+"晴天 22度"
#不使用@tool定义工具 规范写法
#describe里声明变量则函数定义要加类型city:str
#可加默认值，但后续结果不包含requires
def getweather2(city:str)->str:
    """
    获取指定城市的天气信息，返回天气状况和温度。

    Args:
        city:具体城市

    Returns:
        返回城市天气
    """
    return city+"晴天 22度"


#利用args_schema进行参数描述
@tool(args_schema=WeatherInput)
def get_weather(city:str)->str:
    """
    获取城市天气
    """
    return city+"天气晴朗"

#直接调用
#getweather.invoke({"city","上海"})

#模型调用
model_bind_tools = model.bind_tools([getweather])
#model.bind_tools执行后把函数转为openai tools
#底层实现 convert_to_openai_tool(getweather2())
model_bind_tools = model.bind_tools([getweather2])
messages=[HumanMessage("上海天气如何")]
response= model_bind_tools.invoke(messages)
messages.append(response)

if response.tool_calls:
    print("AI调用工具",response.tool_calls)
else:
    print("AI直接回答",response.content)