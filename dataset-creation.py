# Importing all necessary libraries
import cv2, os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-s','--source', help='Provide a custom video path')
parser.add_argument('-c', '--count', help='Provide what number to start the count from', type=int)
parser.add_argument('-d', '--directory', help='Provide path of directory where dataset should be saved')
args = parser.parse_args()

# Read the video from specified path
cam = cv2.VideoCapture(str(args.source))

try:	
	# creating a folder named data
	if not os.path.exists(str(args.directory)):
		os.makedirs(str(args.directory))

# if not created then raise error
except OSError:
	print ('Error while creating directory for dataset')

# frame
current_frame = args.count
while True:
	# reading from frame
	ret, frame = cam.read()

	if ret:
		# if video is still left continue creating images
		name = str(args.directory) + '/frame' + str(current_frame) + '.jpg'
		print ('Creating...' + name)

		# writing the extracted images
		cv2.imwrite(name, frame)

		# increasing counter so that it will
		# show how many frames are created
		current_frame += 1
	else:
		break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()