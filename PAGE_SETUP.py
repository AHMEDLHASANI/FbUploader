from requests import get
from os import mkdir

url = "https://graph.facebook.com/v13.0/me"

cfg = """
###### DO NOT DELETE THIS FILE ######

use_ffmpeg = True


access_token = "{0}"
'''
    title         :    title of youtube video.
    author        :    channel name.
    views         :    video views count.
    publish_date  :    publish date of the video.
    watch_url     :    video url.
    size          :    video size.
    height        :    video height.
    width         :    video width.
'''
title = "<title>"
description = '''
🖋 : <title>
👤 : <author>
👁‍🗨 : <views>
🗓️ : <publish_date>
↗️️ : <watch_url>


POSTED IN <upload_date> BY OUR BOT.
'''
"""
while True:
    access_token = input("Access token: ")
    data = {"access_token": access_token, "fields": "name"}
    print("sending")
    res = get(url, params=data)
    print(res.text)
    if res.ok:

        id = res.json()["id"]
        name = res.json()["name"]
        print(f"name : {name}\nid : {id}")
        try:
            mkdir(id)
            open(f"{id}/CONFIG.py", "a").write(cfg.format(access_token))
        except FileExistsError:
            open(f"{id}/CONFIG.py", "a").write(cfg.format(access_token))
        break
