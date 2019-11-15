#!/usr/bin/env python
#https://www.youtube.com/watch?v=8p2cH1qEBZQ
#https://www.facebook.com/hamid.mehrdad.944/posts/109903260451140
#[::-1] reverses the array
#image.shape =(h,w),(r,c)

import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
from PIL import Image
import cv2
import numpy as np
from sys import exit as exit
from matplotlib import pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import queue
import threading
import time

def SELECT_FILE(filename):
	import os
	here = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(here,filename)

values=[]
MODE=''
oldEvent=capL=capR=MiddleImg=frameL=frameR=frame_grayL=frame_grayR=None
Width=200
Height=180
CameraRecording=False
numDisparities=16; blockSize=15
MiddleSource='combineCam'
BASELINEF=13.4*6# 4.2mm, 6mm, 8mm Focal Length
H_FRAME=480
W_FRAME=640
mask_image   = np.zeros((H_FRAME,W_FRAME), np.uint8)
mask_image_s = np.zeros((Height,Width), np.uint8)
COLOR_R,COLOR_L=(255,0,0),(0,255,0)
roi_w,roi_h=70,110
ROI_L=ROI_R=template=np.zeros((roi_h,roi_w), np.uint8)
comparison_methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

def findComonImage(image,whichOne,method=0):
	global template
	if whichOne=='R':
		template=ROI_R
		#print(image.shape,template.shape,image[W_FRAME-roi_w:W_FRAME ,0:roi_h].shape)#(480, 640, 3) (110, 70, 3) 370 480
		#image[W_FRAME-roi_w:W_FRAME ,0:roi_h]=ROI_L
	else:
		template=ROI_L
		#print(image.shape,template.shape,image[W_FRAME-roi_w,W_FRAME :0,roi_h].shape)
		#image[W_FRAME-roi_w:W_FRAME ,0:roi_h]=ROI_R
	#w,h=template.shape[:,:,-1]
	cm= values['comparison_methods']
	#print(cm)
	res = cv2.matchTemplate(image,template,eval(cm))
	#threshold=.8#values['thresh_slider']
	#print(threshold)
	#loc=np.where(res >= threshold)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)# find the minimum and maximum element values and their positions
	if comparison_methods[method] in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
		top_left = min_loc
	else:
		top_left = max_loc

	bottom_right = (top_left[0] + roi_h, top_left[1] + roi_w)
	dx=int((bottom_right[0]-top_left[0])/2)
	dy=int((bottom_right[1]-top_left[1])/2)
	#print(top_left,bottom_right,dx,dy)

	font                   = cv2.FONT_HERSHEY_SIMPLEX
	bottomLeftCornerOfText = (int(W_FRAME/2),int(H_FRAME/2))
	fontScale              = 1
	fontColor              = (255,255,255)
	lineType               = 2
	matn='Distance %.3f cm'%abs(distance(W_FRAME/2,top_left[0]+dx))
	print(matn)
	cv2.putText(image,matn,bottomLeftCornerOfText,font,fontScale,fontColor,lineType)
	cv2.line(image,(int(W_FRAME/2),int(H_FRAME/2)) , (top_left[0]+dx,int(H_FRAME/2)), (0,100,200), 5)

	#for pt in zip(*loc[::-1]):
	#	return	cv2.rectangle(image,pt, (pt[0]+roi_w,pt[1]+roi_h), (0,0,255), 2)
	return 	cv2.rectangle(image,top_left, bottom_right, (0,0,255), 2)

#ROI lambda x:
def distance(px1,px2):
	return BASELINEF*2650/(int(px1-px2+.001))

def numberOfChannel(image):
	if len(image.shape)>2:
		return image.shape[-1]
	return 1
#row , column| height, width, channels = img.shape
def drawRec(image,w=roi_w,h=roi_h,color=COLOR_R,thickness=2):
	W,H=W_FRAME,H_FRAME#image.shape[0],image.shape[1]#(480,640)

	start_point,end_point=(int((W-w)/2),int((H-h)/2)),(int((W+w)/2),int((H+h)/2))
	#print(start_point,end_point)
	return cv2.rectangle(image, start_point, end_point, color, thickness)

