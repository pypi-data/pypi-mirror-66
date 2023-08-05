from ffmpeg_streams_manager import *

input1 = Input("../fixtures/sintel.mp4")
input1.debug()
"""
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
"""
"""
This result means this file has 2 streams : 1 video and 1 audio (0 subtitles)
"""