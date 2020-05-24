import pandas as pd
import numpy as np
import glob, os, tqdm
from cral_hash import hashFile,hashStr
from cral_util import fileName, find_images

def get_dataset_info(file_dir, train_only=True):
	"""Parses the data and makes a pandas dataset
	
	Args:
		file_dir (str): path to folder with images
		train_only (bool, optional):  True=Train ,False=Validation 
	
	Returns:
		pandas_dataset: pandas dataset with information filled
	"""
	dataset_info = {"image_name":[], "annotation_name":[], "image_hash":[], "train_only":[]}

	for folder in os.listdir(file_dir) :
		class_images_path = os.path.join(file_dir, folder)
		#class_name=folder
		images = find_images(class_images_path)

		for image_location in tqdm.tqdm(images):
			image_name = os.path.basename(image_location)
			image_hs = hashFile(image_location)

			dataset_info['image_name'].append(image_name)
			dataset_info['annotation_name'].append(folder)
			dataset_info['image_hash'].append(image_hs)
			dataset_info['train_only'].append(train_only)

	return dataset_info

def make_csv(csv_dir, train_images_dir, val_images_dir=None, split=0.2):
	"""Parses the data and makes a csv file and returns its hash
	
	Args:
		csv_dir (str): path to save the CSV file created
		train_images_dir (str): path to images 
		val_images_dir (str, optional): path to validation images
		split (float, optional): float to divide training dataset into traing and validation
	
	Returns:
		str: Hash of the csv file created
	"""
	assert os.path.isdir(csv_dir), '{} is not a directory'.format(csv_dir)
	assert os.path.isdir(train_images_dir), '{} is not a directory'.format(train_images_dir)
	assert isinstance(split, float), 'expected to be float, but got {} instead'.format(type(split))

	if val_images_dir == None:
		assert 0<=split<=1.0, 'expected a float between 0 and 1, but got {} instead'.format(split)

	train_dataset_info = get_dataset_info(file_dir=train_images_dir)
	dataset_df = pd.DataFrame.from_dict(train_dataset_info)

	if val_images_dir:
		val_dataset_info = get_dataset_info(file_dir=val_images_dir, train_only=False)
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

