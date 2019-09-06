#!/usr/bin/env python3
import logging,os,asyncio,cv2,aiohttp_jinja2,jinja2,aiofiles,json, threading,dotenv,argparse,aiohttp,aiohttp_session 

from aiohttp         import web, MultipartWriter
from queue           import Queue
from aiohttp.web     import middleware
from objbrowser      import browse



logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=getattr(logging, args.log))
INDEX_File=os.path.join(os.path.dirname(__file__), 'index.html'); print(INDEX_File)
LOGIN_File=os.path.join(os.path.dirname(__file__), 'login.html'); print(LOGIN_File)
STATIC_DIR=os.path.join(os.path.dirname(__file__), 'static');print(STATIC_DIR)

GlobalWS=None
IsAucheticated = False
VERBOSE_DEBUG = False
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_DELAY = 0.01
DEFAULT_STORAGE = "./photos"
ALLOWED_LOG_LEVELS = (
    "CRITICAL",
    "FATAL",
    "ERROR",
    "WARNING",
    "WARN",
    "INFO",
    "DEBUG",
    "NOTSET",
)

def get_args():
    parser = argparse.ArgumentParser( description="Aiohttp based streaming service", )
    parser.add_argument( "-s", "--storage", help="Path to photo storage root directory",           required=False, type=str,                             default=os.getenv("STORAGE"  , DEFAULT_STORAGE),)
    parser.add_argument( "-d", "--delay"  , help="Interval between sending the chunks in seconds", required=False, type=float,                           default=os.getenv("DELAY"    , DEFAULT_DELAY), )
    parser.add_argument( "-l", "--log"    , help="Loging level",                                   required=False, type=str, choices=ALLOWED_LOG_LEVELS, default=os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL), )
    args = parser.parse_args()
    return args

