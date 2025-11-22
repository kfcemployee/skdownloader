import yt_dlp
import os
import argparse

def dl_(url, output_path="downloads/", is_pl=None, ffmpeg_path=None):
    if not output_path:
        output_path = "downloads/"

        if not os.path.exists(output_path):
            os.mkdir(output_path)

    if ("/sets/" in url) or is_pl:
        output_path += "playlists/"

    ffmpath: str = "ffmpeg.exe"
    if not ffmpeg_path:
        if os.path.exists("config.txt"):
            ffmpath = open("config.txt").readline().strip()
    else:
        ffmpath = ffmpeg_path
        with open('config.txt', "w") as f:
            f.write(ffmpeg_path)

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
        opts.pop("postprocessors")

        try:
            print("error with ffmpeg: trying to download without ffmpeg...")
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except yt_dlp.DownloadError:
            print("download error")

    except Exception as ex:
        print(f"error: {ex}")

    print("downloaded successfully")

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
    pr.add_argument(
        "-pl", "--playlist",
        action="store_true"
    )
    pr.add_argument(
        "-ff", "--ffmpeg_path",
        default=None
    )
    pr.add_argument(
        "-i", "--interactive",
        action="store_true"
    )

    args = pr.parse_args()

    if args.interactive or not any(vars(args).values()):
        interactive()
    else:
        try:
            opts = [args.url,
                args.out_path,
                args.playlist,
                args.ffmpeg_path]
            dl_(*opts)
        except Exception as e:
            print(e)

def interactive():
    while True:
        print(f"1. Скачать трек или плейлист.\n"
              f"2. Указать путь к ffmpeg.\n"
              f"3. Выйти.")

        ch = input("Введите команду...\n")
        match ch:
            case "1":
                url = input("Введите ссылку...\n")
                if url:
                    path = input("Введите путь для сохранения... (Enter для стандартного)\n")

                    if path:
                        dl_(url, output_path=path)
                    dl_(url)
            case "2":
                ff_path = input("Введите путь к ffmpeg...\n").strip()
                if ff_path and os.path.exists(ff_path):
                    with open('config.txt', "w") as f:
                        f.write(ff_path)
                    print(f"Путь к ffmpeg установлен: {ff_path}")
                else:
                    print("Некорректный файл")
            case "3":
                break


        input("\nНажмите Enter чтобы продолжить...")

main()