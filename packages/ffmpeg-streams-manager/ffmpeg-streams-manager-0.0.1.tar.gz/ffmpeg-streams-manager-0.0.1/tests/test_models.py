import unittest
from ffmpeg.nodes import FilterableStream, OutputStream
from ffmpeg_streams_manager import *
from pathlib import Path


class TestConverter(unittest.TestCase):
    def test_init(self):
        input = Input('fixtures/sintel-multi.mkv')
        converter = Converter('file.mkv')
        converter.add_input(input)
        self.assertEqual(
            converter.get_ffmpeg_output().get_args(),
            [
                '-i',
                'fixtures/sintel-multi.mkv',
                '-map',
                '0:0',
                '-map',
                '0:1',
                '-map',
                '0:2',
                '-map',
                '0:3',
                '-metadata:s:a:0',
                'language=eng',
                '-metadata:s:s:0',
                'language=eng',
                '-metadata:s:s:1',
                'language=es',
                '-metadata:s:v:0',
                'language=eng',
                'file.mkv'
             ]
        )

    def test_clean_inputs_metadata(self):
        input = Input('fixtures/sintel-multi.mkv')
        converter = Converter('file.mkv')
        converter.add_input(input)
        converter.clean_inputs_metadata()
        self.assertIn('-map_metadata', converter.get_ffmpeg_output().get_args())

    def test_no_metadata(self):
        input = Input('fixtures/sintel-multi.mkv')
        # No metadata in MP4 files
        converter = Converter('file.mp4')
        converter.add_input(input)
        self.assertEqual(
            converter.get_ffmpeg_output().get_args(),
            [
                '-i',
                'fixtures/sintel-multi.mkv',
                '-map',
                '0:0',
                '-map',
                '0:1',
                '-map',
                '0:2',
                '-map',
                '0:3',
                'file.mp4'
            ]
        )

    def test_add_input(self):
        input1 = Input('fixtures/sintel.mp4')
        input2 = Input('fixtures/en.srt')
        input3 = Input('fixtures/es.srt')
        converter = Converter('file.mkv')
        converter.add_input(input1)
        converter.add_input(input2)
        converter.add_input(input3)

        self.assertEqual(
            converter.get_ffmpeg_output().get_args(),
            [
                '-i',
                'fixtures/sintel.mp4',
                '-i',
                'fixtures/en.srt',
                '-i',
                'fixtures/es.srt',
                '-map',
                '0:0',
                '-map',
                '0:1',
                '-map',
                '1:0',
                '-map',
                '2:0',
                '-metadata:s:a:0',
                'language=eng',
                '-metadata:s:s:0',
                'language=und',
                '-metadata:s:s:1',
                'language=und',
                '-metadata:s:v:0',
                'language=und',
                'file.mkv'
            ]
        )

    def test_add_language(self):
        input1 = Input('fixtures/sintel.mp4')
        input2 = Input('fixtures/en.srt')
        input2.get_media().get_subtitle_streams()[0].language = 'eng'

        converter = Converter('file.mkv')
        converter.add_input(input1)
        converter.add_input(input2)

        self.assertEqual(
            converter.get_ffmpeg_output().get_args(),
            [
                '-i',
                'fixtures/sintel.mp4',
                '-i',
                'fixtures/en.srt',
                '-map',
                '0:0',
                '-map',
                '0:1',
                '-map',
                '1:0',
                '-metadata:s:a:0',
                'language=eng',
                '-metadata:s:s:0',
                'language=eng',
                '-metadata:s:v:0',
                'language=und',
                'file.mkv'
            ]
        )

    def test_get_final_streams(self):
        input1 = Input('fixtures/sintel.mp4')
        input2 = Input('fixtures/en.srt')
        input3 = Input('fixtures/es.srt')

        converter = Converter('file.mkv')
        converter.add_input(input1)
        converter.add_input(input2)
        converter.add_input(input3)

        streams = converter.get_final_streams()

        self.assertIsInstance(streams[0], VideoStream)
        self.assertEqual(streams[0].language, 'und')
        self.assertEqual(streams[0].codec, 'h264')
        self.assertEqual(streams[0].map, 0)

        self.assertIsInstance(streams[1], AudioStream)
        self.assertEqual(streams[1].language, 'eng')
        self.assertEqual(streams[1].codec, 'aac')
        self.assertEqual(streams[1].map, 1)

        self.assertIsInstance(streams[2], SubtitleStream)
        self.assertEqual(streams[2].language, 'und')
        self.assertEqual(streams[2].codec, 'subrip')
        self.assertEqual(streams[2].map, 0)

        self.assertIsInstance(streams[3], SubtitleStream)
        self.assertEqual(streams[3].language, 'und')
        self.assertEqual(streams[3].codec, 'subrip')
        self.assertEqual(streams[3].map, 0)

    def test_get_final_video_streams(self):
        input1 = Input('fixtures/sintel.mp4')
        input2 = Input('fixtures/en.srt')
        input3 = Input('fixtures/es.srt')

        converter = Converter('file.mkv')
        converter.add_input(input1)
        converter.add_input(input2)
        converter.add_input(input3)

        streams = converter.get_final_video_streams()
        self.assertEqual(len(streams), 1)

    def test_get_final_audio_streams(self):
        input1 = Input('fixtures/sintel.mp4')
        input2 = Input('fixtures/en.srt')
        input3 = Input('fixtures/es.srt')
        input4 = Input('fixtures/music.mp3')

        converter = Converter('file.mkv')
        converter.add_input(input1)
        converter.add_input(input2)
        converter.add_input(input3)
        converter.add_input(input4)

        streams = converter.get_final_audio_streams()
        self.assertEqual(len(streams), 2)

    def test_get_final_subtitle_streams(self):
        input1 = Input('fixtures/sintel.mp4')
        input2 = Input('fixtures/en.srt')
        input3 = Input('fixtures/es.srt')

        converter = Converter('file.mkv')
        converter.add_input(input1)
        converter.add_input(input2)
        converter.add_input(input3)

        streams = converter.get_final_subtitle_streams()
        self.assertEqual(len(streams), 2)

    def test_get_ffmpeg_output(self):
        input1 = Input('fixtures/sintel.mp4')
        input2 = Input('fixtures/en.srt')
        input3 = Input('fixtures/es.srt')

        converter = Converter('file.mkv')
        converter.add_input(input1)
        converter.add_input(input2)
        converter.add_input(input3)

        self.assertIsInstance(converter.get_ffmpeg_output(), OutputStream)

    def test_debug(self):
        input1 = Input('fixtures/sintel.mp4')
        input2 = Input('fixtures/en.srt')
        input3 = Input('fixtures/es.srt')

        converter = Converter('file.mkv')
        converter.add_input(input1)
        converter.add_input(input2)
        converter.add_input(input3)
        converter.debug()

    def test_run(self):
        input = Input('fixtures/sintel.mp4')
        converter = Converter('fixtures/output.mp4')
        converter.add_input(input)
        converter.run()
        converter.__repr__()


