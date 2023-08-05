from ffmpeg_streams_manager import *

input1 = Input("../fixtures/sintel.mp4")
input2 = Input("../fixtures/en.srt")
input3 = Input("../fixtures/es.srt")

converter = Converter('output.mkv')
converter.add_input(input1)
converter.add_input(input2)
converter.add_input(input3)
converter.debug()
# converter.run()

"""
Result :
  {'language': 'und', 'map': 0, 'codec': 'h264'}
  {'language': 'eng', 'map': 1, 'codec': 'aac'}
  {'language': None, 'map': 0, 'codec': 'subrip'}
  {'language': None, 'map': 0, 'codec': 'subrip'}

Input : sintel-1024-surround.mp4
  Mapping :
    {'language': 'und', 'map': 0, 'codec': 'h264'}
    {'language': 'eng', 'map': 1, 'codec': 'aac'}
  ----  debug ---- 
  Video streams :
    {'language': 'und', 'map': 0, 'codec': 'h264'}
  Audio streams :
    {'language': 'eng', 'map': 1, 'codec': 'aac'}
  Subtitle streams :

Input : sintel_en.srt
  Mapping :
    {'language': None, 'map': 0, 'codec': 'subrip'}
  ----  debug ---- 
  Video streams :
  Audio streams :
  Subtitle streams :
    {'language': None, 'map': 0, 'codec': 'subrip'}

Input : sintel_es.srt
  Mapping :
    {'language': None, 'map': 0, 'codec': 'subrip'}
  ----  debug ---- 
  Video streams :
  Audio streams :
  Subtitle streams :
    {'language': None, 'map': 0, 'codec': 'subrip'}
"""