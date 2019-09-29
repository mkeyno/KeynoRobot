#!/usr/bin/env python3
import logging,os,asyncio,cv2,aiojobs,aiofiles,json, threading,dotenv,argparse,aiohttp,aiohttp_session ,time,serial_asyncio
 
from aiohttp         import web, MultipartWriter
from queue           import Queue
from aiohttp.web     import middleware
from objbrowser      import browse
from aiojobs.aiohttp import setup, spawn
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor

# logging.basicConfig(format="[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
# logger = logging.getLogger('async')
# logger.setLevel(logging.DEBUG)

logging.basicConfig(filename="firefly.log",filemode='w',level=logging.DEBUG)
#logging.basicConfig(level=getattr(logging, args.log))
INDEX_File=os.path.join(os.path.dirname(__file__), 'index.html'); logging.debug(INDEX_File)
LOGIN_File=os.path.join(os.path.dirname(__file__), 'login.html'); logging.debug(LOGIN_File)
STATIC_DIR=os.path.join(os.path.dirname(__file__), 'static');logging.debug(STATIC_DIR)

PORT='COM3'
GlobalAPP=_writer=None

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

class VideoCaptureThreading:
    def __init__(self, src=0, width=640, height=480):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def set(self, var1, var2):
        self.cap.set(var1, var2)

    def start(self):
        if self.started:
            print('[!] Threaded video capturing has already been started.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()

class VideoCamera(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        """""";        logging.basicConfig(level=logging.INFO,format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
        self._raw_channel = Queue()
        self.video = cv2.VideoCapture(0);logging.debug("start camera");print("start camera")
        self.encode_param = (int(cv2.IMWRITE_JPEG_QUALITY), 90)

    def __del__(self):
        self.video.release();print("video.release")

    def delete(self):
        self.video.release();print("video.release")
 
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        try:
            ret, jpeg = cv2.imencode('.jpg', image)
        except Exception as e:
            logging.debug('Exception encoding image ' + str(e))
            return None
        #self._raw_channel.put(jpeg)
        return jpeg.tobytes()
    
@middleware
async def authorize(request, handler):
	print("Do Auchetication=");
	logging.debug("Do Auchetication=",request.path.startswith('/login')) #False
	session = await aiohttp_session.get_session(request)
	logging.debug("Dsession uid=",session.get('uid'))
	if (not session.get('uid')) and (not request.path.startswith('/login')):
		url = request.app.router['login'].url_for()
		log.debug('redirecting to {}'.format(str(url)))
		raise web.HTTPFound(url)
	response = await handler(request)
	return response
	
def redirect(request, router_name):
	print("redirect");
	url = request.app.router[router_name].url_for()
	logging.debug("redirect url =",url) #False
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
        print('Total clients: ' , self.ws_list, str(len(self.ws_list)))
		#Total clients:{<__main__.WSClient object at 0xF28>, <__main__.WSClient object at 0x630>, <__main__.WSClient object at 0xD58F6D8>} 3
        for c in self.ws_list:
            print( c.ws,c.id )
			#<WebSocketResponse Switching Protocols GET /ws > 1
			#<WebSocketResponse Switching Protocols GET /ws > 0
			#<WebSocketResponse Switching Protocols GET /ws > 2
        await self._send_user_list()
		#loop---------
        async for msg in ws:  
          if msg.type == aiohttp.WSMsgType.TEXT:
              Income=msg.data;
              parsing(Income) #message = msg.json()
              await ws.send_str("got your message website")
		#---------loop
        self.ws_list.remove(client)
        print("Removing... " + str(len(self.ws_list)))
        return ws

    async def _send_user_list(self):
        token = [c.id for c in self.ws_list if c.id]
        for c in self.ws_list:
            await c.ws.send_str('LIST*{}'.format(token));print('we send LIST*{}'.format(token) )#LIST*[4, 2, 3, 1]
        return

async def uploadFile(request):
    print("uploadFile");
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
	print("mjpeg_handler=",request.url);
	#browse(locals(), 'locals()')
	#param1=request.get('client');
	com = request.rel_url.query['com'];  print("com=",com)
	if com=='start':
		# param2 = request.rel_url.query['age']
		# result = "name: {}, age: {}".format(param1, param2)
		
		boundary = "boundarydonotcross";
		responseImage = web.StreamResponse(status=200, reason='OK', headers={'Content-Type': 'multipart/x-mixed-replace; ''boundary=--%s' % boundary,})
		#responseImage.content_type = 'multipart/x-mixed-replace;boundary=ffserver'
		await responseImage.prepare(request) #Send HTTP header. You should not change any header data after calling this method.
		VC = cv2.VideoCapture(0);
		request.app["camera"]=VC
		encode_param = (int(cv2.IMWRITE_JPEG_QUALITY), 90)
		request.app["streaming"].add(responseImage)
		while True:
			try:
				_, frame = VC.read(); #await
				if frame is None:
					  break
				with MultipartWriter('image/jpeg', boundary=boundary) as mpwriter:
					result, encimg = cv2.imencode('.jpg', frame, encode_param)
					data = encimg.tostring()
					mpwriter.append(data, {'Content-Type': 'image/jpeg'})
					await mpwriter.write(responseImage, close_boundary=False);print("next frame");
				await asyncio.sleep(0.010)#await responseImage.drain()
				
			except asyncio.CancelledError as e:
				request.app["streaming"].remove(responseImage);request.app["camera"].remove(VC)
				print("Exit camera mjpeg_handler");
				VC.shutdown();
		return responseImage
	else :
		print("streaming_clear",request.app["camera"]);
		if request.app["camera"] is not None:
			request.app["camera"].release();
		return web.Response();#return HTTPNotFound(text='No file found')
		#await shut_down(request)

# async def startcamera(request):
	# scheduler = await aiojobs.create_scheduler()
	# await scheduler.spawn(mjpeg_handler(request))
	
async def stopcamera(request):
	print("stocamera")
	camera=request.app['camera']
	await camera.delete()
	return response
	

def parsing(data):
	print("parsing websocket data=",data);#data= <WebSocketResponse Switching Protocols GET /ws >
	#await GlobalWS.send_str("AKA")
	
async def websocket_handler(request):


	global _writer
	#logging.debug("this is another one= ",request.app["GlobalWS"])
	if request.app["GlobalWS"] != None:
		print("             return, this is more than one  client:{} ".format(request.app["GlobalWS"]))
		return
	print('--------------------Websocket connection starting>>>>>>>>>>>>>>>>>>>')
	

	ws = web.WebSocketResponse()
	await ws.prepare(request)
	request.app["GlobalWS"]=1000
	logging.debug('------- -----Websocket connection ready------- -----')
	request.app["websockets"].add(ws)
	try:		
		async for msg in ws:
			# this remain live
			if msg.type == aiohttp.WSMsgType.TEXT:
				Income=msg.data;
				if(_writer):
					_writer.write(Income)
				print(Income)
		#check serial
	#request.app["GlobalWS"]=None;#.remove(ws) 
	finally:
		request.app['websockets'].discard(ws)
	return ws
	
async def websockets_clear(app):
	print("websockets_clear");
	for ws in app['websockets']:
		await ws.close()
	app['websockets'].clear()
	app['streaming'].clear();app["camera"].clear();print("streaming_clear done");

async def index(request):
    logging.debug("index simple handler")
    return web.Response(text='<div><img src="/imageH"  /></div><p> video </p><div><img src="/imageV"  /></div>', content_type='text/html')

async def handle_index_page(request):
	
	global IsAucheticated
	print(">>>>>>....IsAucheticated = ?",IsAucheticated)
	if not IsAucheticated:
		return await handle_login_page(request)
	print("handle_index_page");
	request.app["GlobalWS"] = None
	if VERBOSE_DEBUG:
		 str="index_page method={},host={},path={},headers={},transport={},cookies={}".format(request.method,request.host,request.path,request.headers,request.transport,request.cookies,)
		 logging.debug(str);print(str)#clientIP = request.headers['X-Forwarded-For']  #password = None " url=",request.app.router['login'].url_for());#  logging.debug(request.headers)  
	async with aiofiles.open(INDEX_File, mode='r') as index_file:
		index_contents = await index_file.read()
	return web.Response(text=index_contents, content_type='text/html')

async def handle_login_page(request):
    #print("handle_login_page=",request.url_for());
    if VERBOSE_DEBUG:
         str="login_page method={},host={},path={},headers={},transport={},cookies={}".format(request.method,request.host,request.path,request.headers,request.transport,request.cookies,)
         logging.debug(str);print(str)
    async with aiofiles.open(LOGIN_File, mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')
async def handle_authenticate(request):
    print("handle_authenticate");
    global IsAucheticated
    if VERBOSE_DEBUG:
         str="authenticate method={},host={},path={},headers={},transport={},cookies={}".format(request.method,request.host,request.path,request.headers,request.transport,request.cookies,)
         logging.debug(str);print(str)
    data=await request.post() #<MultiDictProxy('uname': 'xxx', 'psw': 'c', 'remember': 'on')>
    #user=data.get('uname');password=data.get('psw')
    user = data['uname'];  password = data['psw']
    print("username =",user," password =",password ) 
    if user=="admin" and password=="admin":
       IsAucheticated = True
       logging.debug("login successful");print("login successful")       
       return await handle_index_page(request)
    else :
       logging.debug("login failed");print("login failed")
       return await handle_login_page(request)
    # for key,val in data.items():
       # logging.debug(key, "=>", val)
    #browse(locals(), 'locals()')



async def serialRead(f):
	print("send serialRead")
	while True:
		print("sending......")
		await send_ws("helo web site ")
		await asyncio.sleep(1/f);

async def SerialReader(loop):
		reader,writer = await serial_asyncio.open_serial_connection(url='COM3', baudrate=115200,loop=loop)
		while True:
			line = await reader.readline()
			line = line.decode("utf-8").strip()
			print(line)
			for x in GlobalAPP['websockets']:                
				await x.send_str(line)
				
async def setup_server(loop, address, port):
	global GlobalAPP
	GlobalAPP=app = web.Application(loop=loop)
	app.router.add_route('GET', "/login", handle_login_page) #login?uname=asd&psw=asd&remember=on 
	app.router.add_route('POST', "/", handle_authenticate)
	app.router.add_route('GET', "/", handle_index_page)
	app.router.add_static('/static/', path=STATIC_DIR, name='static')
	app.router.add_route('GET', "/image", mjpeg_handler)
	app.router.add_route('GET', "/stopcamera", stopcamera)
	#wshandler = WSHandler()
	#app.router.add_get('/ws', wshandler.ws_handler)
	app.router.add_route('GET', '/ws', websocket_handler)
	app["GlobalWS"] = None
	app['websockets'] = set()
	app['psw'] = 'admin';app['uname'] = 'admin'
	app.on_shutdown.append(websockets_clear)
	app["threads"] = threading.Event()
	app["arg"] = get_args()
	# app.middlewares.append(authorize)
	#logging.debug(app.router['login'].url_for())
	#aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(STATIC_DIR))
	
	# for name, resource in app.router.named_resources().items():
	# logging.debug("Name of resource:",name,"R=", resource)
 
	return await loop.create_server(app.make_handler(), address, port)

def server_begin():
	ip='0.0.0.0';port=8080
	loop = asyncio.new_event_loop();print("server_begin",loop)	#get_event_loop get_running_loop
	asyncio.set_event_loop(loop)
	asyncio.run_coroutine_threadsafe(setup_server(loop, ip,port ), loop)
	#asyncio.run_coroutine_threadsafe(SerialReader(loop) , loop)
	print("Server ready!",ip,port)
	logging.debug("Server ready!");print("Server ready!",ip,port)
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		logging.debug("Shutting Down!");print("Shutting Down!")
		loop.close()

def setup_serial():
	loop = asyncio.new_event_loop();print("setup_serial",loop)	#get_event_loop get_running_loop
	asyncio.set_event_loop(loop)
	loop.run_until_complete(SerialReader(loop))
	loop.run_forever() 


if __name__ == '__main__':

	main_threads =    threading.Thread(target = server_begin )
	serial_threads =  threading.Thread(target = setup_serial )
	main_threads.start() ;	serial_threads.start() ;
	main_threads.join() ;serial_threads.join()  
	
	
"""
Calling a coroutine function   returns a coroutine object.
To execute a coroutine object,  use   await in front of it, or                                   await coroObj                             await asyncio.sleep(10)
                                      schedule it with ensure_future() or                                             asyncio.ensure_future(coroObj),asyncio.ensure_future(coro_function("example.com"))
									  create_task()                               asyncio.get_event_loop().create_task(coro_function("example.com"))

future  is callable coroObj                                                       future = loop.create_future(), future.add_done_callback(fn)
																				  future = loop.create_task(coroutine)
																				  future = asyncio.ensure_future(coroutine[, loop=loop])
																				  
use an event loop in the main thread													loop = asyncio.get_event_loop()	
run an event loop in another thread						  							loop = asyncio.new_event_loop()    asyncio.set_event_loop(loop)


loop.run_until_complete(<future or coroutine>).
loop.run_until_complete(asyncio.wait([      ]))
loop.run_until_complete(asyncio.gather(                                                                ))
loop.run_until_complete(asyncio.gather(helloworld(), asyncio.sleep(2)))                run a co-routine repeatedly for 2 seconds

to add a function to an already running event loop       asyncio.ensure_future(my_coro())

async def corotinglist():
    await asyncio.gather( coro2(), coro2() )

loop = asyncio.get_event_loop()
loop.run_until_complete(corotinglist())
"""