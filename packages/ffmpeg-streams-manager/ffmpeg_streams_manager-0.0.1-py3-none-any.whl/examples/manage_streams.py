from ffmpeg_streams_manager import *

"""
We want to keep only video stream or english streams or on MAP 0
"""
input1 = Input("../fixtures/sintel-multi.mkv", ['video', 'eng', 0])
"""
By default, keep all streams
"""
input2 = Input("../fixtures/music.mp3")

"""
We will get a video with:
stream Video (map 0)
stream Audio (eng)
stream Subtitle (eng)
stream Audio (music.mp3)
"""
converter = Converter('../fixtures/output.mkv')
converter.add_input(input1)
converter.add_input(input2)
# converter.debug()
converter.run()
