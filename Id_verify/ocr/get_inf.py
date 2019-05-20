from __future__ import print_function
import os
import sys
import re
import glob
import json
from lib.fast_rcnn.config import cfg, cfg_from_file

def arr_to_str(arr):
	string = ''
	for element in arr:
		string = string + ' ' + element
	return string.strip()

cur_dir = os.getcwd()
im_names = glob.glob(os.path.join(cfg.DATA_DIR, 'demo', '*.png')) + glob.glob(os.path.join(cfg.DATA_DIR, 'demo', '*.jpg'))
for im_name in im_names:
	base_name = im_name.split('/')[-1]
	#print (base_name)
	with open( cur_dir +'/ocr/results/' + 'ocr_res_{}.txt'.format(base_name.split('.')[0]), 'r') as f:
		boxes = f.read()
		boxes = boxes.split('\n')
		boxes = boxes[:-1]

		sort_boxes = []
		#### Making dictonary for sorting #####
		for box in boxes:
			co_ord = box.split(',')
			if len(co_ord) >= 5:
				sort_boxes.append(co_ord)

		sort_boxes.sort(key=lambda x: (int(x[3]),int(x[0])))
		
	with open( cur_dir +'/Id_result/text/' + 'ocr_res_{}.txt'.format(base_name.split('.')[0]), 'w') as f:
		prev_y = 0
		content = ""
		for box in sort_boxes:
			text_arr = box[4:]
			text = arr_to_str(text_arr)
			if prev_y != box[3]:
				content += '\n' + text
			else:
				content += '    ' + text 
			prev_y = box[3]
		f.write(content)

	#print (content)
############################################################################################################
###################################### Section 4: Extract relevant information #############################
############################################################################################################
	text = content
	# Initializing data variable
	name = None
	email =None
	mob = None
	address = None 
	dob = None 

	nameline = []
	dobline = []
	text0 = []
	text1 = []
	text2 = []

	# Searching for Detail
	lines = text.split('\n')
	for lin in lines:
	    s = lin.strip()
	    s = lin.replace('\n','')
	    s = s.rstrip()
	    s = s.lstrip()
	    text1.append(s)

	text1 = list(filter(None, text1))
	#print(text1)

	#### Regex for extracting all email and Mobile or Phone number on id card#####
	emails = []
	phones = [] 
	dates = []
	c_name = []
	address = []
	name = []
	flag,count = 0,0
	for line in text1:
		temp = line.lower()
		wordss = temp.split(' ')

		words = []
		for word in wordss:
			word = word.replace(';',':')
			words.append(word)
		#print(words)
		
#(unique)###################### Name and Cleaning ####################
		nm = ['name','name:']
		for word in nm:
			if word in words:
				temp1 = temp.replace(word,'')
				temp1 = temp1.rstrip()
				temp1 = temp1.lstrip()
				temp1 = temp1.replace("8", "B")
				temp1 = temp1.replace("0", "D")
				temp1 = temp1.replace("6", "G")
				temp1 = temp1.replace("1", "I")
				temp1 = re.sub('[^a-zA-Z] +', ' ',temp1)
				name.append(temp1.upper())
		###############################################


#(unique)####### Name of Institute ########### Please add if remaining
		syn = ['college', 'institute', 'school', 'vidyalaya' , 'university', 'academy']
		for word in syn:
			if word in words:
				temp1 = line.rstrip()
				temp1 = temp1.lstrip()
				temp1 = temp1.replace("8", "B")
				temp1 = temp1.replace("0", "D")
				temp1 = temp1.replace("6", "G")
				temp1 = temp1.replace("1", "I")
				temp1 = re.sub('[^a-zA-Z] +', ' ',temp1)
				c_name.append(temp1)

#(multiple)	#################### Email Date Phone No. #################
		for word in words:
			
			## email for each line
			elst = re.findall(r'[\w\.-]+@[\w\.-]+',word)
			emails = list(set(emails + elst))


			## phone no. for each line
			plst = re.search(r'((\+*)((0[ -]+)*|(91 )*)(\d{12}|\d{10})| )|\d{5}([- ]*)\d{6}',word)
			if plst is not None:
				phn = word
				phn = phn.rstrip()
				phn = phn.lstrip()
				phn = phn.replace(" ", "")
				phones.append(phn)


#(multiple)	## Date in form of xx(./-)mm(./-)yyyy ###
			dlst = re.search('(\d{2})[/.-](\d{2})[/.-](\d{4})$', word)
			if dlst is not None:
				dob = word
				dob = dob.rstrip()
				dob = dob.lstrip()
				dob = dob.replace('l', '/')
				dob = dob.replace('L', '/')
				dob = dob.replace('I', '/')
				dob = dob.replace('i', '/')
				dob = dob.replace('|', '/')
				dob = dob.replace('\"', '/1')
				dob = dob.replace(" ", "")
				dates.append(dob)
		
		############################################################

#(multiple)	############### If address is given in proper format (3lines)########
		add = ['address', 'add', 'add.','address:', 'add:', 'add.:']
		for word in add:
			if word in words:
				flag = 1
		if (flag==1):
			count += 1
			address.append(line)
		if (count==3): flag=0
		################# 3 lines of proper format address #############
	

	######## Making Tuple of Data ##################
	#print ("These are the quantities can extract for every card")
	data = {}
	data['name'] = arr_to_str(name) 
	data['college'] = arr_to_str(c_name)
	data['dates'] = arr_to_str(dates)
	data['emails'] = arr_to_str(emails)
	data['phones'] =  arr_to_str(phones)
	data['address'] = arr_to_str(address)
	#print (data)
	# Writing data into JSON
	try:
		to_unicode = unicode
	except NameError:
		to_unicode = str

	# Write JSON file
	with open(cur_dir + '/Id_result/json/' +'res_{}.json'.format(base_name.split('.')[0]), 'w', encoding='utf-8') as outfile:
		str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
		outfile.write(to_unicode(str_))
