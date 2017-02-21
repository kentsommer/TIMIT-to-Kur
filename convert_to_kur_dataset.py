import os
import json
import uuid
import shutil
from glob import glob
from tqdm import tqdm
import soundfile as sf

# Train Paths
TRAIN_PATH = os.getcwd() + '/TRAIN'
TRAIN_AUDIO_PATH = "timit_train/audio/"
TRAIN_TEXT_PATH = "timit_train/text/"
TRAIN_KUR_PATH = "timit_train/"

# Test Paths
TEST_PATH = os.getcwd() + '/TEST'
TEST_AUDIO_PATH = "timit_test/audio/"
TEST_TEXT_PATH = "timit_test/text/"
TEST_KUR_PATH = "timit_test/"

def update_dirs():
	try:
		# Make Training Trees
		os.mkdir("timit_train")
		os.mkdir("timit_train/audio")
		os.mkdir("timit_train/text")
		# Make Testing Trees
		os.mkdir("timit_test")
		os.mkdir("timit_test/audio")
		os.mkdir("timit_test/text")
	except:
		#RM Training and Testing Trees
		shutil.rmtree("timit_train", ignore_errors=True)
		shutil.rmtree("timit_test", ignore_errors=True)
		# Make Training Trees
		os.mkdir("timit_train")
		os.mkdir("timit_train/audio")
		os.mkdir("timit_train/text")
		# Make Testing Trees
		os.mkdir("timit_test")
		os.mkdir("timit_test/audio")
		os.mkdir("timit_test/text")

def get_duration(wav_file):
	f = sf.SoundFile(wav_file)
	seconds = (len(f) * 1.0) / f.samplerate
	print('seconds = {}'.format(seconds))
	f.close()
	return seconds

def get_text(txt_file):
	ftxt = open(txt_file, "rb")
	line = ftxt.readline().strip("\n")
	line = line.replace(".", "")
	line = line.replace(",", "")
	line = line.replace("?", "")
	line = line.replace(":", "")
	result = " ".join(line.split(" ")[2:])
	print(result)
	ftxt.close()
	return result

def convert_train():
	files = {}
	for x in os.walk(TRAIN_PATH):
		for txt in glob(os.path.join(x[0], '*.TXT')):
			base = txt.split(".")[0]
			GUID = uuid.uuid4()
			txt_file = base + ".TXT"
			wav_file = base + ".WAV"
			duration = get_duration(wav_file)
			text = get_text(txt_file)
			files[base] = [text, duration, GUID, txt_file, wav_file]


	fjson = open(TRAIN_KUR_PATH + "timit_train.jsonl", "wb")
	for key, value in tqdm(files.iteritems()):
		text, duration, GUID, txt_src, wav_src = value
		txt_dst = TRAIN_TEXT_PATH + str(GUID) + ".txt"
		wav_dst = TRAIN_AUDIO_PATH + str(GUID) + ".wav"

		#Copy the Files
		shutil.copyfile(txt_src, txt_dst)
		data, samplerate = sf.read(wav_src)
		sf.write(wav_dst, data, samplerate)
		# shutil.copyfile(wav_src, wav_dst)

		#Write line to json file
		data = {}
		data['text'] = text
		data['duration_s'] = duration
		data['uuid'] = str(GUID)
		json_data = json.dumps(data)
		fjson.write(json_data + "\n")

	fjson.close()

def convert_test():
	files = {}
	for x in os.walk(TEST_PATH):
		for txt in glob(os.path.join(x[0], '*.TXT')):
			base = txt.split(".")[0]
			GUID = uuid.uuid4()
			txt_file = base + ".TXT"
			wav_file = base + ".WAV"
			duration = get_duration(wav_file)
			text = get_text(txt_file)
			files[base] = [text, duration, GUID, txt_file, wav_file]


	fjson = open(TEST_KUR_PATH + "timit_test.jsonl", "wb")
	for key, value in tqdm(files.iteritems()):
		text, duration, GUID, txt_src, wav_src = value
		txt_dst = TEST_TEXT_PATH + str(GUID) + ".txt"
		wav_dst = TEST_AUDIO_PATH + str(GUID) + ".wav"

		#Copy the Files
		shutil.copyfile(txt_src, txt_dst)
		data, samplerate = sf.read(wav_src)
		sf.write(wav_dst, data, samplerate)
		# shutil.copyfile(wav_src, wav_dst)

		#Write line to json file
		data = {}
		data['text'] = text
		data['duration_s'] = duration
		data['uuid'] = str(GUID)
		json_data = json.dumps(data)
		fjson.write(json_data + "\n")

	fjson.close()


if __name__ == '__main__':
	update_dirs()
	convert_train()
	convert_test()
	print("Converted to kur's expected speech format")