def convert1to3channel(g_image):
	return  np.zeros( ( np.array(g_image).shape[0], np.array(g_image).shape[1], 3 ) )
	if len(g_image.shape)>2:
		print(g_image.shape[-1])
		return g_image

	img3 = np.zeros_like(g_image)
	img3[:,:,0] = g_image
	img3[:,:,1] = g_image
	img3[:,:,2] = g_image
	return img2

def start_camera():
	global capR,capL
	capL = cv2.VideoCapture(int(values['camera_left']))  
	capR = cv2.VideoCapture(int(values['camera_right']))
	CameraRecording = True
	print("camera starting")
def stop_camera():
	global capR,capL
	capL.release()
	capR.release()
	CameraRecording = False
	print("camera stoping")

def showFrams():
	global 	numDisparities,blockSize,MiddleImg,frameL,frameR,frame_grayL,frame_grayR,ROI_L,ROI_R
	ret, frameL = capL.read()
	ret2,frameR = capR.read()
	ROI_L=frameL[int((H_FRAME-roi_h)/2):int((H_FRAME+roi_h)/2)	,	int((W_FRAME-roi_w)/2):int((W_FRAME+roi_w)/2)]
	ROI_R=frameR[int((H_FRAME-roi_h)/2):int((H_FRAME+roi_h)/2)	,	int((W_FRAME-roi_w)/2):int((W_FRAME+roi_w)/2)]
	#print("raw:",frameR.shape,frameR.shape[::-1]) #                  shape(480,640,3)  CV_8UC3
	#       raw: (480, 640, 3) (3, 640, 480)
	frame_grayL =cv2.cvtColor(frameL , cv2.COLOR_BGR2GRAY)
	frame_grayR =cv2.cvtColor(frameR , cv2.COLOR_BGR2GRAY)
	#print("gray scale:",frame_grayL.shape,frame_grayL.dtype)  shape(480,640  )  CV_8UC1
	frameLsmall=drawRec(frameL,color=COLOR_L);
	frameRsmall=drawRec(frameR,color=COLOR_R);
	frameLsmall =cv2.resize(frameL ,(Width,Height))
	frameRsmall =cv2.resize(frameR ,(Width,Height))
	#LeftImgbytes =cv2.imencode('.png', frameLsmall)[1].tobytes()
	#RightImgbytes=cv2.imencode('.png', frameRsmall)[1].tobytes()

	if MiddleSource=='combineCam':
		ws=int(values['blockSize_slider'])
		if ws%2==0:
			ws=ws+1
		numDisparities=int(int(values['ndis_slider']/16)*16)
		#print(numDisparities, ws)
		stereo    = cv2.StereoBM_create(numDisparities=numDisparities, blockSize=ws)
		disparity = stereo.compute(frame_grayR,frame_grayL)# Both input images must have CV_8UC1 in function 'cv::StereoBMImpl::compute'

		mask_image[disparity > 0] = (942.8 * 140) / (0.001  * disparity[disparity > 0])
		MiddleImg=disparity#mask_image##cv2.imencode('.png', disparity)[1].tobytes();  CV_16SC1


	elif MiddleSource=='LeftCam':
		MiddleImg=frameL#frame_grayL#cv2.imencode('.png', frame_grayL)[1].tobytes()MiddleImg: (480, 640) uint8

		MiddleImg=findComonImage(MiddleImg,'R',method=0)

	elif MiddleSource=='RightCam':
		MiddleImg=frameR#frame_grayR#cv2.imencode('.png', frame_grayR)[1].tobytes()
		MiddleImg=findComonImage(MiddleImg,'L',method=0)



	cv2.line(MiddleImg,(0,int(H_FRAME/2)),(W_FRAME,int(H_FRAME/2)),(255,20,100),2)
	cv2.line(MiddleImg,(int(W_FRAME/2),0),(int(W_FRAME/2),H_FRAME),(255,20,100),2)
	#print("MiddleImg:",MiddleImg.shape,MiddleImg.dtype)
	return frameLsmall,MiddleImg,frameRsmall

