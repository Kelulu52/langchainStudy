import re

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain_core.messages import HumanMessage

from model.ollamaInit import model
from dotenv import load_dotenv
load_dotenv(verbose=True)

 #自定义检测函数
def detect_phone_number(content: str):
    return [
        {
            "text": m.group(0), # 提取出具体匹配到的 11 位数字文本（例如 "13800138000"）
            "start": m.start(), # 这段数字在原文本中的“起始索引位置”（从 0 开始算）
            "end": m.end() # 这段数字在原文本中的“结束索引位置”
        } for m in re.finditer(r"[0-9]{11}", content)
    ]
agent=create_agent(
    model=model,
    tools=[],
    middleware=[
        #用于检测和处理对话中的个人身份信息   apply_to_input输入agent前
        #redact 将检测到的PII信息用字符串[REDACTED_[PII_TYPE]] 替换
        PIIMiddleware("email",strategy="redact",apply_to_input=True),
        #mask ：用***将PII信息的前面一部分信息遮蔽。
        PIIMiddleware("credit_card",strategy="mask",apply_to_input=True),
        #hash ：用检测到的PII信息的哈希值替代原值。
        PIIMiddleware("url",strategy="hash",apply_to_input=True),
        #block ：如果检测到PII信息，直接抛出异常。
        PIIMiddleware("ip",strategy="block",apply_to_input=True),
        PIIMiddleware("mac_address",strategy="mask",apply_to_input=True),
    ]
)
agent2 = create_agent(
    model=model,
    tools=[],
    middleware=[
        PIIMiddleware("api_key", strategy="hash", apply_to_input=True,
detector=r"sk-[a-zA-Z0-9]+"),
        PIIMiddleware("phone_number", strategy="mask", apply_to_input=True,
detector=detect_phone_number)
    ]
)
# response = agent.invoke({
#     "messages": [HumanMessage("""
#     帮我向 156168188@qq.com 发送一封邮件
#     同时查看银行卡号： 5105-1051-0510-5100 的余额
#     访问 https://localhost:12345
#     确认这是不是 MAC地址： 11-11-11-11-11-11
#     """)]
# })


response = agent2.invoke({
    "messages": [HumanMessage("""
    这是不是有效的 API_KEY： sk-awef23AFEfaafaefa
    帮我给这个号码打电话： 12345612345
    访问 https://localhost:12345   """)]
})
for msg in response["messages"]:
    msg.pretty_print()
# try:
#     response1 = agent.invoke({
#     "messages": [HumanMessage("看看这个 IP 能不能 ping 通：192.168.10.1")]
#     })
# except Exception as e:
#     print('=' * 30, '-> 抛异常 <-', '=' * 30)
#     print(f"检测到IP，抛出异常：{e}")