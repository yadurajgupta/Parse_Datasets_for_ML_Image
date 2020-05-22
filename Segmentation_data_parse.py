import csv
import glob
import os
import csv
from cral_hash import hashFile
from cral_util import fileName,findImages
import random

def add_to_csv_path_pascal(csv_path,image_path,annotation_path,train,mode='w'):
	with open(csv_path,mode,newline='') as file_csv:
		csv_write=csv.writer(file_csv)
		for curr_image_path in findImages(image_path):
			name=fileName(curr_image_path)
			curr_annotation_path=annotation_path+name+'.png'
			image_hs=hashFile(curr_image_path)
			annotation_hs=hashFile(curr_annotation_path)
			# print(image_hs,annotation_hs)
			if(image_hs is not None) and (annotation_hs is not None):
				csv_write.writerow([fileName(curr_image_path,True),image_hs,fileName(curr_annotation_path,True),annotation_hs,train])

def add_to_csv_split_pascal(csv_path,image_path,annotation_path,train_split,mode='w'):
	with open(csv_path,mode,newline='') as file_csv:
		csv_write=csv.writer(file_csv)
		for curr_image_path in findImages(image_path):
			name=fileName(curr_image_path)
			curr_annotation_path=annotation_path+name+'.png'
			image_hs=hashFile(curr_image_path)
			annotation_hs=hashFile(curr_annotation_path)
			# print(image_hs,annotation_hs)
			train=1;
			if(random.uniform(0,1)>train_split):
				train=0;
			if(image_hs is not None) and (annotation_hs is not None):
				csv_write.writerow([fileName(curr_image_path,True),image_hs,fileName(curr_annotation_path,True),annotation_hs,train])


def add_to_csv_path_coco(csv_path,image_path,anno_path,train,mode='w'):
	with open(csv_path,mode,newline='') as csv_file:
		csv_write=csv.writer(csv_file)
		anno_hs=hashFile(anno_path)
		for curr_image_path in findImages(image_path):
			name=fileName(curr_image_path)
			image_hs=hashFile(curr_image_path)
			if(image_hs is not None) and (anno_hs is not None):
				csv_write.writerow([fileName(curr_image_path,True),image_hs,fileName(anno_path,True),anno_hs,train])

def add_to_csv_split_coco(csv_path,image_path,anno_path,annotation_format,split):
	with open(csv_path,mode,newline='') as csv_file:
		csv_write=csv.writer(csv_file)
		anno_hs=hashStr(anno_path)
		for curr_image_path in findImages(image_path):
			name=fileName(curr_image_path)
			image_hs=hashFile(curr_image_path)
			train=1
			if random.uniform(0,1)>split:
				train=0
			if(image_hs is not None) and (anno_hs is not None):
				csv_write.writerow([fileName(curr_image_path,True),image_hs,fileName(anno_path,True),anno_hs,train])


def make_csv(csv_path,train_image,train_annotation,annotation_format,val_img=None,val_annotation=None,split=None):
	if annotation_format=='pascal':
		if ((val_img is not None) and (val_annotation is not None)):
			add_to_csv_path_pascal(csv_path,train_image,train_annotation,1)
			add_to_csv_path_pascal(csv_path,val_img,val_annotation,0,'a')
		elif split is not None:
			add_to_csv_split_pascal(csv_path,train_image,train_annotation,split)
		else:
			add_to_csv_path_pascal(csv_path,train_image,train_annotation,1)
	elif annotation_format =='coco':
		if ((val_img is not None) and (val_annotation is not None)):
			add_to_csv_path_coco(csv_path,train_image,train_annotation,annotation_format,1)
			add_to_csv_path_coco(csv_path,val_img,val_annotation,annotation_format,0,'a')
		elif split is not None:
			add_to_csv_split_coco(csv_path,train_image,train_annotation,annotation_format,split)
		else:
			add_to_csv_path_coco(csv_path,train_image,train_annotation,annotation_format,1)

def find_classes_pascal(image_path,anno_path):
	classes=[]
	for curr_image_path in findImages(image_path):
		name=fileName(curr_image_path)
		curr_anno_path=anno_path+name+extention['pascal']
		tree = ET.parse(curr_anno_path)
		root = tree.getroot()
		for obj in root.iter('object'):
			for name in obj.iter('name'):
				if name.text not in classes:
					classes.append(name.text)
	return classes

def find_classes_coco(anno_path):
	classes=[]
	with open(anno_path) as file:
		data=json.load(file)
		for class_desc in data['categories']:
			class_name=class_desc['name']
			classes.append(class_name)
	return classes

csv_path="C:\\Users\\yadur\\Downloads\\Edge\\Dataset\\Aerial Object Detection\\CSV\\test.csv"
train_img="C:\\Users\\yadur\\Downloads\\Edge\\Dataset\\ADEChallengeData2016\\images\\training\\"
train_anno="C:\\Users\\yadur\\Downloads\\Edge\\Dataset\\ADEChallengeData2016\\annotations\\training\\"
val_img="C:\\Users\\yadur\\Downloads\\Edge\\Dataset\\ADEChallengeData2016\\annotations\\validation\\"
val_anno="C:\\Users\\yadur\\Downloads\\Edge\\Dataset\\ADEChallengeData2016\\annotations\\validation\\"
make_csv(csv_path,train_img,train_anno,'pascal',val_img,val_anno)