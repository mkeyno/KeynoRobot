import asyncio

import aioredis
from aiohttp import web

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %ws.exception())
    print('websocket connection closed')
    return ws


async def websocket_handler1(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    request.app['websockets'].append(ws)
    try:
        async for msg in ws:
            print(msg)
            await asyncio.sleep(1)
    finally:
        request.app['websockets'].remove(ws)
    return ws


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=999, message='Server shutdown')


async def listen_to_redis(app):
    try:
        sub = await aioredis.create_redis(('localhost', 6379), loop=app.loop)
        ch, *_ = await sub.subscribe('news')
        async for msg in ch.iter(encoding='utf-8'):
            # Forward message to all connected websockets:
            for ws in app['websockets']:
                await ws.send_str('{}: {}'.format(ch.name, msg))
            print("message in {}: {}".format(ch.name, msg))
    except asyncio.CancelledError:
        pass
    finally:
        print('Cancel Redis listener: close connection...')
        await sub.unsubscribe(ch.name)
        await sub.quit()
        print('Redis connection closed.')


async def start_background_tasks(app):
    app['redis_listener'] = app.loop.create_task(listen_to_redis(app))


async def cleanup_background_tasks(app):
    print('cleanup background tasks...')
    app['redis_listener'].cancel()
    await app['redis_listener']


def init():
    app = web.Application()
    app['websockets'] = []
    app.add_routes([web.get('/ws', websocket_handler)])
    #app.router.add_get('/news', websocket_handler) #app.router.add_get('/', index)
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    app.on_shutdown.append(on_shutdown)
    return app


def websocketmain():
    web.run_app(init())
    
if __name__ == '__main__':
    print("this start indivisuali")
    websocketmain()
