#!/bin/bash
source .pyenv/bin/activate
python demo.py
ffmpeg -i demo.mp4 -i demo.wav -ar 44100 demo_audio.mp4
