import xxhash
import glob
import os
BUFF_SIZE=65536
def hash_file(file_path,hs):
	head, file_name = os.path.split(file_path)
	hs.update(file_name.encode())
	with open(file_path,encoding='Latin-1') as file:
		while True:
			data=file.read(BUFF_SIZE)
			if not data:
				break
			data=data.encode()
			hs.update(data)
		print(file_name,hs.hexdigest())

def hash_all(root_path):
	hs=xxhash.xxh64()
	files=[]
	for format in formats:
		files.extend(glob.glob(root_path+format))
	for f in sorted(files):
		hash_file(f,hs)
	return hs

def hashFile(file_path):
	with open(file_path,encoding='Latin-1') as file:
		hs=xxhash.xxh32()
		while True:
			data=file.read(BUFF_SIZE)
			if not data:
				break
			data=data.encode()
			hs.update(data)
		return hs.hexdigest()
	return None;

def hashStr(str):
	return xxhash.xxh32(str.encode()).hexdigest()