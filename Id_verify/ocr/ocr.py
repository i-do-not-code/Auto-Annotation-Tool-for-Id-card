from __future__ import print_function
import glob
import os
import sys
import numpy as np
import cv2
sys.path.append(os.getcwd())

from lib.fast_rcnn.config import cfg, cfg_from_file
from lib.fast_rcnn.test import _get_blobs
from lib.text_connector.text_connect_cfg import Config as TextLineCfg
from PIL import Image
import pytesseract
import argparse
import ftfy

################################################################################################################
############################# Section 1: Initiate the command line interface ###################################
################################################################################################################

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--preprocess", type=str, default="cubic",
                help="type of preprocessing to be done, choose from blur, linear, cubic or bilateral")
args = vars(ap.parse_args())

'''
Our command line arguments are parsed. We have two command line arguments:

--image : The path to the image we’re sending through the OCR system.
--preprocess : The preprocessing method. This switch is optional and for this tutorial and can accept the following 
                parameters to be passed (refer sections to know more:
                - blur
                - adaptive
                - linear
                - cubic
                - gauss
                - bilateral
                - thresh (meadian threshold - default)
                
------  Use Blur when the image has noise/grain/incident light etc. ------
'''







##############################################################################################################
###################### Section 2: Load the image -- Preprocess it -- Write it to disk ########################
##############################################################################################################
def ocr_extract_text(image):
	# load the example image and convert it to grayscale
	image = cv2.imread(image)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# check to see if we should apply thresholding to preprocess the
	# image
	if args["preprocess"] == "thresh":
	    gray = cv2.threshold(gray, 0, 255,
	                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	elif args["preprocess"] == "adaptive":
	    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

	if args["preprocess"] == "linear":
	    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

	elif args["preprocess"] == "cubic":
	    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

	if args["preprocess"] == "blur":
	    gray = cv2.medianBlur(gray, 3)

	elif args["preprocess"] == "bilateral":
	    gray = cv2.bilateralFilter(gray, 9, 75, 75)

	elif args["preprocess"] == "gauss":
	    gray = cv2.GaussianBlur(gray, (5,5), 0)

	# write the grayscale image to disk as a temporary file so we can
	# apply OCR to it
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	##############################################################################################################
	######################################## Section 3: Running PyTesseract ######################################
	##############################################################################################################

	# load the image as a PIL/Pillow image, apply OCR, and then delete
	# the temporary file
	text = pytesseract.image_to_string(Image.open(filename), lang = 'eng',config='-psm 6')
	# add +hin after eng within the same argument to extract hindi specific text - change encoding to utf-8 while writing
	os.remove(filename)
	return text





def resize_im(im, scale, max_scale=None):
    f = float(scale) / min(im.shape[0], im.shape[1])
    if max_scale != None and f * max(im.shape[0], im.shape[1]) > max_scale:
        f = float(max_scale) / max(im.shape[0], im.shape[1])
    return cv2.resize(im, None, None, fx=f, fy=f, interpolation=cv2.INTER_LINEAR), f



##########################This function is ropping the images################## 
###############according the boxes we get from my previous ctnc model##########
def crop(image, coords, saved_location,image_name,image_no):
    img = Image.open(image_name)
    base_name = image_name.split('/')[-1]
    name = str(image_no) + '.jpg'
    if os.path.exists(cfg.DATA_DIR  + '/temp/' + base_name.split('.')[0]):
    	base_name = image_name.split('/')[-1]
    else:
    	os.mkdir(cfg.DATA_DIR  + '/temp/' + base_name.split('.')[0])
    saved_location = cfg.DATA_DIR  + '/temp/' + base_name.split('.')[0] + '/' + name
    cropped_image = img.crop(coords)
    cropped_image.save(saved_location)
    text = ocr_extract_text(saved_location)
    return text


############ Getting the data from results, obtained from Ctcn################
im_names = glob.glob(os.path.join(cfg.DATA_DIR, 'demo', '*.png')) + glob.glob(os.path.join(cfg.DATA_DIR, 'demo', '*.jpg'))
for im_name in im_names:
	img = cv2.imread(im_name)
	img, scale = resize_im(img, scale=TextLineCfg.SCALE, max_scale=TextLineCfg.MAX_SCALE)
	base_name = im_name.split('/')[-1]
	#print (base_name)
	line = ""
	with open(cfg.DATA_DIR +'/results/' + 'res_{}.txt'.format(base_name.split('.')[0]), 'r') as f:
		i = 0
		boxes = f.readlines()
		for box in boxes:
			i = i + 1
			box = box.strip('\n')
			co_ords = box.split(',')
			min_x = int(co_ords[0])
			min_y = int(co_ords[1])
			max_x = int(co_ords[2])
			max_y = int(co_ords[3])
			text = crop(img, (min_x,min_y,max_x,max_y),'data/temp/',im_name,i)
			line += ','.join([str(min_x), str(min_y), str(max_x), str(max_y),str(text)]) + '\r\n'
		f.close()
	cur_dir = os.getcwd()
	with open( cur_dir +'/ocr/results/' + 'ocr_res_{}.txt'.format(base_name.split('.')[0]), 'w') as f:
		f.write(line)
		f.close()

