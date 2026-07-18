from langchain.chat_models import init_chat_model

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
# print((model2.invoke("你好")))