from aiohttp import web

app = web.Application()

async def hello(request: web.Request):
    response = web.json_response({"hello": "world"})
    return response

app.add_routes([
    web.post('/hello/world', hello)
])

web.run_app(app)
