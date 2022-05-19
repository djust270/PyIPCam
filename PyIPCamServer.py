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


lock = threading.Lock()
video = VideoStream(src=0).start()

def vid_stream():
	# grab global references to the output frame and lock variables
	global outputFrame, lock
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
cam_app = Flask(__name__)
@cam_app.route("/")
def index():
	return render_template("index.html")
@cam_app.route("/video_stream")
def video_feed():
	return Response(vid_stream(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
cam_app.run(host='127.0.0.1', port='8000', debug=True,
		threaded=True, use_reloader=False)
video.stop()