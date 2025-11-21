import yt_dlp
import os
import argparse
import logging

logging.basicConfig(
    format="%(level)s - %(message)s"
)

lg = logging.getLogger(__name__)

def dl_(url, output_path="downloads/"):
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    if "/sets/" in url:
        output_path += "playlists/"

    ffmpath = r"utils/ffmpeg.exe"
    output_path += "%(uploader)s - %(title)s.%(ext)s"

    opts = {
        "quiet": True,
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'ffmpeg_location': ffmpath,

        'embedthumbnail': True,

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

    except yt_dlp.DownloadError:
        lg.error("Download_error")
    except Exception as ex:
        lg.error(f"error: {ex}")

def main():
    pr = argparse.ArgumentParser()

    pr.add_argument(
        "url",
        nargs="?"
    )
    pr.add_argument(
        "-o", "--out_path",
        default=None
    )

    args = pr.parse_args()
    try:
        if not args.url:
            dl_(input())
            return

        if args.out_path:
            dl_(args.url, args.out_path)
            return
        dl_(args.url)
    except Exception as e:
        lg.error(e)

main()
