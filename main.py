from pytube import YouTube
from tqdm import tqdm
import requests
import os
import sys

from videos import courses


class YouTubeDownloader:
    def __init__(self, video_urls, download_path):
        self.video_urls = video_urls
        self.download_path = download_path

    def download_videos_with_progress(self):
        for video_url in self.video_urls:
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()
            total_size = stream.filesize

            response = requests.get(stream.url, stream=True)
            video_title = yt.title
            video_file_path = os.path.join(self.download_path, f"{video_title}.mp4")

            with open(video_file_path, 'wb') as output_file, tqdm(
                    unit='B', unit_scale=True, unit_divisor=1024,
                    total=int(response.headers.get('content-length', 0)), file=sys.stdout,
            ) as bar:
                for data in response.iter_content(1024):
                    output_file.write(data)
                    bar.update(len(data))

            print(f"Video '{video_title}' downloaded successfully.")


if __name__ == "__main__":
    for path, videos in courses.items():
        videos = videos
        download_path = path
        downloader = YouTubeDownloader(videos, download_path)
        downloader.download_videos_with_progress()
