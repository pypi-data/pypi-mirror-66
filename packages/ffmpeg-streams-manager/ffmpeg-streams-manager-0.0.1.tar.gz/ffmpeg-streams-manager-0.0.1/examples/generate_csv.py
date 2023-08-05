from ffmpeg_streams_manager import *
from pathlib import Path
import csv

"""
sudo mount -t cifs -o username=username,password=password //192.168.1.10/series /mnt/series
"""
columns = [
    'video',
    'nb_streams',
    'nb_videos',
    'video_language',
    'video_codec',
    'nb_audios',
    'audio_language',
    'audio_codec',
    'nb_subtitles',
    'subtitle_language'
]

filename = 'output.csv'
with open(filename, 'w+', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(columns)

    for path in Path('/mnt/series').rglob('*'):
        if not path.is_dir():
            print(str(path))
            media = Media(str(path))

            video_codec = ''
            video_language = ''
            video_streams = media.get_video_streams()
            for stream in video_streams:
                video_codec += str(stream.codec)+', '
                video_language += str(stream.language)+', '

            audio_codec = ''
            audio_language = ''
            audio_streams = media.get_audio_streams()
            for stream in audio_streams:
                audio_codec += str(stream.codec)+', '
                audio_language += str(stream.language)+', '

            sub_language = ''
            sub_streams = media.get_subtitle_streams()
            for stream in sub_streams:
                sub_language += str(stream.language)+', '

            writer.writerow([
                str(path),
                len(media.get_streams()),
                len(video_streams),
                video_language,
                video_codec,
                len(audio_streams),
                audio_language,
                audio_codec,
                len(media.get_subtitle_streams()),
                sub_language,
            ])
f.close()
