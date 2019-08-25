#!/usr/bin/python3
print("******************************************************")
print("* This is a test script. There are many like it,     *")
print("* but this one is mine. My script is my best friend. *")
print("* It is my life. I must master it as I must master   *")
print("* my life.                                           *")
print("******************************************************")
import sys
print(sys.version)


from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name+ sys.version
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

web.run_app(app)