from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from rich import print as rprint
from model.ollamaInit import model2,model
@tool
def get_weather(city: str, is_forcast: bool = False) -> str:
    """
    查询指定城市天气
    Args:
    city: 城市名称
    is_forcast: 是否包含明日天气预报？
    """
    res = f"{city}今天天气不错"
    if is_forcast:
        res += "\n明天下雨"
    return res
@tool
def get_news() -> str:
    """
    查询当日新闻
    """
    return "中方三艘油轮通过霍尔木兹海峡"
@tool
def read_email_tool(email_id: str) -> str:
    """通过邮件ID读取内容的伪函数"""
    return f"邮件ID：{email_id}\n是空的"
@tool
def send_email_tool(recipient: str, subject: str, body: str) -> str:
    """发送邮件伪函数"""
    print(">>> 真的执行发送邮件工具了")
    return f"发送给 {recipient} 的邮件标题是：{subject}，内容：{body}"
# ）在工具调用前中断Agent运行，等
# 待用户对工具调用请求决策。可选的决策有：
# approve（同意执行） 、
# edit（编辑调用配置后执行）、
# reject（拒绝执行） 。
agent=create_agent(
    model=model,
    tools=[get_weather, get_news,read_email_tool,send_email_tool],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                # True表示所有决策(approve, edit, reject) 都可以选择
                "get_weather": True,
                "get_news": True,
                #False表示不中断，即无需审批即可执行。
                "read_email_tool": False,
                "send_email_tool": {
                    "allowed_decisions":["approve","reject"],
                    "description":"发送邮件中断。。。"
                }
            },
            description_prefix="中断！",
        ),
    ]
)
weather_decision={
    "type":"edit",
    "edited_action":{
        "name":"get_weather",
        "args":{"city":"上海","is_forcast":True},
    }
}
news_decision={
    "type":"approve"
}
send_email_decision={
    "type":"approve"
}
decisions={
    "decisions":[]
}
config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
    {
        "messages": [
            HumanMessage(content="请帮我查询今天北京的天气"
                                 "查询今日新闻"
                                 "查看ID为 'sk2131421' 的邮件内容，"
                                 "向15641685664@qq.com发送邮件，标题是'哈哈哈'，内容是：'你好啊'"
                                 "同时做这四件事")]
    },
    config=config,
)
# rprint(response)
interrupts=response.get("__interrupt__",[])
action_requests=interrupts[0].value["action_requests"]
for action in action_requests:
    if action["name"]=="get_weather":
        decisions["decisions"].append(weather_decision)
    if action["name"] == "get_news":
        decisions["decisions"].append(news_decision)
    if action["name"] == "send_email_tool":
        decisions["decisions"].append(send_email_decision)
if interrupts:
    resume_response=agent.invoke(
        Command(resume=decisions),
        config=config,
    )
    for msg in resume_response["messages"]:
        msg.pretty_print()