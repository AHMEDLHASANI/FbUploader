from pytube import YouTube, Playlist, Channel
from utils import DescriptionMaker
from requests import post
from os import system
import argparse
import datetime
import time

parser = argparse.ArgumentParser(description="List the content of a folder")
parser.add_argument("page", metavar="Page", type=str, help="Page Id")
parser.add_argument(
    "-c", metavar="https://youtube.com/c/Channel", type=str, help="Channel Url To Upload From It", nargs="+"
)
parser.add_argument(
    "-p", metavar="p",metavars=[6,8,6], type=str, help="PlayList Url To Upload From It", nargs="+"
)
parser.add_argument(
    "-v", metavar="v", type=str, help="Video Url To Upload", nargs="+"
)
parser.add_argument("--ffmpeg", action="store_true")
parser.add_argument("--no-ffmpeg", dest="feature", action="store_false")
parser.set_defaults(feature=True)
parser.add_argument("-o", type=str, help="File To Save links")
# Execute the parse_args() method
args = parser.parse_args()
print(args.ffmpeg)
page = args.page
output_file = args.o
Channels = args.c
Playlists = args.p
Videos = args.v


class Uploader:
    def __init__(self, page, c, p, v):
        self.page = page
        self.c = c
        self.p = p
        self.v = v

    def extract_links(self) -> tuple:
        FinalList = []
        try:
            for F, V in zip([Channel, Playlist], [self.c, self.p]):
                for _ in V:
                    try:
                        FinalList.extend(list(F(_)))
                    except:
                        print(f"ERROR ({F.__name__}): While Extract Links From {_}")
        except:
            pass
        FinalList.extend(self.v)
        print(FinalList)
        return FinalList

    def get_best_res(self, url):
        vid = YouTube(url)
        for res in __import__(f"{self.page}.CONFIG").CONFIG.resolutions:
            Filtered1 = vid.streams.filter(progressive=True, res=res)
            Filtered2 = vid.streams.filter(progressive=False, res=res)
            if Filtered1 or Filtered2:
                return Filtered1 or Filtered2, vid

    def make_desc(self, video):
        print(dir(video))
        desc = {
            "<title>": video.title,
            "<author>": video.author,
            "<views>": video.views,
            "<publish_date>": video.publish_date,
            "<watch_url>": video.watch_url,
            "<upload_date>": str(datetime.datetime.now())[:16],
        }
        title = video.title
        return desc, title

    def download_video(self, video):
        video.download(filename=f"{self.page}/current_video.mp4"
        try:
	    print("trying")
            #video.download(filename=f"{self.page}/current_video.mp4")
        except:
            print(f"ERROR (Downloading): While Downloading {video.title}")
            return False
        else:
            return f"{self.page}/current_video.mp4"

    def compress_video(self, path, url):
        print(f"Start Compressing {url}")
        system(
            f"ffmpeg -i {self.page}/current_video.mp4 -vcodec h264 -acodec aac {self.page}/new_current_video.mp4"
        )
        return f"{self.page}/new_current_video.mp4"

    def upload_video(self, path, title, description, url):
        files = {"source": open(path, "rb")}
        payload = {
            "access_token": __import__(f"{self.page}.CONFIG").CONFIG.access_token,
            "title": title,
            "description": description,
        }
        try:
            print(f"start Uploading {url}")
            res = post(
                "https://graph-video.facebook.com/v13.0/me/videos",
                files=files,
                data=payload,
            )
        except:
            print(f"ERROR (Uploading): While Uploading {url}")
            system(f"rm path")
            system(f"rm {self.page}/new_current_video.mp4")
            time.sleep(60 * 5)
        else:
            id = res.json()["id"]
            if id:
                print(f"Successfully (Uploading): Uploading {url}")
                print(f"https://facebook.com/{id}")
                with open(f"{self.page}/{output_file}", "a") as SaveLinks:
                    SaveLinks.write(f"\n{title} :\nhttps://facebook.com/{id}")
                return True
            else:
                print(f"Failed (Uploading) : Uploading {url}")
                print(res.text)
                return False


Uploader = Uploader(page, Channels, Playlists, Videos)


def main():
    for link in Uploader.extract_links():
        target = Uploader.get_best_res(link)
        vid = Uploader.download_video(target[0][0])
        if vid:
            if args.ffmpeg:
                path = Uploader.compress_video(vid, link)
            else:
                path = f"{args.page}/current_video.mp4"
            desc_and_title = Uploader.make_desc(target[1])
            if Uploader.upload_video(
                path,
                desc_and_title[1],
                DescriptionMaker(
                    __import__(f"{args.page}.CONFIG").CONFIG.description,
                    desc_and_title[0],
                ),
                link,
            ):
                time.sleep(10 * 60)


if __name__ == "__main__":
    main()
