from aiohttp import web

from models import init_orm, close_orm

app = web.Application()

async def orm_context(app: web.Application):
    print("start")
    await init_orm()
    yield
    await close_orm()
    print("finish")

async def hello(request: web.Request):
    response = web.json_response({"hello": "world"})
    return response

app.cleanup_ctx.append(orm_context)

app.add_routes([
    web.post('/hello/world', hello)
])

web.run_app(app)
