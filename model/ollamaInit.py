from langchain.chat_models import init_chat_model
from langchain_ollama import OllamaEmbeddings

model = init_chat_model(
    model="qwen3.6:27b",
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
model2=init_chat_model(
    model="batiai/qwen3.6-27b:iq4 ",
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
embedding_model = OllamaEmbeddings(
    model="qwen3-embedding:8b ",
    base_url="http://10.20.62.52:11434"
)
# print((model2.invoke("你好")))