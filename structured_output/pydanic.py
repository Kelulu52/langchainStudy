from enum import Enum
from typing import Optional, Literal, List

from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

model = init_chat_model(
    model="qwen3.6:27b",          # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
#枚举类型
class Priority(str, Enum):
    LOW = "LOW"
    HIGH = "HIGH"
class Adress(BaseModel):
    city: str=Field(description="城市")
    district: str=Field(description="区")
class Person(BaseModel):
    """人物信息"""
    name: str=Field(description="名字",min_length=3,max_length=5) #限制条件
    #限制条件 最好搭配 try except 使用 不同平台效果不同
    age: int=Field(20,description="年龄",le=150)
    #可选字段
    #默认值每个供应商支持不一样 ollama会直接导致判断失误
    # age: Optional[int]=Field(description="年龄")
    occupation: str=Field(description="职业")
    salary:Priority=Field(description="薪水")
    #嵌套结构 层级<=3
    address:Adress=Field(description="住址")
    #或者下面的方式
    # salary:Literal["低","中","高"]=Field(description="薪水")
#列表
class PersonList(BaseModel):
    people: List[Person]
#结构化输出
output = model.with_structured_output(Person)
result=output.invoke("小明是一个30岁的高薪后端开发工程师")
print(result)
