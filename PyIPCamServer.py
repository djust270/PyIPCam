from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
from imutils.video import VideoStream
import time
import cv2
from numpy import vdot

# define arguments 
parser = argparse.ArgumentParser()
parser.add_argument("-port", dest="serv_port" , type=str, default='8000', help="Server TCP Port Number")
parser.add_argument("-index", dest="cam_index" , type=int, default = 0, help="Camera index number")
parser.add_argument("-width", dest="img_width" , type=str, default = '480', help="Camera Width in pixels")
parser.add_argument("-height", dest="img_height" , type=str, default = '600', help="Camera Width in pixels")


args = vars(parser.parse_args())


lock = threading.Lock()
video = VideoStream(src=args['cam_index'], resolution=(args['img_height'], args['img_width'])).start()

def vid_stream(stream_type):
	# grab global references to the output frame and lock variables
	global lock
	
	# loop over frames from the output stream
	
	while True:
		frame = video.read()
		with lock:
			stream_output = frame.copy()
			if stream_output is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", stream_output)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')
		if stream_type == "im":
			break
cam_app = Flask(__name__)
@cam_app.route("/")
def index():
	return render_template("index.html")
@cam_app.route("/video_stream")
def video_stream():
	return Response(vid_stream('vd'),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
@cam_app.route("/single_img")
def single_img():
	return Response(vid_stream('im'),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
cam_app.run(host='127.0.0.1', port='8000', debug=True,
		threaded=True, use_reloader=False)