def GUI_c():
	columnFlag = [
			[sg.Checkbox('Normalize',     size=(12, 1), default=True), sg.Checkbox('Verbose', size=(20, 1))],
			[sg.Checkbox('Cluster',       size=(12, 1)),               sg.Checkbox('Flush Output', size=(20, 1), default=True)],
			[sg.Checkbox('Write Results', size=(12, 1)),               sg.Checkbox('Keep Intermediate Data', size=(20, 1))],
			[sg.Checkbox('Normalize',     size=(12, 1), default=True), sg.Checkbox('Verbose', size=(20, 1))],
			[sg.Checkbox('Cluster',       size=(12, 1)),               sg.Checkbox('Flush Output', size=(20, 1), default=True)],
			[sg.Checkbox('Write Results', size=(12, 1)),               sg.Checkbox('Keep Intermediate Data', size=(20, 1))],
			]

	columnLF = [
				[sg.Radio('Cross-Entropy', 'loss', size=(12, 1)), sg.Radio('Logistic', 'loss', default=True, size=(12, 1))],
				[sg.Radio('Hinge', 'loss',         size=(12, 1)), sg.Radio('Huber', 'loss', size=(12, 1))],
				[sg.Radio('Kullerback', 'loss',    size=(12, 1)), sg.Radio('MAE(L1)', 'loss', size=(12, 1))],
				[sg.Radio('object', 'loss',       size=(12, 1)), sg.Radio('detect', 'loss', size=(12, 1), enable_events=True,key='detect')],
				]

	columnCommand = [
					[sg.Text('Passes', size=(8, 1)), sg.Spin(values=[i for i in range(1, 1000)], initial_value=20, size=(6, 1)), sg.Text('Steps', size=(8, 1), pad=((7,3))), sg.Spin(values=[i for i in range(1, 1000)], initial_value=20, size=(6, 1))],
					[sg.Text('ooa',    size=(8, 1)), sg.In(default_text='6', size=(8, 1)),                                       sg.Text('nn',    size=(8, 1)),              sg.In(default_text='10', size=(10, 1))],
					[sg.Text('q',      size=(8, 1)), sg.In(default_text='ff', size=(8, 1)),                                      sg.Text('ngram', size=(8, 1)),              sg.In(default_text='5', size=(10, 1))],
					[sg.Text('l',      size=(8, 1)), sg.In(default_text='0.4', size=(8, 1)),                                     sg.Text('Comparison',size=(8, 1)),              sg.Drop(values=('cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'), auto_size_text=True,key='comparison_methods')],
					]

	columnL=[
			  [sg.Text('Left Camera ', justification='center', font='Helvetica 12')],
			  [sg.Image(filename='',data= Image.fromarray(mask_image_s, 'P'),  key='imageL')],

			  [sg.Frame(layout=[
									[sg.Radio('Combine Cameras', "RADIO1",enable_events=True,key='combineCam', default=True)],
									[sg.Radio('Left Camera'    , "RADIO1",enable_events=True,key='LeftCam')],
									[sg.Radio('Right Camera'   , "RADIO1",enable_events=True,key='RightCam')]

					           ], title='Image Source',title_color='black', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')
			  ],
			  [sg.Image(filename='', key='ROI')]
			]
	columnM=[
			#[sg.Text('OpenCV ', size=(40, 1), justification='center', font='Helvetica 18')],
			#[sg.Text('				Main Image ', justification='center', font='Helvetica 12')],
			[sg.Image(filename='', key='output',)]
			]
	columnR=[
			[sg.Text('Right Camera ', justification='center', font='Helvetica 12')],
			[sg.Image(filename='', key='imageR')],
		    [sg.Output(size=(40,9))]
			]


	column11=[
			  [sg.Radio('None',      'Radio', True, enable_events=True,key='NONE', size=(10, 1))],
			  [sg.Radio('Num of Disparities/block Size ','Radio',enable_events=True, key='ndis'),sg.Slider((16, 160), 16, 1, enable_events=True,orientation='h',  key='ndis_slider'),sg.Slider((5, 255), 5, 5, enable_events=True,orientation='h', key='blockSize_slider')],
			  [sg.Radio('fgbfghe','Radio',               enable_events=True, key='blocnvbncvkSize') ,sg.Slider((10, 21), 10, 1, enable_events=True,orientation='h', size=(40, 15), key='bxxxSize_slider')],
			  ]
	column12=[
			[sg.Radio('canny',     'Radio', size=(10, 1),enable_events=True, key='canny')     ,sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='canny_slider_a'),sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='canny_slider_b')],
		    [sg.Radio('Cam Preset','Radio', size=(10, 1),enable_events=True, key='campreset') ,sg.Slider((0, 3), 0, 1, orientation='h',enable_events=True, size=(40, 15), key='campreset_slider')],
			[sg.Radio('Chess Corner',     'Radio', size=(10, 1),enable_events=True, key='ChessCorner'),sg.In(key='ChessNum'),sg.Slider((2, 16), 8, 1, orientation='h', size=(20, 15), key='ChesX_slider'),sg.Slider((2, 16), 6, 1, orientation='h', size=(20, 15), key='ChesY_slider')]
		]
	column21=[
		  [sg.Radio('threshold', 'Radio', size=(10, 1),enable_events=True, key='thresh')    ,sg.Slider((0, 255), 128, 1, orientation='h', size=(40, 15), key='thresh_slider')],
		  [sg.Radio('contour',   'Radio', size=(10, 1),enable_events=True, key='contour'),sg.Slider((0, 255), 128, 1, orientation='h',  size=(20, 15), key='contour_slider'),sg.Slider((0, 255), 80, 1,  orientation='h', size=(20, 15), key='base_slider')],
		  [sg.Radio('blur',      'Radio', size=(10, 1),enable_events=True, key='blur')   ,sg.Slider((1, 11),  1,   1, orientation='h', size=(40, 15), key='blur_slider')],
		  ]
	column22=[
		  [sg.Radio('hue',       'Radio', size=(10, 1),enable_events=True, key='hue')    ,sg.Slider((0, 225), 0,   1, orientation='h', size=(40, 15), key='hue_slider')],
		  [sg.Radio('line',      'Radio', size=(10, 1),enable_events=True, key='line'),   sg.Slider((0, 1000), 10, 1, orientation='h', size=(20, 15), key='linemax_slider'),sg.Slider((0, 1000), 1000, 1,  orientation='h', size=(20, 15), key='linemin_slider')],
		  [sg.Radio('enhance',   'Radio', size=(10, 1),enable_events=True, key='enhance'),sg.Slider((1, 255), 128, 1, orientation='h', size=(40, 15), key='enhance_slider')]
		  ]

	tab_ObjectDetectionSetting =[ [sg.Column(column11,),sg.Column(column12,)] ]
	tab_DepthDetectionSetting  =[ [sg.Column(column21,),sg.Column(column22,)] ]
	tab_MachineLearningSetting =[ [sg.Column(columnCommand,),sg.Column(columnFlag,),sg.Column(columnLF,)] ]
	#layout2 = [	sg.Column(column1,),sg.Column(column2)]
	# create the window and show it without the plot
	# define the window layout
	tab_Main=[
			  [sg.Column(columnL),sg.Column(columnM),sg.Column(columnR)],
			  [sg.TabGroup([ [sg.Tab('Object Detection Setting', tab_ObjectDetectionSetting),sg.Tab('Depth Detection Setting' , tab_DepthDetectionSetting),sg.Tab('Machine Learning Setting', tab_MachineLearningSetting),]], key='_TABGROUP_')]
			 ]
