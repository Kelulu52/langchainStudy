from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

model = init_chat_model(
    model="qwen3.6:27b",          # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
class Movie(BaseModel):
    """电影信息"""
    title: str= Field(description="电影标题")
    year: int= Field(description="电影上映年份")
    director: str= Field(description="导演")
    rating: float= Field(description="电影评分（10分满分）")

#include_raw=True让输出结果包含原始的AImessage
#新版方式 老版为链式方式
with_structured_output= model.with_structured_output(Movie,include_raw=True)
response=with_structured_output.invoke("帮我介绍一下《星际穿越》")
print(response)
