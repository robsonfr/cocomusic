import PIL.Image as im
import PIL.ImageDraw as dr
import cv2
import numpy as np

# 32 - 160
def render(frame_index : int, channels : list) -> im.Image:
    frame=im.new("RGB",(1280,720))
    draw = dr.Draw(frame)
    pos = frame_index * 102
    for i, channel in enumerate(channels):
        mx = 20
        my = i * 144 
        coords = list(zip((x * 12 + mx for x in range(102)),((64 - v) * 2 + my for v in channel[pos:pos+102])))
        for n in range(1,len(coords)):
            draw.line(xy=(coords[n-1][0],coords[n-1][1],coords[n][0],coords[n][1]), fill=(255,255,255))
    return frame

def process(channels : list, filename : str):
    frame_count = len(channels[0]) // 102
    writer = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'),30,(1280,720))
    #writer.open("demo.mpg")
    for f in range(frame_count):
        frame=np.array(render(f, channels))
        writer.write(frame)
    writer.release()
        