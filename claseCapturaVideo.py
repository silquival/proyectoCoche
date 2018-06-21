# import the necessary packages
from threading import Thread
import io
import socket
import struct
import time
import picamera
import cv2
import numpy as np

start = time.time()
server_ip = '192.168.1.137'
server_port = 8000
recording_time = 10
print('uno')
 
class WebcamVideoStream:
	
	def __init__(self):
		
             self.image_width = 320
             self.image_height = 240
             self.image_fps = 10
             print('dentro de la clase')             
             # initialize the variable used to indicate if the thread should
             # be stopped
             self.stopped = False


             # initialize los valores de la camara
             
             with picamera.PiCamera() as self.camera:
             #   self.camera.resolution = (self.image_width, self.image_height)
             #    self.camera.framerate = self.image_fps
             #    print('dentro del with')
             #    # Give 2 secs for camera to initilize
             #    time.sleep(2)                       
             #    self.stream = io.BytesIO()
             #    print('al final del wiyh')               
             #self.camera=picamera.Picamera
              self.camera.resolution = (self.image_width, self.image_height)
              self.camera.framerate = self.image_fps
              # Give 2 secs for camera to initilize
              time.sleep(2)                       
              self.stream = io.BytesIO()
              print('al final del with')
              print(type(self.stream))
	
	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
 
	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
 
			# otherwise, read the next frame from the stream
			self.camera.capture_continuous(self.stream, 'jpeg', use_video_port = True)

	def leer(self):
		# return the frame most recently read
		print('inicio leer')
		print(type(self.stream))
		return self.stream
 
	def stop(self):
		# indicate that the thread should be stopped
             self.stopped = True



# create socket and bind host
print('dos')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('dos')
client_socket.connect((server_ip, server_port))
print('tres')
connection = client_socket.makefile('wb')
print( 'Connection creada on videostream thread' )
wvs= WebcamVideoStream().start()
print('despues de la clase')
print(time.time()-start)
while time.time()- start < recording_time:

       print('dentro del while')
       cuadro=wvs.leer()
       print('tipo de cuadro',type(cuadro))
       print('despues del read')
       image_data=np.asarray(cuadro)
       print('tipo del cuadro 2', image_data.shape)
       cv2.imwrite('cuadro.jpg',image)
       connection.write(struct.pack('<L', cuadro.tell()))
       connection.flush()
       cuadro.seek(0)
       connection.write(cuadro.read())

connection.close()
client_socket.close()
print( 'JPEG streaming finished!' );

