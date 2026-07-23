from langgraph.store.memory import InMemoryStore
from pprint import pprint
#自定义嵌入函数
def embed(text: list[str]) -> list[list[float]]:
    return [[1.0] * 6 for _ in range(len(text))]
index_config = {
    "embed": embed,
    "dims": 6, #维度
    "fields": ["$", "course"]
}
store = InMemoryStore()
store1 = InMemoryStore(
    index = index_config
)
namespace1 = ("users", "Alice", "memories")
key1 = 'preferences'
value1 = {
    "course": "计算机组成原理",
    "sports": "跑步",
    "food": "紫光园奶皮子酸奶"
}
namespace2 = ("users", "Bob", "memories")
key2 = 'preferences'
value2 = {
    "course": "数字电路与模拟电路",
    "sports": "跑步",
    "food": "奶皮子糖葫芦"
}
namespace3 = ("users", "Black", "memories")
key3 = 'preferences'
value3 = {
    "course": "数字电路与模拟电路",
    "sports": "羽毛球",
    "food": "紫光园奶皮子酸奶"
}
store.put(namespace1, key1, value1)
store.put(namespace2, key2, value2)
store.put(namespace3, key3, value3)

store1.put(namespace1, key1, value1)
store1.put(namespace2, key2, value2)
store1.put(namespace3, key3, value3)
#基于前缀搜索
for item in store.search(("users",)):
    print(item)
for item in store.search(("users","Bob")):
    print(item)
#filter对value进行条件过滤 选择包含条件的
#filter换成query 就是语义检索
for item in store.search(("users",),filter={"food": "紫光园奶皮子酸奶"}):
    print(item)
#查看嵌入向量
pprint(store1._vectors)
#通过指定namespace、key、index_config的fields中指定的字段名查看特定向量。
pprint(store1._vectors[('users', 'Alice', 'memories')]['preferences']['$'])