from os.path import exists
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
from blinkpy.helpers.util import json_load
from blinkpy.api import request_videos
from dateutil.parser import parse
from blinkpy.helpers.constants import (
    DEFAULT_MOTION_INTERVAL,
    DEFAULT_REFRESH,
    MIN_THROTTLE_TIME,
    TIMEOUT_MEDIA,
)

import json

TMP_PATH = "./tmp/"
AUTHFILE = "./auth.json"
MOST_RECENT_VIDEO_PATH = "./mostRecent.json"
HARD_PAGE_LIMIT = 10

mostRecentVideo = dict()



def download_latest_videos(blink,path,since="2021-12-20 12:00", stop=10, delay=1):
	parsed_datetime = parse(since, fuzzy=True)
	since_epochs = parsed_datetime.timestamp()
	
	for page in range(1, HARD_PAGE_LIMIT):
		response = request_videos(blink, time=since_epochs, page=page)
		try:
			result = response["media"]
			for item in result:
				for item in result:
					try:
						created_at = item["created_at"]
						camera_name = item["device_name"]
						is_deleted = item["deleted"]
						address = item["media"]
					except KeyError:
						continue
		            if not mostRecentVideo[camera_name]["has_been_updated"]:
						if mostRecentVideo[camera_name]["created_at"] < created_at:	
				            clip_address = f"{blink.urls.base_url}{address}"
				            filename = f"{camera_name}.mp4"
				            filename = os.path.join(path, filename)
			                response = api.http_get(
			                    self,
			                    url=clip_address,
			                    stream=True,
			                    json=False,
			                    timeout=TIMEOUT_MEDIA,
			                )
			                with open(filename, "wb") as vidfile:
			                    copyfileobj(response.raw, vidfile			
			



blink = Blink()

if exists(AUTHFILE):
	auth = Auth(json_load(AUTHFILE))
	blink.auth = auth
blink.start()
blink.save("./auth")

for name, camera in blink.cameras.items():
	mostRecentVideo["name"] = {"created_at":0, "has_been_updated":False}

download_latest_videos(blink, TMP_PATH)
	
