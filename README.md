# README

This is Cocomusic, a Python program that renders Tandy Color Computer music video that was based on the source code found at:
https://colorcomputerarchive.com/repo/Programming/Source/Assembly%20music

## Requirements

Python 3.x and a virtual environment. Use the requirements.txt to make the virtualenv.

[FFmpeg](https://ffmpeg.org) is required.

You can run this code as:

```python cocomusic.py -i"input.bin" [-a|-A]```

the -a (or -A) parameter generates the audio. If ommited, the video will have no audio, only the waveform.

Use [ASM6809](https://www.6809.org.uk/asm6809/) to compile. Then add the Tandy Color Computer bin file header to the compiled file:

- 0x00 (data chunk)
- 0xnn 0xnn (length)
- 0xnn 0xnn (load address, usually is 0x3e 0x00)

You can make the header as:

```echo -n -e "\x00\x52\x2d\x3e\x00" > header.bin```

Finaly you put all together with a mere cat:

```cat header.bin music.bin > music_with_header.bin```







