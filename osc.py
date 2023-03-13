import PIL.Image as im
import PIL.ImageDraw as dr
import cv2
import numpy as np

fundo=im.open("oscillosc.png")

# 32 - 160
def render(frame_index : int, channels : list) -> im.Image:
    frame=fundo.copy()
    draw = dr.Draw(frame)
    pos = frame_index * 102
    for i, channel in enumerate(channels):
        mx = (i % 2) * 310 + 20
        my = ((i >> 1) % 2) * 274 + 16
        coords = list(zip((x * 3 + mx for x in range(102)),((64 - v) * 2 + my for v in channel[pos:pos+102])))
        for n in range(1,len(coords)):
            draw.line(xy=(coords[n-1][0],coords[n-1][1],coords[n][0],coords[n][1]), fill=(255,255,255))
    return frame.convert('RGB')

def process(channels : list):
    frame_count = len(channels[0]) // 102
    writer = cv2.VideoWriter("demo.mp4", cv2.VideoWriter_fourcc(*'mp4v'),30,(640,480))
    #writer.open("demo.mpg")
    for f in range(frame_count):
        frame=np.array(render(f, channels))
        writer.write(frame)
    writer.release()
        