from flask import Response, send_file
from flask import Flask
from flask import render_template
import threading
import argparse
import imutils
from imutils.video import VideoStream
import cv2
from numpy import vdot
import os
import sys

# define arguments 
parser = argparse.ArgumentParser()
parser.add_argument("-port", dest="serv_port" , type=str, default='8000', help="Server TCP Port Number")
parser.add_argument("-index", dest="cam_index" , type=int, default = 0, help="Camera index number")
parser.add_argument("-width", dest="img_width" , type=int, default = 640, help="Camera Width in pixels")
parser.add_argument("-height", dest="img_height" , type=int, default = 480, help="Camera Width in pixels")
parser.add_argument("-ip",  dest="serv_ip" , type=str, default = '127.0.0.1', help="Server IP Address")

args = vars(parser.parse_args())
resolution=(int(args['img_width']), int(args['img_height']))
lock = threading.Lock()
video = VideoStream(src=args['cam_index']).start()
print(f"Selected resolution : {resolution}")
def vid_stream():
	global lock
	global resolution
	global video		
	while True:
		#frame = video.read()
		frame = imutils.resize(video.read(), width=resolution[0], height=resolution[1])
		with lock:
			stream_output = frame.copy()
			if stream_output is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpeg", stream_output)
			# ensure the frame was successfully encoded
			if not flag:
				continue			
				# yield the output frame in the byte format
			yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
				bytearray(encodedImage) + b'\r\n')	
def img_stream():
	frame = imutils.resize(video.read(), width=resolution[0], height=resolution[1])
	cv2.imwrite("./image.jpeg",frame)	
if getattr(sys, 'frozen', False):
	template_folder = os.path.join(sys._MEIPASS, 'templates')
	cam_app = Flask(__name__ , template_folder=template_folder)
else :
	cam_app = Flask(__name__)
@cam_app.route("/")
def index():
	return render_template("index.html")
@cam_app.route("/video_stream")
def video_stream():
	return Response(vid_stream(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
@cam_app.route("/jpeg")
def jpeg():
	#return Response(vid_stream('im'), mimetype='image/jpeg')
	img_stream()
	return send_file('image.jpeg', mimetype='image/jpeg')

cam_app.run(host=args['serv_ip'], port=args['serv_port'], debug=True,
		threaded=True, use_reloader=False)




