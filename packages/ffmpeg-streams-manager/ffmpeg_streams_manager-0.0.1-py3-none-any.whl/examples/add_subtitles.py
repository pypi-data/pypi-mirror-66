from ffmpeg_streams_manager import *

input1 = Input("../fixtures/sintel.mp4")
input1.get_media().get_video_streams()[0].language = 'eng'

input2 = Input("../fixtures/en.srt")
input2.get_media().get_subtitle_streams()[0].language = 'eng'

input3 = Input("../fixtures/es.srt")
input3.get_media().get_subtitle_streams()[0].language = 'es'

converter = Converter('../fixtures/output.mkv')
converter.add_input(input1)
converter.add_input(input2)
converter.add_input(input3)
# converter.debug()
converter.run()