class TestH265Converter(unittest.TestCase):
    def test_init(self):
        input = Input('fixtures/sintel-multi.mkv')
        converter = H265Converter('file.mkv')
        converter.add_input(input)
        self.assertIn('hevc', converter.get_ffmpeg_output().get_args())


class TestH264Converter(unittest.TestCase):
    def test_init(self):
        input = Input('fixtures/sintel-multi.mkv')
        converter = H264Converter('file.mkv')
        converter.add_input(input)
        self.assertIn('h264', converter.get_ffmpeg_output().get_args())


class TestInput(unittest.TestCase):
    def test_init(self):
        input = Input('fixtures/sintel-multi.mkv')
        self.assertIsInstance(input.get_media(), Media)
        self.assertIsInstance(input.get_ffmpeg_input(), FilterableStream)
        self.assertEqual(input.get_final_maps(), [0, 1, 2, 3])

        streams = input.get_final_streams()

        self.assertIsInstance(streams[0], VideoStream)
        self.assertEqual(streams[0].language, 'eng')
        self.assertEqual(streams[0].codec, 'h264')
        self.assertEqual(streams[0].map, 0)

        self.assertIsInstance(streams[1], AudioStream)
        self.assertEqual(streams[1].language, 'eng')
        self.assertEqual(streams[1].codec, 'vorbis')
        self.assertEqual(streams[1].map, 1)

        self.assertIsInstance(streams[2], SubtitleStream)
        self.assertEqual(streams[2].language, 'eng')
        self.assertEqual(streams[2].codec, 'ass')
        self.assertEqual(streams[2].map, 2)

        self.assertIsInstance(streams[3], SubtitleStream)
        self.assertEqual(streams[3].language, 'es')
        self.assertEqual(streams[3].codec, 'ass')
        self.assertEqual(streams[3].map, 3)

    def test_mapping_language(self):
        input = Input('fixtures/sintel-multi.mkv', ['eng'])
        self.assertEqual(input.get_final_maps(), [0, 1, 2])

        streams = input.get_final_streams()

        self.assertIsInstance(streams[0], VideoStream)
        self.assertEqual(streams[0].language, 'eng')
        self.assertEqual(streams[0].codec, 'h264')
        self.assertEqual(streams[0].map, 0)

        self.assertIsInstance(streams[1], AudioStream)
        self.assertEqual(streams[1].language, 'eng')
        self.assertEqual(streams[1].codec, 'vorbis')
        self.assertEqual(streams[1].map, 1)

        self.assertIsInstance(streams[2], SubtitleStream)
        self.assertEqual(streams[2].language, 'eng')
        self.assertEqual(streams[2].codec, 'ass')
        self.assertEqual(streams[2].map, 2)

    def test_mapping_maps(self):
        input = Input('fixtures/sintel-multi.mkv', [0, 3])
        self.assertEqual(input.get_final_maps(), [0, 3])

        streams = input.get_final_streams()

        self.assertIsInstance(streams[0], VideoStream)
        self.assertEqual(streams[0].language, 'eng')
        self.assertEqual(streams[0].codec, 'h264')
        self.assertEqual(streams[0].map, 0)

        self.assertIsInstance(streams[1], SubtitleStream)
        self.assertEqual(streams[1].language, 'es')
        self.assertEqual(streams[1].codec, 'ass')
        self.assertEqual(streams[1].map, 3)

    def test_mapping_type(self):
        input = Input('fixtures/sintel-multi.mkv', ['subtitle', 'v', 'sound'])
        self.assertEqual(input.get_final_maps(), [0, 1, 2, 3])

        streams = input.get_final_streams()

        self.assertIsInstance(streams[0], VideoStream)
        self.assertEqual(streams[0].language, 'eng')
        self.assertEqual(streams[0].codec, 'h264')
        self.assertEqual(streams[0].map, 0)

        self.assertIsInstance(streams[1], AudioStream)
        self.assertEqual(streams[1].language, 'eng')
        self.assertEqual(streams[1].codec, 'vorbis')
        self.assertEqual(streams[1].map, 1)

        self.assertIsInstance(streams[2], SubtitleStream)
        self.assertEqual(streams[2].language, 'eng')
        self.assertEqual(streams[2].codec, 'ass')
        self.assertEqual(streams[2].map, 2)

        self.assertIsInstance(streams[3], SubtitleStream)
        self.assertEqual(streams[3].language, 'es')
        self.assertEqual(streams[3].codec, 'ass')
        self.assertEqual(streams[3].map, 3)

    def test_mapping_mixes(self):
        input = Input('fixtures/sintel-multi.mkv', ['sub', 'eng', 3])
        self.assertEqual(input.get_final_maps(), [0, 1, 2, 3])

        streams = input.get_final_streams()

        self.assertIsInstance(streams[0], VideoStream)
        self.assertEqual(streams[0].language, 'eng')
        self.assertEqual(streams[0].codec, 'h264')
        self.assertEqual(streams[0].map, 0)

        self.assertIsInstance(streams[1], AudioStream)
        self.assertEqual(streams[1].language, 'eng')
        self.assertEqual(streams[1].codec, 'vorbis')
        self.assertEqual(streams[1].map, 1)

        self.assertIsInstance(streams[2], SubtitleStream)
        self.assertEqual(streams[2].language, 'eng')
        self.assertEqual(streams[2].codec, 'ass')
        self.assertEqual(streams[2].map, 2)

        self.assertIsInstance(streams[3], SubtitleStream)
        self.assertEqual(streams[3].language, 'es')
        self.assertEqual(streams[3].codec, 'ass')
        self.assertEqual(streams[3].map, 3)

    def test_mapping_complex_filter(self):
        input = Input('fixtures/sintel-multi.mkv', ['s:es', 'v:eng:0'])
        self.assertEqual(input.get_final_maps(), [0, 3])
        streams = input.get_final_streams()

        self.assertIsInstance(streams[0], VideoStream)
        self.assertEqual(streams[0].language, 'eng')
        self.assertEqual(streams[0].codec, 'h264')
        self.assertEqual(streams[0].map, 0)

        self.assertIsInstance(streams[1], SubtitleStream)
        self.assertEqual(streams[1].language, 'es')
        self.assertEqual(streams[1].codec, 'ass')
        self.assertEqual(streams[1].map, 3)

    def test_wrong_mapping(self):
        input = Input('fixtures/sintel-multi.mkv', 'blabla')
        self.assertEqual(input.get_final_maps(), [])

        streams = input.get_final_streams()
        self.assertEqual(len(streams), 0)

    def test_debug(self):
        input = Input('fixtures/sintel-multi.mkv')
        input.debug()


