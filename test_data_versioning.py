import unittest
import os, time, zipfile
from urllib.request import urlretrieve


class TestObjectDetection(unittest.TestCase):

	def setUp(self):
		zip_url = 'https://segmind-data.s3.ap-south-1.amazonaws.com/edge/data/aerial-vehicles-dataset.zip'
		path_to_zip_file = '/tmp/aerial-vehicles-dataset.zip'
		directory_to_extract_to = '/tmp'
		urlretrieve(zip_url, path_to_zip_file)
		with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
			zip_ref.extractall(directory_to_extract_to)

	def test_directory_format_with_split(self):
		from cral.data_versioning import objectDetection_dataset_hasher
		train_img="/tmp/Aerial Object Detection/images"
		anno_yolo="/tmp/Aerial Object Detection/annotations/yolo_txt"
		anno_pascal="/tmp/Aerial Object Detection/annotations/pascalvoc_xml"
		hash_of_dataset = objectDetection_dataset_hasher(
			csv_dir="/tmp",
			train_images_dir=train_img, 
			train_anno_dir=anno_pascal, 
			anno_format='pascal', 
			val_images_dir=None, 
			val_anno_dir=None, 
			split=0.2)
		hash_of_dataset = objectDetection_dataset_hasher(
			csv_dir="/tmp",
			train_images_dir=train_img, 
			train_anno_dir=anno_yolo, 
			anno_format='yolo', 
			val_images_dir=None, 
			val_anno_dir=None, 
			split=0.2)

	def test_directory_format_with_val(self):
		from cral.data_versioning import objectDetection_dataset_hasher

		train_img="/tmp/Aerial Object Detection/images"
		anno_yolo="/tmp/Aerial Object Detection/annotations/yolo_txt"
		anno_pascal="/tmp/Aerial Object Detection/annotations/pascalvoc_xml"
		hash_of_dataset = objectDetection_dataset_hasher(
			csv_dir="/tmp",
			train_images_dir=train_img, 
			train_anno_dir=anno_pascal, 
			anno_format='pascal', 
			val_images_dir=train_img, 
			val_anno_dir=anno_pascal, 
			split=None)
		hash_of_dataset = objectDetection_dataset_hasher(
			csv_dir="/tmp",
			train_images_dir=train_img, 
			train_anno_dir=anno_yolo, 
			anno_format='yolo', 
			val_images_dir=train_img, 
			val_anno_dir=anno_yolo, 
			split=None)


if __name__ == '__main__':
	unittest.main()
