#!pip install pytube3 --upgrade
#pip install opencv-python

from pytube import YouTube
import cv2
import os

def youtub2imgs(dir_name,youtube_url,frame_name,total_images,folder_images):

	if not os.path.exists(dir_name):
			os.mkdir(dir_name)
			print("Directory " , dir_name ,  " Created ")
	else:    
		print("Directory " , dir_name ,  " already exists")
		
	YouTube(youtube_url).streams.first().download(dir_name)

	#-----------

	files = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(dir_name):
		for file in f:
			if '.mp4' in file:
				files.append(os.path.join(r, file))

	for f in files:
		print(f)

	if not os.path.exists(folder_images):
			os.mkdir(folder_images)
			print("Directory " , folder_images ,  " Created ")
	else:    
		print("Directory " , folder_images ,  " already exists")
		
		#---------------
	vidcap = cv2.VideoCapture(f)
	success,image = vidcap.read()
	count = 0
	while success:
	  cv2.imwrite(folder_images+'/'+frame_name+"%d.jpg" % count, image)     # save frame as JPEG file      
	  success,image = vidcap.read()
	  #print('Read a new frame: ', success)
	  count += 1
	  if count==total_images:
		  break
	print('finish is success')