#-----------------------------------key='tab_left'------------------------------------------------------------------------------------			 
	column_Tab_lef_LEFT=[
						  [sg.Text('Left Camera ', justification='center', font='Helvetica 12')],
						  [sg.Image(filename='',  key='column_Tab_lef_LEFT_image')],
						 ]
	column_Tab_lef_RIGHT=[
						  [sg.Text('Left Camera ', justification='center', font='Helvetica 12')],
						  [sg.Text('Left Camera ', justification='center', font='Helvetica 12')],
						  [sg.Text('Left Camera ', justification='center', font='Helvetica 12')],
						  [sg.Text('Left Camera ', justification='center', font='Helvetica 12')],
						  [sg.Text('Left Camera ', justification='center', font='Helvetica 12')],
						 ]
	tab_left=[ #key='tab_left'
			  [sg.Column(column_Tab_lef_LEFT),sg.Column(column_Tab_lef_RIGHT)],
			  [sg.Text('Select Camera Left')],
			  [sg.Text('Select Camera Left')],
			  [sg.Text('Select Camera Left')],
			  ]
#----------------------------------------tab_right  -------------------------------------------------------------------------------
	column_Tab_right_LEFT=[
						  [sg.Text('right Camera ', justification='center', font='Helvetica 12')],
						  [sg.Image(filename='',  key='column_Tab_right_LEFT_image')],
						 ]
	column_Tab_right_RIGHT=[
						  [sg.Text('right Camera ', justification='center', font='Helvetica 12')],
						  [sg.Text('right Camera ', justification='center', font='Helvetica 12')],
						  [sg.Text('right Camera ', justification='center', font='Helvetica 12')],
						  [sg.Text('right Camera ', justification='center', font='Helvetica 12')],
						  [sg.Text('right Camera ', justification='center', font='Helvetica 12')],
						 ]
	tab_right=[ #key='tab_right'
			  [sg.Column(column_Tab_right_LEFT),sg.Column(column_Tab_right_RIGHT)],
			  [sg.Text('Select Camera right')],
			  [sg.Text('Select Camera right')],
			  [sg.Text('Select Camera right')],
			  ]
