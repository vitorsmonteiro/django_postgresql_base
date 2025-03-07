from ninja import NinjaAPI

from todo.api.api_v1 import router as todo_router_v1
from todo.api.api_v2 import router as todo_router_v2

api_v1 = NinjaAPI(version="1.0.0")
api_v2 = NinjaAPI(version="2.0.0")

api_v1.add_router("/todo/v1", todo_router_v1)
api_v2.add_router("/todo/v2", todo_router_v2)
