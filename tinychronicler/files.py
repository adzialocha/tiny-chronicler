import mimetypes
import os
import subprocess
import uuid

import aiofiles
from fastapi import File
from PIL import Image

from .constants import UPLOADS_DIR
from .helpers import temporary_file

CHUNK_SIZE_1MB = 1000 * 1000  # in bytes

THUMBNAIL_SIZE = 1600, 1600

ALLOWED_MIME_TYPES_AUDIO = ["audio/mpeg", "audio/x-wav"]
ALLOWED_MIME_TYPES_VIDEO = ["video/mp4", "video/mpeg"]
ALLOWED_MIME_TYPES_IMAGE = ["image/jpeg", "image/png"]

ALLOWED_MIME_TYPES = (
    ALLOWED_MIME_TYPES_IMAGE
    + ALLOWED_MIME_TYPES_VIDEO
    + ALLOWED_MIME_TYPES_AUDIO
)


def create_uploads_dir():
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)


def generate_file_name(file_ext: str):
    random_uuid = uuid.uuid4().hex
    file_name = "{}{}".format(random_uuid, file_ext)
    return file_name


def generate_videostill(video_file_path: str, img_file_path: str):
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            video_file_path,
            "-ss",
            "00:00:00.000",
            "-frames:v",
            "1",
            img_file_path,
        ],
        check=True,
    )


def generate_waveform(audio_file_path: str, img_file_path: str):
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            audio_file_path,
            "-filter_complex",
            "color=c=black[color];aformat=channel_layouts=mono,showwavespic=s=1600x1024:colors=white[wave];[color][wave]scale2ref[bg][fg];[bg][fg]overlay=format=auto",
            "-frames:v",
            "1",
            img_file_path,
        ],
        check=True,
    )


def generate_thumbnail(img_file_path: str):
    thumb_file_name = generate_file_name(".jpg")
    thumb_file_path = "{}/{}".format(UPLOADS_DIR, thumb_file_name)
    thumb_file_url = "/uploads/{}".format(thumb_file_name)

    with Image.open(img_file_path) as im:
        rgb_im = im.convert("RGB")
        rgb_im.thumbnail(THUMBNAIL_SIZE)
        rgb_im.save(thumb_file_path, "JPEG")

    return {
        "thumb_file_name": thumb_file_name,
        "thumb_file_path": thumb_file_path,
        "thumb_file_url": thumb_file_url,
    }


def thumbnail_from_file_type(file_path: str, file_mime: str):
    if file_mime in ALLOWED_MIME_TYPES_IMAGE:
        return generate_thumbnail(file_path)
    elif file_mime in ALLOWED_MIME_TYPES_VIDEO:
        with temporary_file(".jpg") as tmp_file_path:
            generate_videostill(file_path, tmp_file_path)
            return generate_thumbnail(tmp_file_path)
    elif file_mime in ALLOWED_MIME_TYPES_AUDIO:
        with temporary_file(".png") as tmp_file_path:
            generate_waveform(file_path, tmp_file_path)
            return generate_thumbnail(tmp_file_path)
    else:
        raise Exception("Cant process unknow file type")


async def store_file(file: File):
    # Generate new file name and destination
    file_mime = file.content_type
    file_ext = mimetypes.guess_extension(file_mime)
    file_name = generate_file_name(file_ext)
    file_path = "{}/{}".format(UPLOADS_DIR, file_name)
    file_url = "/uploads/{}".format(file_name)

    # Write file in chunks to not put too much pressure on memory
    async with aiofiles.open(file_path, "wb") as out_file:
        while content := await file.read(CHUNK_SIZE_1MB):
            await out_file.write(content)

    # Generate thumbnails after uploading files
    thumb = thumbnail_from_file_type(file_path, file_mime)

    return {
        "file_name": file_name,
        "file_path": file_path,
        "file_mime": file_mime,
        "file_url": file_url,
        "thumb_name": thumb["thumb_file_name"],
        "thumb_path": thumb["thumb_file_path"],
        "thumb_url": thumb["thumb_file_url"],
    }


def remove_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