#-------------------------------------------------tab_both----------------------------------------------------------------------			  
	column_Tab_both_LEFT=[
						  [sg.Text('left Camera ', justification='center', font='Helvetica 12')],
						  [sg.Image(filename='',  key='column_Tab_both_LEFT_image')],
						 ]
	column_Tab_both_RIGHT=[
						  [sg.Text('right Camera ', justification='center', font='Helvetica 12')],
						  [sg.Image(filename='',  key='column_Tab_both_RIGHT_image')],
						 ]
	tab_both=[ #key='tab_both'
			  [sg.Column(column_Tab_both_LEFT),sg.Column(column_Tab_both_RIGHT)],
			  [sg.Text('both Camera ')],
			  [sg.Text('both Camera ')],
			  [sg.Text('both Camera ')],
			  ]
#-----------------------------------------------------------------------------------------------------------------------


	layout =[
			#[sg.Text('(Almost) All widgets in one Window!', size=(50, 1), justification='center')],
			[sg.TabGroup([[
							sg.Tab('Main',         tab_Main ,key='tab_Main'),
							sg.Tab('Left Camera' , tab_left  ,key='tab_left' ),
							sg.Tab('Right Camera', tab_right,key='tab_right' ),
							sg.Tab('Both Camera',  tab_both ,key='tab_both' ),
							]],enable_events=True,key='NEW_TAB')
				],
			[	sg.Text('Select Camera left'),sg.InputCombo(('0', '1','2','3'), size=(2, 1),key='camera_left',default_value='1'),
				sg.Text('Select Camera right'),sg.InputCombo(('0', '1','2','3'), size=(2, 1),key='camera_right',default_value='2'),
				sg.Text('				'),
				sg.Button('Record', size=(8, 1), pad=(4,4),font='Helvetica 10'),
				sg.Button('Stop', size=(8, 1),  pad=(4,4),font='Any 10'),
				sg.Button('Exit', size=(8, 1),  pad=(4,4),font='Helvetica 10'),
				sg.Button('About', size=(8,1),  pad=(4,4),font='Any 10')]
			]


	#sg.ChangeLookAndFeel('LightGreen')
	sg.SetOptions(element_padding=(0, 0))
	# SetOptions(icon=None,
    # button_color=None,
    # element_size=(None, None),
    # button_element_size=(None, None),
    # margins=(None, None),
    # element_padding=(None, None),
    # auto_size_text=None,
    # auto_size_buttons=None,
    # font=None,
    # border_width=None,
    # slider_border_width=None,
    # slider_relief=None,
    # slider_orientation=None,
    # autoclose_time=None,
    # message_box_line_width=None,
    # progress_meter_border_depth=None,
    # progress_meter_style=None,
    # progress_meter_relief=None,
    # progress_meter_color=None,
    # progress_meter_size=None,
    # text_justification=None,
    # background_color=None,
    # element_background_color=None,
    # text_element_background_color=None,
    # input_elements_background_color=None,
    # input_text_color=None,
    # scrollbar_color=None,
    # text_color=None,
    # element_text_color=None,
    # debug_win_size=(None, None),
    # window_location=(None, None),
    # error_button_color=(None, None),
    # tooltip_time=None)

	window = sg.Window("Sterio Camera Depth Calculation",
                   default_element_size=(12, 1),
                   text_justification='c',
                   auto_size_text=True,
                   auto_size_buttons=True,
                   no_titlebar=False,
                   grab_anywhere=False,
				   keep_on_top=True,
				    #location=(400,200),
				    # button_color=None,
					# font=None,
					# progress_bar_color=(None, None),
					# background_color=None,
					# border_depth=None,
					# auto_close=False,
					# auto_close_duration=DEFAULT_AUTOCLOSE_TIME,
					# icon=DEFAULT_WINDOW_ICON,
					# force_toplevel = False,
				    #return_keyboard_events=True,
					# use_default_focus=True,
					resizable=True,
                   default_button_element_size=(12, 1))
	return window.Layout(layout).Finalize()
	# ---===---  Event LOOP Read and display frames, operate the GUI --- #
