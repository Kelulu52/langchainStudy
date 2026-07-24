from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

text = """
LangChain 是一个用于开发由语言模型驱动的应用程序的框架的。它提供了一套工具和抽象，使开发者
能够更容易地构建复杂的应用程序。
"""
text2= "这是一个示例文本啊。我们将使用CharacterTextSplitter将其分割成小块。分割基于字符数。"
text3="LangChain框架特性\n\n多模型集成(GPT/Claude)\n记忆管理功能\n链式调用设计。文档分析场景示例：需要处理PDF/Word等格式。"
list=["LangChain框架特性\n\n多模型集成(GPT/Claude)\n记忆管理功能\n链式调用设计。文档分析场景示例：需要处理PDF/Word等格式。"]
#导入
loader = PyPDFLoader("../asset/load/04-load.pdf")
# 加载和切割文档对象
docs = loader.load()   # 返回Document对象构成的list
# 2.打开.txt文件
with open("../asset/load/09-ai.txt", encoding="utf-8") as f:
    state_of_the_union = f.read()  #返回的是字符串
# 3.定义字符分割器
splitter = CharacterTextSplitter(
    chunk_size=50, # 每块大小
    chunk_overlap=5,# 块与块之间的重复字符数
    #length_function=len,
    separator=""   # 设置为空字符串时，表示禁用分隔符优先
)
 #3.定义分割器实例
text_splitter = CharacterTextSplitter(
    chunk_size=30,   # 每个块的最大字符数
    chunk_overlap=5, # 块之间的重叠字符数
    separator="。",  # 按句号分割优先 结果可比chunk_size大
)
#递归文本分割器
#默认情况下，它尝试进行切割的字符包括 ["\n\n", "\n", " ", ""]。
text_splitter2 = RecursiveCharacterTextSplitter(
    chunk_size=10,
    chunk_overlap=0,
    add_start_index=True,
)
# 4.分割文本
# texts = splitter.split_text(text)
# texts2=text_splitter.split_text(text2)
# paragraphs = text_splitter2.split_text(text3)
# paragraphs2 = text_splitter.create_documents(list)
# # 5.打印结果
# for i, chunk in enumerate(paragraphs):
#     print(f"块 {i+1}:长度：{len(chunk)}")
#     print(chunk)
#     print("-" * 50)
#
# for para in paragraphs:
#     print(para)
#     print('-------')


text_splitter3 = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    #自定义分隔符
    # separators=["\n\n", "\n", "。", "！", "？", "……", "，", ""],  # 添加中文标点
    #chunk_overlap=0,
    length_function=len
)

text_splitter4 = RecursiveCharacterTextSplitter(
    chunk_size=200,
    #chunk_size=120,
    chunk_overlap=0,
    # chunk_overlap=100,
    length_function=len,
    add_start_index=True,
)
# 4.分割文本
texts = text_splitter3.create_documents([state_of_the_union])

paragraphs = text_splitter4.split_documents(docs)
# 5.打印分割文本
for text in texts:
    print(f"🔥{text.page_content}")