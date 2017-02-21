import os
import json
import uuid
import shutil
from glob import glob
import soundfile as sf

PATH = os.getcwd() + '/TRAIN'
AUDIO_PATH = "kur_train/audio/"
TEXT_PATH = "kur_train/text/"
KUR_PATH = "kur_train/"

try:
	os.mkdir("kur_train")
	os.mkdir("kur_train/audio")
	os.mkdir("kur_train/text")
except:
	shutil.rmtree("kur_train", ignore_errors=True)
	os.mkdir("kur_train")
	os.mkdir("kur_train/audio")
	os.mkdir("kur_train/text")

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

# {"text": "words words words", "duration_s": 6.385, "uuid": "21737w03248347437203"}
files = {}
for x in os.walk(PATH):
	for txt in glob(os.path.join(x[0], '*.TXT')):
		base = txt.split(".")[0]
		GUID = uuid.uuid4()
		txt_file = base + ".TXT"
		wav_file = base + ".WAV"
		duration = get_duration(wav_file)
		text = get_text(txt_file)
		files[base] = [text, duration, GUID, txt_file, wav_file]


fjson = open(KUR_PATH + "TIMIT-TRAIN.jsonl", "wb")
for key, value in files.iteritems():
	text, duration, GUID, txt_src, wav_src = value
	txt_dst = TEXT_PATH + str(GUID) + ".TXT"
	wav_dst = AUDIO_PATH + str(GUID) + ".WAV"

	#Copy the Files
	shutil.copyfile(txt_src, txt_dst)
	shutil.copyfile(wav_src, wav_dst)

	#Write line to json file
	data = {}
	data['text'] = text
	data['duration_s'] = duration
	data['uuid'] = str(GUID)
	json_data = json.dumps(data)
	fjson.write(json_data + "\n")

fjson.close()


print("Converted to kur's expected speech format")

