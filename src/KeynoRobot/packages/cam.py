import cv2 as cv
from datetime import datetime
import time,sys
import numpy as np

class MotionDetector():
    def onChange(self, val): #callback when the user change the ceil
        self.ceil = val

    def __init__(self,ceil=8, doRecord=True, showWindows=True):
        self.writer = None
        self.font = None
        self.doRecord=doRecord #Either or not record the moving object
        self.show = showWindows #Either or not show the 2 windows
        self.frame = None

        self.capture=cv.VideoCapture(0)
        self.frame =self.capture.read() #Take a frame to init recorder
        if doRecord:
            self.initRecorder()

        self.frame1gray = cv.CreateMat(self.frame.height, self.frame.width, cv.CV_8U) #Gray frame at t-1
        cv.CvtColor(self.frame, self.frame1gray, cv.CV_RGB2GRAY)

        #Will hold the thresholded result
        self.res = cv.CreateMat(self.frame.height, self.frame.width, cv.CV_8U)

        self.frame2gray = cv.CreateMat(self.frame.height, self.frame.width, cv.CV_8U) #Gray frame at t

        self.width = self.frame.width
        self.height = self.frame.height
        self.nb_pixels = self.width * self.height
        self.ceil = ceil
        self.isRecording = False
        self.trigger_time = 0 #Hold timestamp of the last detection

        if showWindows:
            cv.NamedWindow("Image")
            cv.CreateTrackbar("Mytrack", "Image", self.ceil, 100, self.onChange)

    def initRecorder(self): #Create the recorder
        codec = cv.CV_FOURCC('D', 'I', 'V', 'X')
        #codec = cv.CV_FOURCC("D", "I", "B", " ")
        self.writer=cv.CreateVideoWriter(datetime.now().strftime("%b-%d_%H:%M:%S")+".avi", codec, 15, cv.GetSize(self.frame), 1)
        #FPS set at 15 because it seems to be the fps of my cam but should be ajusted to your needs
        self.font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 2, 8) #Creates a font

    def run(self):
        started = time.time()
        while True:

            curframe = cv.QueryFrame(self.capture)
            instant = time.time() #Get timestamp o the frame

            self.processImage(curframe) #Process the image

            if not self.isRecording:
                if self.somethingHasMoved():
                    self.trigger_time = instant #Update the trigger_time
                    if instant > started +5:#Wait 5 second after the webcam start for luminosity adjusting etc..
                        print ("Something is moving !")
                        if self.doRecord: #set isRecording=True only if we record a video
                            self.isRecording = True
            else:
                if instant >= self.trigger_time +10: #Record during 10 seconds
                    print ("Stop recording")
                    self.isRecording = False
                else:
                    cv.PutText(curframe,datetime.now().strftime("%b %d, %H:%M:%S"), (25,30),self.font, 0) #Put date on the frame
                    cv.WriteFrame(self.writer, curframe) #Write the frame

            if self.show:
                cv.ShowImage("Image", curframe)
                cv.ShowImage("Res", self.res)

            cv.Copy(self.frame2gray, self.frame1gray)
            c=cv.WaitKey(1)
            if c==27 or c == 1048603: #Break if user enters 'Esc'.
                break

    def processImage(self, frame):
        cv.CvtColor(frame, self.frame2gray, cv.CV_RGB2GRAY)

        #Absdiff to get the difference between to the frames
        cv.AbsDiff(self.frame1gray, self.frame2gray, self.res)

        #Remove the noise and do the threshold
        cv.Smooth(self.res, self.res, cv.CV_BLUR, 5,5)
        element = cv.CreateStructuringElementEx(5*2+1, 5*2+1, 5, 5,  cv.CV_SHAPE_RECT)
        cv.MorphologyEx(self.res, self.res, None, None, cv.CV_MOP_OPEN)
        cv.MorphologyEx(self.res, self.res, None, None, cv.CV_MOP_CLOSE)
        cv.Threshold(self.res, self.res, 10, 255, cv.CV_THRESH_BINARY_INV)

    def somethingHasMoved(self):
        nb=0 #Will hold the number of black pixels

        for y in range(self.height): #Iterate the hole image
            for x in range(self.width):
                if self.res[y,x] == 0.0: #If the pixel is black keep it
                    nb += 1
        avg = (nb*100.0)/self.nb_pixels #Calculate the average of black pixel in the image
        #print "Average: ",avg, "%\r",
        if avg > self.ceil:#If over the ceil trigger the alarm
            return True
        else:
            return False







