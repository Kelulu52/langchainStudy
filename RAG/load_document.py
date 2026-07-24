from langchain_community.document_loaders import TextLoader, CSVLoader, JSONLoader, UnstructuredWordDocumentLoader, \
    UnstructuredMarkdownLoader, DirectoryLoader, PythonLoader
from rich import print as rprint
#格式差不多
#加载文本
loader=TextLoader(
    file_path="../asset/load/01-langchain-utf-8.txt",
    encoding="utf-8"
)
loader1=TextLoader(
    file_path="../asset/load/01-langchain-gbk.txt",
    encoding="gbk"
)
loader2=CSVLoader(
    file_path="../asset/load/02-load.csv",
)
#导入word
load3=UnstructuredWordDocumentLoader(
    # 文件路径
    file_path="../asset/load/05-sgg_chat.docx",
    # 加载模式:
    #   single 返回单个Document对象
    #   elements 按标题等元素切分文档
    mode="single",
)
#导入markdown
loader = UnstructuredMarkdownLoader(
    file_path="../asset/load/06-load.md",
    # 加载模式:
    #   single 返回单个Document对象
    #   elements 按标题等元素切分文档
    mode= "single",
    # 解析策略：
    #   "fast"（快速模式），它会以最快的速度提取文本，不进行复杂的版面分析
    #   "hi_res" 高分辨率模式
    strategy="fast"
)
#加载文件夹
directory_loader = DirectoryLoader(
    path="../asset/load",
    glob="*.py", # 文件匹配模式（过滤器）。使用标准的 Unix 路径通配符。
    use_multithreading=True, # 是否启用多线程。填 True 意味着 LangChain 会同时并发读取多个文件。
    show_progress=True, # 是否显示进度条。填 True 时，控制台在加载文件时会弹出一个进度条
    loader_cls=PythonLoader # 指定底层核心加载器
)
docs = loader.load()
# json_loader=JSONLoader(
#     file_path="../asset/load/03-load.json",
#     jq_schema=".", ## 提取所有字段
#     #True为字符串
#     text_content=False #保持原始 JSON 结构，将提取的数据转换为JSON字符串存入page_content字段中
# )
# 情况2
# .messages[].content:遍历.messages[]中所有元素 从每一个元素中提取.content字段
json_loader=JSONLoader(
    file_path="../asset/load/03-load.json",
    jq_schema=".messages[].content"
)
docs = loader.load()
docs2=loader2.load()
docs3=json_loader.load()
rprint(docs3)
