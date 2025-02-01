import yt_dlp
import requests
import re
import vk_api
from vk_api.utils import get_random_id
import time
import os 
from youtubers import youtubers_list

VK_TOKEN = os.getenv(TOKEN_VK) #также токен можно указать напрямую в файле VK_TOKEN = "ваш_токен"
vk_session = vk_api.VkApi(token=VK_TOKEN)
upload = vk_api.VkUpload(vk_session)
vk = vk_session.get_api()
script_dir = os.path.dirname(os.path.abspath(__file__))

# user_id = заменить на ваш айди в вк  
user_id = os.getenv(USER_ID) #аналогично можно указать напрямую в файле как и токен

def get_url(youtuber) -> str:
            html = requests.get(f"https://www.youtube.com/@{youtuber}/videos").text
            print("проверяем последнее видео")
            URL = (
                "https://www.youtube.com/watch?v="
                + re.search('(?<="videoId":").*?(?=")', html).group()
            )
            return URL

ydl_opts = {
    "format": "bestvideo+bestaudio/best",
    "concurrent-fragments": "4",
    "outtmpl": "video.%(ext)s",
    "ignoreerrors": True,
    "no-overwrites": True,
    "continue": True,
    "writethumbnail": True,
    "embedthumbnail": True,
    "convert-thumbnails": "jpg",
    "postprocessors": [
        {
            "format": "jpg",
            "key": "FFmpegThumbnailsConvertor",
            "when": "before_dl",
        }
    ],
}

def download_video(URL):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(URL, download=True)
            video_channel = info_dict.get("channel", None)
            video_title = info_dict.get("title", None)
            video_format = info_dict.get("ext", None)
            video_name = f"[{video_channel}] {video_title}"
            file_name = f"video.{video_format}"
        except:
            vk.messages.send(
                user_id=user_id,
                random_id=get_random_id(),
                message=f"ОШИБКА! ВИДЕО {video_name} СКАЧАТЬ НЕ УДАЛОСЬ",
            )
    print("загрузка видео в вк")
    response = upload.video(
        video_file=file_name,
        name=video_name,
        group_id=youtuber.group_id,
        album_id=youtuber.pl_id,
        wallpost="1",
    )
    print("загрузка обложки")
    video_id = response.get("video_id")
    response = upload.thumb_video(
        photo_path=script_dir+"/video.jpg",
        owner_id=f"-{group_id}",
        video_id=video_id,
    )
    vk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        message=f"Видео {video_name} успешно загружено в группу",
    )
    file.write(URL + "\n")
    os.remove(file_name)
    os.remove("video.jpg")



while True:
    try:
        for youtuber in youtubers_list:
            URL = get_url(youtuber)
            with open("downloaded.txt", "r+") as file:
                content = file.read()
                if URL not in content:
                    download_video(URL)
        print("перерыв 10 минут")
        time.sleep(10 * 60)
    except:
        vk.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            message="Программа завершена из-за ошибки. Перезапустите скрипт.",
        )
        break
