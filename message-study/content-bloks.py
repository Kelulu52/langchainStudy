import base64
import io
from PIL import Image
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

model = init_chat_model(
    model="qwen3.6:27b",          # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)

#多模态数据，使用字典列表

def encode_image(image_path, max_size=(1024, 1024), quality=80):
    img = Image.open(image_path)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{img_base64}"
#content_blocks
def encode_image2(image_path, max_size=(1024, 1024), quality=80):
    img = Image.open(image_path)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_base64
image_path = "jpgtest.jpg"
base64_image = encode_image(image_path)
#content_blocks
base64_image2=encode_image2(image_path)

response = model.invoke(
    [HumanMessage(
        # content=[
        #     {"type": "text", "text": "这张图里有什么？"},
        #     {"type": "image_url", "image_url": base64_image}
        # ]
        content_blocks=[
            {"type": "text", "text": "这张图里有什么？"},
            {
                "type": "image",
                "base64": base64_image2,
                "mime_type": "image/jpeg"
            }
        ]
    )]
)
print(response.content)