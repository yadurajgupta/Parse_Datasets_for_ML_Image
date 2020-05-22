import glob
import os
root_path=""
formats=["*.jpg","*.jepg","*.png"]

def fileName(file_path,ext=False):
	head,tail=os.path.split(file_path)
	if ext is False:
		file_name=".".join(tail.split('.')[:-1])
	else:
		file_name=tail
	return file_name

def findImages(path):
	if(path[-1]!=os.sep):
		path=path+os.sep;
	files=[]
	for format in formats:
		files.extend(glob.glob(path+format))
	return sorted(files)