class TestMedia(unittest.TestCase):
    def test_init_video(self):
        path = 'fixtures/sintel.mp4'
        media = Media(path)
        self.assertEqual(str(media.get_path()), path)
        self.assertIsInstance(media.get_path(), Path)
        self.assertEqual(len(media.get_streams()), 2)
        self.assertEqual(len(media.get_video_streams()), 1)
        self.assertEqual(len(media.get_audio_streams()), 1)
        self.assertEqual(len(media.get_subtitle_streams()), 0)

        streams = media.get_streams()

        self.assertIsInstance(streams[0], VideoStream)
        self.assertEqual(streams[0].language, 'und')
        self.assertEqual(streams[0].codec, 'h264')
        self.assertEqual(streams[0].map, 0)

        self.assertIsInstance(streams[1], AudioStream)
        self.assertEqual(streams[1].language, 'eng')
        self.assertEqual(streams[1].codec, 'aac')
        self.assertEqual(streams[1].map, 1)

    def test_init_audio(self):
        path = 'fixtures/music.mp3'
        media = Media(path)
        self.assertEqual(str(media.get_path()), path)
        self.assertIsInstance(media.get_path(), Path)
        self.assertEqual(len(media.get_streams()), 1)
        self.assertEqual(len(media.get_video_streams()), 0)
        self.assertEqual(len(media.get_audio_streams()), 1)
        self.assertEqual(len(media.get_subtitle_streams()), 0)

        streams = media.get_streams()

        self.assertIsInstance(streams[0], AudioStream)
        self.assertEqual(streams[0].language, 'und')
        self.assertEqual(streams[0].codec, 'mp3')
        self.assertEqual(streams[0].map, 0)

    def test_init_subtitle(self):
        path = 'fixtures/es.srt'
        media = Media(path)
        self.assertEqual(str(media.get_path()), path)
        self.assertIsInstance(media.get_path(), Path)
        self.assertEqual(len(media.get_streams()), 1)
        self.assertEqual(len(media.get_video_streams()), 0)
        self.assertEqual(len(media.get_audio_streams()), 0)
        self.assertEqual(len(media.get_subtitle_streams()), 1)

        streams = media.get_streams()

        self.assertIsInstance(streams[0], SubtitleStream)
        self.assertEqual(streams[0].language, 'und')
        self.assertEqual(streams[0].codec, 'subrip')
        self.assertEqual(streams[0].map, 0)

    def test_init_multi(self):
        path = 'fixtures/sintel-multi.mkv'
        media = Media(path)
        self.assertEqual(str(media.get_path()), path)
        self.assertIsInstance(media.get_path(), Path)
        self.assertEqual(len(media.get_streams()), 4)
        self.assertEqual(len(media.get_video_streams()), 1)
        self.assertEqual(len(media.get_audio_streams()), 1)
        self.assertEqual(len(media.get_subtitle_streams()), 2)

        streams = media.get_streams()

        self.assertIsInstance(streams[0], VideoStream)
        self.assertEqual(streams[0].language, 'eng')
        self.assertEqual(streams[0].codec, 'h264')
        self.assertEqual(streams[0].map, 0)

        self.assertIsInstance(streams[1], AudioStream)
        self.assertEqual(streams[1].language, 'eng')
        self.assertEqual(streams[1].codec, 'vorbis')
        self.assertEqual(streams[1].map, 1)

        self.assertIsInstance(streams[2], SubtitleStream)
        self.assertEqual(streams[2].language, 'eng')
        self.assertEqual(streams[2].codec, 'ass')
        self.assertEqual(streams[2].map, 2)

        self.assertIsInstance(streams[3], SubtitleStream)
        self.assertEqual(streams[3].language, 'es')
        self.assertEqual(streams[3].codec, 'ass')
        self.assertEqual(streams[3].map, 3)

    def test_wrong_file(self):
        with self.assertRaises(Exception):
            # File doesn't exist
            path = 'fixtures/sintel.mp3'
            media = Media(path)


class TestStream(unittest.TestCase):
    def test_init(self):
        stream = Stream()
        stream.from_json({
            'index': 0,
            'codec_name': 'h264',
            'tags': {
                'language': 'fre'
            }
        })
        self.assertEqual(stream.map, 0)
        self.assertEqual(stream.codec, 'h264')
        self.assertEqual(stream.language, 'fre')
