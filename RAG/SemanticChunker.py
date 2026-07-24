#语义分块
from model.ollamaInit import embedding_model
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.embeddings import init_embeddings
import os
from dotenv import load_dotenv
load_dotenv(override=True)
# 加载文本
with open("../asset/load/09-ai1.txt", encoding="utf-8") as f:
    state_of_the_union = f.read()  #返回字符串
# 获取嵌入模型
# embedding_model = OpenAIEmbeddings(
#     model="BAAI/bge-m3",  # 付费模型 ID： Pro/BAAI/bge-m3
#     base_url=os.getenv("SILICONFLOW_BASE_URL"),
#     api_key=os.getenv("SILICONFLOW_API_KEY"),
#     dimensions=1024
# )

# 获取切割器
text_splitter = SemanticChunker(
    embeddings=embedding_model,
    breakpoint_threshold_type="percentile",  # 断点阈值类型：字面值["百分位数", "标准差", "四分位距", "梯度"] 选其一
    breakpoint_threshold_amount=65.0,  # 断点阈值数量 (极低阈值 → 高分割敏感度)
    sentence_split_regex=r"(?<=[。？！])\s+"  # 句子切分正则:遇到中文的句号、感叹号、问号（。？！）且后面带有空格时，先将其切分为独立的“句子”。
)
# 切分文档
docs = text_splitter.create_documents(texts = [state_of_the_union])
print(len(docs))
for doc in docs:
    print(f"🔍 文档: {doc}")