import pandas as pd
import numpy as np
import glob, os, tqdm
from cral_hash import hashFile,hashStr
from cral_util import fileName, find_images
import json
_ALLOWED_ANNOTATION_FORMATS=('coco','pascal','yolo')
_EXT={'pascal':'.xml','yolo':'.txt'}

def get_dataset_info(image_dir,anno_dir,anno_format,train_only=True):
	"""Parses the data and makes a pandas dataset
	
	Args:
		image_dir (str): path to image directory
		anno_dir (str): path to annotation directory or json file in coco
		anno_format (str): one of 'yolo','coco','pascal'
		train_only (bool, optional): True=Train ,False=Validation
	
	Returns:
		pandas_dataset: pandas dataset with information filled
	"""
	dataset_info = {"image_name":[], "annotation_name":[], "image_hash":[],"annotation_hash":[], "train_only":[]}
	if anno_format == 'coco' :

		with open(anno_dir) as anno_file:
			json_file=json.load(anno_file)
			anno_hs=hashFile(anno_dir)
			anno_name=fileName(anno_dir,ext=True)
			for image_data in tqdm.tqdm(json_file['images']) :
				image_name=image_data['file_name']
				image_path=os.path.join(image_dir,image_name)
				if os.path.isfile(image_path):
					dataset_info['image_name'].append(image_name)
					dataset_info['annotation_name'].append(anno_name)
					dataset_info['image_hash'].append(hashFile(image_path))
					dataset_info['annotation_hash'].append(anno_hs)
					dataset_info['train_only'].append(train_only)

	else:

		images = find_images(image_dir)

		for curr_image_path in tqdm.tqdm(images):
			curr_image_name=fileName(curr_image_path)
			curr_anno_path=os.path.join(anno_dir,curr_image_name+_EXT[anno_format])
		
			if os.path.isfile(curr_anno_path):
				dataset_info['image_name'].append(fileName(curr_image_path,ext=True))
				dataset_info['annotation_name'].append(fileName(curr_anno_path,ext=True))
				dataset_info['image_hash'].append(hashFile(curr_image_path))
				dataset_info['annotation_hash'].append(hashFile(curr_anno_path))
				dataset_info['train_only'].append(train_only)
		
	return dataset_info


def make_csv(csv_dir, train_images_dir, train_anno_dir, anno_format, val_images_dir=None, val_anno_dir=None, split=0.2):
	"""Parses the data and makes a csv file and returns its hash
	
	Args:
		csv_dir (str): path to save the CSV file created
		train_images_dir (str): path to images 
		train_anno_dir (str): path to annotation
		anno_format (str): one of 'yolo','coco','pascal'
		val_images_dir (str, optional): path to validation images
		val_anno_dir (str, optional): path to vallidation annotation
		split (float, optional): float to divide training dataset into traing and val
	
	Returns:
		str: Hash of the csv file created
	"""
	assert os.path.isdir(csv_dir), '{} is not a directory'.format(csv_dir)
	assert os.path.isdir(train_images_dir), '{} is not a directory'.format(train_images_dir)
	assert anno_format in _ALLOWED_ANNOTATION_FORMATS,"supported annotation formats are coco,pascal,yolo"
	if anno_format=='coco':
		assert os.path.isfile(train_anno_dir) and train_anno_dir.endswith('.json'), '{} is not a json file'.format(train_anno_dir)
	else:    
		assert os.path.isdir(train_anno_dir), '{} is not a directory'.format(train_anno_dir)
	
	if val_images_dir == None or val_anno_dir==None:
		assert 0<=split<=1.0, 'expected a float between 0 and 1, but got {} instead'.format(split)

	train_dataset_info = get_dataset_info(image_dir=train_images_dir,anno_dir=train_anno_dir,anno_format=anno_format)
	dataset_df = pd.DataFrame.from_dict(train_dataset_info)

	if val_images_dir and val_anno_dir:

		assert os.path.isdir(val_images_dir), '{} is not a directory'.format(val_images_dir)

		if anno_format=='coco':			
			assert os.path.isfile(val_anno_dir) and train_anno_dir.endswith('.json'), '{} is not a json file'.format(val_anno_dir)
		else:    
			assert os.path.isdir(val_anno_dir), '{} is not a directory'.format(val_anno_dir)

		val_dataset_info = get_dataset_info(image_dir=train_images_dir,anno_dir=train_anno_dir,anno_format=anno_format,train_only=False)
		val_df = pd.DataFrame.from_dict(val_dataset_info)

		dataset_df = pd.concat([dataset_df, val_df])
		#print(np.unique(dataset_df['train_only']))


	elif split>0:
		msk = np.random.randn(len(dataset_df)) < split
		dataset_df.loc[~msk,('train_only')] = False
		#print(np.unique(dataset_df['train_only']))

	dataset_save_path = os.path.join(csv_dir,'dataset.csv')
	dataset_df.to_csv(dataset_save_path , index=False)

	dataset_csv_hash = hashFile(dataset_save_path)

	return dataset_csv_hash




train_image="C:\\Users\\yadur\\Downloads\\Edge\\Dataset\\Aerial Object Detection\\images"
train_anno="C:\\Users\\yadur\\Downloads\\Edge\\Dataset\\Aerial Object Detection\\annotations\\pascalvoc_xml"
val_image="C:\\Users\\yadur\\Downloads\\Edge\\Dataset\\Aerial Object Detection - Copy\\images"
val_anno="C:\\Users\\yadur\\Downloads\\Edge\\Dataset\\Aerial Object Detection - Copy\\annotations\\pascalvoc_xml\\"
csv_path="C:\\Users\\yadur\\Downloads\\Edge\\Dataset"

make_csv(
	csv_path,
	train_image,
	train_anno,
	'pascal',
	val_images_dir=val_image,
	val_anno_dir=val_anno,
	split=None)

# def make_csv(csv_dir, train_images_dir,train_anno_dir, val_images_dir=None,val_anno_dir=None, split=0.2):
