import csv
import glob
import os
import csv
from cral_hash import hashFile,hashStr
from cral_util import fileName,findImages
import random

def add_to_csv_path(csv_path,image_path,train,mode='w'):
	with open(csv_path,mode,newline='') as csv_file:
		csv_write=csv.writer(csv_file)
		for folder in os.listdir(image_path):
			new_folder=os.path.join(image_path+folder)
			new_folder+=os.sep
			class_name=folder
			for curr_img_path in findImages(new_folder):
				image_hs=hashFile(curr_img_path)
				csv_write.writerow([fileName(curr_img_path,True),image_hs,folder,hashStr(folder),train])

def add_to_csv_split(csv_path,image_path,split,mode='w'):
	with open(csv_path,mode,newline='') as csv_file:
		csv_write=csv.writer(csv_file)
		for folder in os.listdir(image_path):
			new_folder=os.path.join(image_path,folder)
			class_name=folder
			for curr_img_path in findImages(new_folder):
				enter=True
				image_hs=hashFile(curr_img_path)
				train=1
				if random.uniform(0,1)>split:
					train=0
				csv_write.writerow([fileName(curr_img_path,True),image_hs,folder,hashStr(folder),train])



def make_csv(csv_path,train_image,val_img=None,split=None):
	if (val_img is not None):
		add_to_csv_path(csv_path,train_image,1)
		add_to_csv_path(csv_path,val_img,0,'a')
	elif split is not None:
		add_to_csv_split(csv_path,train_image,split)
	else:
		add_to_csv_path(csv_path,train_image,1)

def find_classes(img_path):
	classes=[]
	for folder in os.listdir(img_path):
		new_folder=os.path.join(img_path+folder)
		new_folder+=os.sep
		class_name=folder
		if len(findImages(new_folder))>0 :
			classes.append(class_name)
	return classes

#testing
# csv_path="C:\\Users\\yadur\\Downloads\\Edge\\Dataset\\CSV\\test.csv"
# train_img="C:\\Users\\yadur\\Downloads\\Edge\\Dataset\\bikes_persons_dataset\\"
# val_img="C:\\Users\\yadur\\Downloads\\Edge\\Dataset\\bikes_persons_dataset - Copy\\"
# make_csv(csv_path,train_img,val_img,split=0.7)
# # print(find_classes(train_img))

