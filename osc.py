import PIL.Image as im
import PIL.ImageDraw as dr
import cv2
import numpy as np

SIZE = (1280,720)
# 32 - 160
def render(frame_index : int, channels : list) -> im.Image:
    NUM_CHANNELS = len(channels)
    CHAN_HEIGHT = SIZE[1] * 1.0 / NUM_CHANNELS
    CHAN_LIM = CHAN_HEIGHT * 0.8
    FACTOR = (CHAN_LIM / 2.0) / 32.0
    frame=im.new("RGB",SIZE)
    draw = dr.Draw(frame)
    
    pos = frame_index * 102
    for i, channel in enumerate(channels):
        my = i * CHAN_HEIGHT + (CHAN_LIM / 2.0)
        coords = list(zip((x for x in range(SIZE[0])),(int((32.0 - v) * FACTOR + my) for v in channel[pos:pos+SIZE[0]])))
        for n in range(1,len(coords)):
            draw.line(xy=(coords[n-1][0],coords[n-1][1],coords[n][0],coords[n][1]), fill=(255,255,255))
    return frame

def process(channels : list, filename : str):
    frame_count = len(channels[0]) // 102
    writer = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'),30,SIZE)
    #writer.open("demo.mpg")
    for f in range(frame_count):
        frame=np.array(render(f, channels))
        writer.write(frame)
    writer.release()
        