def sparse_optical_flow(cap):
    # Parameters for Shi-Tomasi corner detection
    feature_params = dict(maxCorners = 300, qualityLevel = 0.2, minDistance = 2, blockSize = 7)
    # Parameters for Lucas-Kanade optical flow
    lk_params = dict(winSize = (15,15), maxLevel = 2, criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))	
    color = (0, 255, 0)# Variable for color to draw optical flow track
    ret, first_frame = cap.read()
    prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
    mask = np.zeros_like(first_frame)
    prev = cv.goodFeaturesToTrack(prev_gray, mask = None, **feature_params)
    # Creates an image filled with zero intensities with the same dimensions as the frame - for later drawing purposes
    while(cap.isOpened()):		 
        ret, frame = cap.read()		
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)		
        next, status, error = cv.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)		
        good_old = prev[status == 1]# Selects good feature points for previous position		
        good_new = next[status == 1]# Selects good feature points for next position
        # Draws the optical flow tracks
        for i, (new, old) in enumerate(zip(good_new, good_old)):			
            a, b = new.ravel()# Returns a contiguous flattened array as (x, y) coordinates for new point			
            c, d = old.ravel()# Returns a contiguous flattened array as (x, y) coordinates for old point			
            mask = cv.line(mask, (a, b), (c, d), color, 2)# Draws line between new and old position with green color and 2 thickness			
            frame = cv.circle(frame, (a, b), 3, color, -1)# Draws filled circle (thickness of -1) at new position with green color and radius of 3

        output = cv.add(frame, mask)# Overlays the optical flow tracks on the original frame		
        prev_gray = gray.copy()# Updates previous frame		
        prev = good_new.reshape(-1, 1, 2)# Updates previous good feature points		
        cv.imshow("sparse optical flow", output)# Opens a new window and displays the output frame
        # Frames are read by intervals of 10 milliseconds. The programs breaks out of the while loop when the user presses the 'q' key
        if cv.waitKey(10) & 0xFF == ord('q'):
            break
    # The following frees up resources and closes all windows

def Dense_Optical_Flow(cap):
    ret, first_frame = cap.read()
    prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
    mask = np.zeros_like(first_frame)	
    mask[..., 1] = 255
    while(cap.isOpened()):		
        ret, frame = cap.read()		
        cv.imshow("input", frame)		
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)		
        flow = cv.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)		
        magnitude, angle = cv.cartToPolar(flow[..., 0], flow[..., 1])# Computes the magnitude and angle of the 2D vectors		
        mask[..., 0] = angle * 180 / np.pi / 2 # Sets image hue according to the optical flow direction		
        mask[..., 2] = cv.normalize(magnitude, None, 0, 255, cv.NORM_MINMAX)# Sets image value according to the optical flow magnitude (normalized)		
        rgb = cv.cvtColor(mask, cv.COLOR_HSV2BGR)# Converts HSV to RGB (BGR) color representation		
        cv.imshow("dense optical flow", rgb)# Opens a new window and displays the output frame		
        prev_gray = gray# Updates previous frame
        # Frames are read by intervals of 1 millisecond. The programs breaks out of the while loop when the user presses the 'q' key
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

def select_point(event, x, y, flags, params):
    global point, point_selected, old_points
    if event == cv.EVENT_LBUTTONDOWN:
        point = (x, y)
        point_selected = True
        old_points = np.array([[x, y]], dtype=np.float32)

def optical_flow(cap):
    _, frame = cap.read()
    old_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Lucas kanade params
    lk_params = dict(winSize = (15, 15),maxLevel = 4,criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
    # Mouse function
    cv.namedWindow("Frame")
    cv.setMouseCallback("Frame", select_point)
    point_selected = False
    point = ()
    old_points = np.array([[]])
    while True:
        _, frame = cap.read()
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        if point_selected is True:
            cv.circle(frame, point, 5, (0, 0, 255), 2)
            new_points, status, error = cv.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points, None, **lk_params)
            old_gray = gray_frame.copy()
            old_points = new_points
            x, y = new_points.ravel()
            cv.circle(frame, (x, y), 5, (0, 255, 0), -1)
        cv.imshow("Frame", frame)
        key = cv.waitKey(1)
        if key == 27:
            break






def main():
    print("camera  loading")
    cap = cv.VideoCapture(0)
    sparse_optical_flow(cap)
    #optical_flow(cap)
    #Dense_Optical_Flow(cap)
    cap.release()
    cv.destroyAllWindows()    

if __name__ == "__main__":
    sys.exit(main())
