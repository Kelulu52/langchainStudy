from langgraph.store.memory import InMemoryStore

store=InMemoryStore()
namespace=("users",)
user_id="user-1"
user_name="小红"
#每次put都会创建一个新的item对象无论namespace, user_id是否相同
store.put(namespace, user_id,{"name":user_name})
item=store.get(namespace,user_id)
print(item)