class VideoCamera(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        """""";        logging.basicConfig(level=logging.INFO,format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
        self._raw_channel = Queue()
        self.video = cv2.VideoCapture(0);print("start camera")
        self.encode_param = (int(cv2.IMWRITE_JPEG_QUALITY), 90)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        try:
            ret, jpeg = cv2.imencode('.jpg', image)
        except Exception as e:
            print('Exception encoding image ' + str(e))
            return None
        #self._raw_channel.put(jpeg)
        return jpeg.tobytes()
    
@middleware
async def authorize(request, handler):
	print("Do Auchetication=",request.path.startswith('/login')) #False
	session = await aiohttp_session.get_session(request)
	print("Dsession uid=",session.get('uid'))
	if (not session.get('uid')) and (not request.path.startswith('/login')):
		url = request.app.router['login'].url_for()
		log.debug('redirecting to {}'.format(str(url)))
		raise web.HTTPFound(url)
	response = await handler(request)
	return response
	
def redirect(request, router_name):
	url = request.app.router[router_name].url_for()
	print("redirect url =",url) #False
	log.debug('redirecting to {}'.format(url))
	raise web.HTTPFound(url)

'''middleware redirects to Login in case there is no 'uid' found in the request's session'''
class Login(web.View):
	async def get(self):
		session = await get_session(self.request)
		uid = 'user{0}'.format(random.randint(1, 1001))
		uids = self.request.app['uids']
		while uid in uids:
			uid = 'user{0}'.format(random.randint(1, 1001))
		uids.append(uid)
		self.request.app['uids'] = uids
		session['uid'] = uid
		log.debug(uid)
		redirect(self.request, '/')
WSID=0

class WSClient(object):
    
    def __init__(self, ws):
        global WSID
        self.id = WSID
        self.ws = ws
        WSID+=1
	
    async def send(self,msg):
         await self.ws.send_str(msg)

class WSHandler:
    def __init__(self):
        self.ws_list = set()

    async def ws_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        client = WSClient(ws)
        self.ws_list.add(client)
        print('Websocket connection ready')
        print('Total clients: ' + str(len(self.ws_list)))
        for c in self.ws_list:
            print( c.ws,c.id )
        #await self._send_user_list()
        async for msg in ws:
          if msg.type == aiohttp.WSMsgType.TEXT:
              Income=msg.data;
              parsing(Income) #message = msg.json()#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
              await ws.send_str("than yoooooooooooooou")#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        self.ws_list.remove(client)
        print("Removing... " + str(len(self.ws_list)))
        return ws

    async def _send_user_list(self):
        token = [c.id for c in self.ws_list if c.id]
        for c in self.ws_list:
            await c.ws.send_str('LIST*{}'.format(token));print('we send LIST*{}'.format(token) )
        return

async def uploadFile(request):

    reader = await request.multipart()
    # /!\ Don't forget to validate your inputs /!\
    # reader.next() will `yield` the fields of your form
    field = await reader.next()
    assert field.name == 'name'
    name = await field.read(decode=True)

    field = await reader.next()
    assert field.name == 'mp3'
    filename = field.filename
    # You cannot rely on Content-Length if transfer is chunked.
    size = 0
    with open(os.path.join('/spool/yarrr-media/mp3/', filename), 'wb') as f:
     while True:
        chunk = await field.read_chunk()  # 8192 bytes by default.
        if not chunk:
          break
        size += len(chunk)
        f.write(chunk)

    return web.Response(text='{} sized of {} successfully stored'''.format(filename, size))

async def mjpeg_handler(request):
    boundary = "boundarydonotcross";
    camera = VideoCamera()
    response = web.StreamResponse(status=200, reason='OK', headers={'Content-Type': 'multipart/x-mixed-replace; ''boundary=--%s' % boundary,})
    print("just once mjpeg_handler")
    await response.prepare(request)    
    while True:
        frame = camera.get_frame();#print("get_frame")
        if frame is None:
            camera = VideoCamera()
            frame = camera.get_frame()
        ##################   object detection  #########################
#       frame=object_detection(frame)
        ##############################################################
        with MultipartWriter('image/jpeg', boundary=boundary) as mpwriter:
            mpwriter.append(frame, {'Content-Type': 'image/jpeg'})
            await mpwriter.write(response, close_boundary=False)
        #camera.logger.info('Number of processed images in the queue: {}'.format(response))
        await response.drain()
    return response

def parsing(data):
    print(">>>>>>>",data)
	
async def websocket_handler(request):
    global GlobalWS
    print("this is another one ",GlobalWS)
    if GlobalWS != None:
        print("                      can not ")
        return
    logging.debug('Websocket connection starting')
    if VERBOSE_DEBUG:
      logging.debug(
                "method={},host={},path={},headers={},transport={},cookies={}"
                .format(
                  request.method,
                  request.host,
                  request.path,
                  request.headers,
                  request.transport,
                  request.cookies,
                ))
    #clientIP = request.headers['X-Forwarded-For']
    """
    ws_ready = ws.can_prepare(request)#checks for request data to figure out if websocket can be started on the request.
    if not ws_ready.ok:        
        return aiohttp_jinja2.render_template('index.html', request, data2html) #put data in html and send to client
"""
    #hash      = request.match_info["hash"];print("equest.match_info[hash]=",hash)
    #logging.debug("Client Request from {}".format(clientIP))  
	#if not XXXXX:
    #    raise web.HTTPNotFound(text="folder was deleted or never existed")
    GlobalWS = web.WebSocketResponse()

    await GlobalWS.prepare(request)
    request.app["websockets"].add(GlobalWS)
    #print(app["websockets"])
    logging.debug('-------------------------------Websocket connection ready-----------------------------')

    async for msg in GlobalWS:
        #logging.debug(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            Income=msg.data;
            parsing(Income) #message = msg.json()#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            await GlobalWS.send_str("than yoooooooooooooou")#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    logging.debug('Websocket connection closed')
    request.app["websockets"].remove(GlobalWS)
    GlobalWS=None
    return GlobalWS
	
async def websockets_clear(app):
    for ws in app['websockets']:
        await ws.close()
    app['websockets'].clear()

async def index(request):
    print("index simple handler")
    return web.Response(text='<div><img src="/imageH"  /></div><p> video </p><div><img src="/imageV"  /></div>', content_type='text/html')

async def handle_index_page(request):
    print("index handler",request.query.get('psw'))#  #password = None " url=",request.app.router['login'].url_for());#  print(request.headers)  
    async with aiofiles.open(INDEX_File, mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')

async def handle_login_page(request):
    print("login handler",request.app["psw"])#," url=",request.app.router['login'].url_for());#  print(request.headers)  
    async with aiofiles.open(LOGIN_File, mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')
async def handle_authenticate(request):
    #redirect(request, '/')
    data=await request.post() #<MultiDictProxy('uname': 'xxx', 'psw': 'c', 'remember': 'on')>
    #user=data.get('uname');password=data.get('psw')
    user = data['uname'];  password = data['psw']
    # for key,val in data.items():
       # print(key, "=>", val)
    print("username =",user," password =",password ) 
    #browse(locals(), 'locals()')
    return await handle_index_page(request)
	
	
async def setup_server(loop, address, port):
    app = web.Application(loop=loop)
    app.router.add_route('GET', "/login", handle_login_page) #login?uname=asd&psw=asd&remember=on 
    app.router.add_route('POST', "/authenticate", handle_authenticate)
    app.router.add_route('GET', "/", handle_index_page)
    app.router.add_static('/static/', path=STATIC_DIR, name='static')
    app.router.add_route('GET', "/imagezH", mjpeg_handler)
    app.router.add_route('GET', "/imagezV", mjpeg_handler)
    wshandler = WSHandler()
    #app.router.add_get('/ws', wshandler.ws_handler)
    app.router.add_route('GET', '/ws', websocket_handler)
    app["websockets"] = set()
    app['uids'] = [] 
    app['psw'] = 'admin';app['uname'] = 'admin'
    app.on_shutdown.append(websockets_clear)
    app["threads"] = threading.Event()
    app["arg"] = get_args()
    # app.middlewares.append(authorize)
    #print(app.router['login'].url_for())
    #aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(STATIC_DIR))
	
    # for name, resource in app.router.named_resources().items():
      # print("Name of resource:",name,"R=", resource)
    return await loop.create_server(app.make_handler(), address, port)

def server_begin():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_server(loop, '127.0.0.1', 8080))
    print("Server ready!")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Shutting Down!")
        loop.close()

if __name__ == '__main__':
    server_begin()