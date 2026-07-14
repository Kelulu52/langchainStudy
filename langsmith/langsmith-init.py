from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
load_dotenv(override=True)
model = init_chat_model(
    model="qwen3.6:27b",          # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
print((model.invoke("你是谁")))