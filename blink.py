from os.path import exists, isfile, join
from os import listdir
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
from blinkpy.helpers.util import json_load
from blinkpy.api import request_videos,http_get
from dateutil.parser import parse
from shutil import copyfileobj
from blinkpy.helpers.constants import (
    DEFAULT_MOTION_INTERVAL,
    DEFAULT_REFRESH,
    MIN_THROTTLE_TIME,
    TIMEOUT_MEDIA,
)

import json
import os.path

TMP_PATH = "./tmp/"
CURRRENT_PATH = "./current/"
AUTHFILE = "./auth.json"
HARD_PAGE_LIMIT = 2


def get_date_for_most_recent_by_camera_media_file(blink, path=CURRRENT_PATH):
	most_recent = dict()
	onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
	for file in onlyfiles:
		file = file.strip(".mp4").split("+")
		camera_name = file[0]
		created_at = file[1]
		most_recent[camera_name] = created_at
	for name, camera in blink.cameras.items():
		if name not in most_recent:
			most_recent[name] = "1970-01-01T12:00:00"
	return most_recent

		

def download_latest_videos(blink,path,since="1970-01-01 12:00"):
	parsed_datetime = parse(since, fuzzy=True)
	since_epochs = parsed_datetime.timestamp()
	mostRecentVideo = get_date_for_most_recent_by_camera_media_file(blink)
	downloaded = 0
	
	for page in range(1, HARD_PAGE_LIMIT):
		response = request_videos(blink, time=since_epochs, page=page)
		try:
			result = response["media"]
			for item in result:
				try:
					created_at = item["created_at"]
					camera_name = item["device_name"]
					is_deleted = item["deleted"]
					address = item["media"]
				except KeyError:
					continue
				if parse(created_at, fuzzy=True).timestamp() > parse(mostRecentVideo[camera_name], fuzzy=True).timestamp():
					mostRecentVideo[camera_name] = created_at
					print('Downloading')
					clip_address = f"{blink.urls.base_url}{address}"
					filename = f"{camera_name}+{created_at}.mp4"
					filename = os.path.join(path, filename)
					response = http_get(
					blink,
					url=clip_address,
					stream=True,
					json=False,
					timeout=TIMEOUT_MEDIA,
					)
					with open(filename, "wb") as vidfile:
						copyfileobj(response.raw, vidfile)
					downloaded+=1

				else:
					print("Skipping")
			if downloaded == len(mostRecentVideo):
				break
					

		except RuntimeError:
			continue			
			



blink = Blink()

if exists(AUTHFILE):
	auth = Auth(json_load(AUTHFILE))
	blink.auth = auth
blink.start()
blink.save(AUTHFILE)

download_latest_videos(blink, TMP_PATH)