def opencv_feature(values):
	if values['canny']:
		MiddleImgbytes = cv2.Canny(MiddleImgbytes, values['canny_slider_a'], values['canny_slider_b'])

	if values['ndis']:
		numDisparities=int(int(values['ndis_slider']/16)*16);
		#print("numDisparities=",numDisparities)
		#print( frame.dtype ) byte8
		#print( frame_gray.dtype ) byte8
		#print( LeftImgbytes.dtype )
		#print( stereo.dtype )
		#print( disparity.dtype ) int16
		#print(stereo,disparity ) <StereoBM 000000000B767110> ,mat

	if values['blockSize']:
		pass#print(int(values['blockSize_slider']))#blockSize
	if values['thresh']:
		#disparity    = cv2.cvtColor(disparity, cv2.COLOR_BGR2LAB)[:, :, 0]
		_, disparity = cv2.threshold(disparity, values['thresh_slider'], 255, cv2.THRESH_BINARY)

	if values['blur']:
		disparity = cv2.GaussianBlur(disparity, (21, 21), values['blur_slider'])
	if values['hue']:
		disparity = cv2.cvtColor(disparity, cv2.COLOR_BGR2HSV)
		disparity[:, :, 0] += values['hue_slider']
		disparity = cv2.cvtColor(disparity, cv2.COLOR_HSV2BGR)
	if values['enhance']:
		enh_val = values['enhance_slider'] / 40
		clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
		lab = cv2.cvtColor(disparity, cv2.COLOR_BGR2LAB)
		lab[:, :, 0] = clahe.apply(lab[:, :, 0])
		disparity = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
	if values['contour']:
		hue = cv2.cvtColor(disparity, cv2.COLOR_BGR2HSV)
		hue = cv2.GaussianBlur(hue, (21, 21), 1)
		hue = cv2.inRange(hue, np.array([values['contour_slider'], values['base_slider'], 40]),
						  np.array([values['contour_slider'] + 30, 255, 220]))
		_, cnts, _ = cv2.findContours(hue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cv2.drawContours(disparity, cnts, -1, (0, 0, 255), 2)
	#disparity=cv2.resize(disparity,(Width,Height));



def handle_Events(event):
	global CameraRecording,MiddleSource,MODE
	print("New Event:",event)
	if   event == 'Exit' :
			stop_camera()
			sys.exit(0)
	elif event == 'Record':
			start_camera()
			CameraRecording = True

	elif event == 'Stop':
			stop_camera()
			CameraRecording = False
			# img = np.full((480, 640),255)
			# imgbytes=cv2.imencode('.png', img)[1].tobytes() #this is faster, shorter and needs less includes
			# window.FindElement('image').Update(data=imgbytes)
	elif event == 'About':
			sg.PopupNoWait('AUT CAIR lab',
						   'CAIR.aut.ac.nz',
						   'Albot robot',
						   'prepare depth calculation',
						   #'ENJOY!  Go make something really cool with this... please!',
						   keep_on_top=True)
	elif event ==    'combineCam':
		MiddleSource='combineCam'
	elif event ==    'LeftCam':
		MiddleSource='LeftCam'
	elif event ==    'RightCam':
		MiddleSource='RightCam'
	elif event ==    'canny':
		MODE='canny'
	elif event ==    'thresh':
		MODE='thresh'
	elif event ==    'blur':
		MODE='blur'
	elif event ==    'contour':
		MODE='contour'
	elif event ==    'enhance':
		MODE='enhance'
	elif event ==    'hue':
		MODE='hue'
	elif event ==    'line':
		MODE='line'
	elif event ==    'ChessCorner':
		MODE='ChessCorner'
	elif event ==    'detect':
		MODE='detect'		#
	elif event=='NEW_TAB':
		if values['NEW_TAB']=='tab_left':		   	
			MODE='tab_left'
		elif values['NEW_TAB']=='tab_right':
			MODE='tab_right'
		elif values['NEW_TAB']=='tab_both':
			MODE='tab_both'
		else:
			MODE='tab_Main'
	elif event ==    'NONE':
		MODE='NONE'

def main():
	global values;
	window=GUI_c()
	gui_queue = queue.Queue()
	while True:
		event, values = window.Read(timeout=0, timeout_key='timeout')
		#(event or timeout_key or None, Dictionary of values or List of values from all elements in the Window)
		if  event!='timeout' or event is None:
			#oldEvent=event;
			handle_Events(event)
			#if event=='NEW_TAB':
				#print('FindElementWithFocus',window.FindElement('NEW_TAB').FindKeyFromTabName('tab_left'))
		if CameraRecording:
			frameLsmall,MiddleImg,frameRsmall=showFrams()
			
			if MODE=='tab_left':
				window.FindElement('column_Tab_lef_LEFT_image').Update(data=cv2.imencode('.png',   frameL)[1].tobytes())
			elif MODE=='tab_right':
				window.FindElement('column_Tab_right_LEFT_image').Update(data=cv2.imencode('.png',   frameR)[1].tobytes())
			elif MODE=='tab_both':
				window.FindElement('column_Tab_both_LEFT_image').Update(data=cv2.imencode('.png',   frameL)[1].tobytes())	
				window.FindElement('column_Tab_both_RIGHT_image').Update(data=cv2.imencode('.png',   frameR)[1].tobytes())
			else:	
				# defualf is stero MiddleSource is selected
				if   MODE=='canny':
					MiddleImg = MiddleImg.astype(np.uint8);#print(numberOfChannel(MiddleImg))
					MiddleImg = cv2.Canny(MiddleImg, values['canny_slider_a'], values['canny_slider_b'],apertureSize = 3)
				elif MODE=='thresh':
					ret,MiddleImg = cv2.threshold(MiddleImg,values['thresh_slider'], 255, cv2.THRESH_BINARY)
				elif MODE=='hue' and MiddleSource!='combineCam':
					MiddleImg = cv2.cvtColor(MiddleImg, cv2.COLOR_BGR2HSV)
					MiddleImg[:, : , 0] += int(values['hue_slider'])
					MiddleImg = cv2.cvtColor(MiddleImg, cv2.COLOR_HSV2BGR)
				elif MODE=='enhance' and MiddleSource!='combineCam':
					enh_val = values['enhance_slider'] / 40
					clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
					lab   = cv2.cvtColor(MiddleImg, cv2.COLOR_BGR2LAB)
					lab[:, :, 0] = clahe.apply(lab[:, :, 0])
					MiddleImg = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
				elif MODE=='contour' and MiddleSource!='combineCam':
					#print("MiddleImg:",MiddleImg.shape,MiddleImg.dtype,numberOfChannel(MiddleImg))
					hue = cv2.cvtColor(MiddleImg, cv2.COLOR_BGR2GRAY)
					#hue = cv2.GaussianBlur(hue, (21, 21), 1)
					#hue = cv2.inRange(hue, np.array([values['contour_slider'], values['base_slider'], 40]),np.array([values['contour_slider'] + 30, 255, 220]))
					ret,thresh = cv2.threshold(hue,values['thresh_slider'], 255, cv2.THRESH_BINARY)
					cnts,hierachy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
					#print(cnts)
					cv2.drawContours(MiddleImg, cnts, -1, (0, 0, 255), 2)
				elif MODE=='blur' and MiddleSource!='combineCam':
					MiddleImg = cv2.GaussianBlur(MiddleImg, (21, 21), values['blur_slider'])
				elif MODE=='ChessCorner':
					MiddleImg = np.uint8(MiddleImg) #just data type not   channel
					#MiddleImg = (MiddleImg).astype(np.uint8)
					if numberOfChannel( MiddleImg)> 1:
						MiddleImg=cv2.cvtColor(MiddleImg, cv2.COLOR_BGR2GRAY)
					#print (int(values['ChesX_slider']),int(values['ChesY_slider']))
					found, corners = cv2.findChessboardCorners(MiddleImg, (int(values['ChesX_slider']),int(values['ChesY_slider'])), None)
					if found:
						print(corners)
					window.FindElement('ChessNum').Update(found)
				elif MODE=='line':
					minLineLength = int( values['linemin_slider'])
					maxLineGap =  int( values['linemax_slider'])
					lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
					for rho,theta in lines[0]:
						a = np.cos(theta)
						b = np.sin(theta)
						x0 = a*rho
						y0 = b*rho
						x1 = int(x0 + 1000*(-b))
						y1 = int(y0 + 1000*(a))
						x2 = int(x0 - 1000*(-b))
						y2 = int(y0 - 1000*(a))
						cv2.line(MiddleImg,(x1,y1),(x2,y2),(0,0,255),2)
				elif MODE=='detect' and MiddleSource!='combineCam':
					#MiddleImg = cv2.cvtColor(MiddleImg, cv2.COLOR_BGR2HSV)
					bbox, label, conf = cv.detect_common_objects(MiddleImg)
					print(bbox, label, conf)
					MiddleImg = draw_bbox(MiddleImg, bbox, label, conf)
				elif MODE=='startTh' :
					print('start thereding')
					#thread_id.threading.Thread(target=long_function_wrapper, args=(work_id, gui_queue,), daemon=True).start()
				elif event == 'StopTh':
					thread_id.exit


				try:
					message = gui_queue.get_nowait()    # see if something has been posted to Queue
				except queue.Empty:                     # get_nowait() will get exception when Queue is empty
					message = None                      # nothing in queue so do nothing

				# if message received from queue, then some work was completed
				if message is not None:
					window.Element('OUTPUT2').Update('Complete Work ID ')


				
				window.FindElement('ROI').Update(   data=cv2.imencode('.png'   , template)[1].tobytes())
				window.FindElement('imageL').Update(data=cv2.imencode('.png', frameLsmall)[1].tobytes())
				window.FindElement('output').Update(data=cv2.imencode('.png',   MiddleImg)[1].tobytes())
				window.FindElement('imageR').Update(data=cv2.imencode('.png', frameRsmall)[1].tobytes())



main()
exit()