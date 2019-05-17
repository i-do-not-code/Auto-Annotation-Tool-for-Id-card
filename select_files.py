import os
import shutil

current = os.getcwd()
Source = os.path.join(os.getcwd() + '/Source')
Output = os.path.join(os.getcwd() + '/Output/json/')
Working = os.path.join(os.getcwd() + '/Working')

####### Getting Source files ############
os.chdir(Source)
S_files = os.listdir()
Source_files = []
for file in S_files:
	f = file.split('.')[0]
	Source_files.append(f)
#print(Source_files)

########## Getting Output Files #####
os.chdir(Output)
O_files = os.listdir()
Output_files = []
for file in O_files:
	f = file.split('.')[0]
	f = f.split('_')[1]
	Output_files.append(f)
#print (Output_files) 

W_files = list(set(Source_files) - set(Output_files))
Working_files = []
for file in W_files:
	file = file + ".jpg"
	Working_files.append(file)
#print (Working_files)

for file in Working_files:
	source_path = Source+'/'+file
	target_path = Working+'/'+file
	shutil.copy(source_path, target_path)

