#推荐from_messages()
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.chat_models import init_chat_model
from openai.resources.skills import content

model = init_chat_model(
    model="qwen3.6:27b",          # 只写模型名，与你在终端用 ollama run 的名字一致
    model_provider="ollama",
    base_url="http://10.20.62.52:11434"
)
#1元组列表
chat_promt_template=ChatPromptTemplate.from_messages([
    ("system","你是一只可爱的{character}"),
    ("human","今天怎么样？"),
    ("ai","很不错呢"),
    ("human","{user_input}")
])

#2字符串
chat_promt_template2=ChatPromptTemplate.from_messages([
    "你好，我是{name}" #会理解为用户消息
])

#3字典列表
chat_promt_template2=ChatPromptTemplate.from_messages([
    {"role":"human","content": "我是{name}"}
])

#4消息对象列表
chat_promt_template2=ChatPromptTemplate.from_messages([
    HumanMessage(content="我是{name}"), #此处变量无效
])

#5:BaseMessagePromptTemplate 支持变量
systemtemplate = SystemMessagePromptTemplate.from_template("你是一只可爱的小猫")
humantemplate = HumanMessagePromptTemplate.from_template("我是{name}")
chat_promt_template3=ChatPromptTemplate.from_messages([
    systemtemplate,
    humantemplate
])

#6:ChatPromptTemplate
inner_chat1=ChatPromptTemplate.from_messages([
    ("system","你是一只可爱的{character}")])
inner_chat2=ChatPromptTemplate.from_messages([
    ("human", "今天怎么样？")
])
chat_promt_template4=ChatPromptTemplate.from_messages([
    inner_chat1,
    inner_chat2
])
#以上可以混合使用

#invoke() 入参：字典列表 返回值类型：ChatPromtValue
result=chat_promt_template.invoke({"character":"小猫","user_input":"吃了吗？"})
#format 参数类型：变量值 返回类型：字符串
result2=chat_promt_template.format(character="小猫",user_input="吃了吗？")
#format_messages 参数类型：变量值 返回类型：消息列表
result3=chat_promt_template.format_messages(character="小猫",user_input="吃了吗？")
response = model.invoke(result)
print(response)
