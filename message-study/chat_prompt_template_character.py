#高级特性
#partial()填充重复值
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

template=ChatPromptTemplate.from_messages([
    ("system","你是{role},目标用户是{audience}"),
    ("human","{task}")
])
#指定不同场景
final_template=template.partial(role="导游",audience="游客")
final_template2=template.partial(role="老师",audience="学生")
result=final_template.invoke({"task":"介绍一下故宫"})
#print(result)

#placeholder占位符
template2=ChatPromptTemplate.from_messages([
    ("system","你是AI助手"),
    ("placeholder","{conversation}")
])

#MessagesPlaceholder占位 导入都一样
template3=ChatPromptTemplate.from_messages([
    ("system","你是AI助手"),
    MessagesPlaceholder(variable_name="conversation")
])
result2=template2.invoke({
    "conversation":[
        ("human","明天天气如何"),
        ("ai","明天天气晴朗")
    ]
})
print(result2)