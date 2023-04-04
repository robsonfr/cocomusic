import pyaudio
import time
import wave
from osc import render, process

import sys
import getopt
import os

def load_from_binary(bindata : bytes):
    sample_data = bindata[:256]
    notes = bindata[256:512]
    tempo = bindata[0x254] >> 1
    music = bindata[0x2B4:]
    return (sample_data, notes, tempo, music)


def create_outputdata(TEMPO, music, sample_data, notes):
    output_data = []
    channels_data = [[],[],[],[]]
    indexes = [0,0,0,0]
    for u in range(len(music) // 5):
        dur, curnotes = music[u*5], music[u*5+1:u*5+5]
        cn = curnotes[0]
        if dur == 0:
            break
        d = dur * TEMPO
        while d:
            s = 0
            for j,cn in enumerate(curnotes):
                i = (indexes[j] >> 8) & 255
                #if notes[cn] == 0:
                #    v = 0
                #else:
                v = sample_data[i]
                
                channels_data[j].append(v)
                s += (v << 2)
                
                carry = 1 if s > 255 else 0
                indexes[j] += (notes[cn] << 8) + notes[cn+1]
                indexes[j] = indexes[j] & 65535
            output_data.append(s >> 2)
            d -= 1
    return output_data, channels_data

def save_wavfile(filename, RATE, audio, output_data):
    wavfile = wave.open(filename,"wb")
    wavfile.setnchannels(1)
    wavfile.setsampwidth(audio.get_sample_size(pyaudio.paUInt8))
    wavfile.setframerate(RATE)
    wavfile.writeframes(bytes(output_data))
    wavfile.close()


def main():
    opts, args = getopt.getopt(sys.argv[1:],'i:Aa')

    inpfilename=''
    generate_audio = False
    for k,v in opts:
        if k == '-i':
            inpfilename=v
        if k.lower() == '-a':
            generate_audio = True

    if inpfilename:
        print(inpfilename)
        video_file = inpfilename[:-3] + 'mp4'

        with open(inpfilename,'rb') as inp:
            data = inp.read()
        
        RATE=3065
        #TEMPO=0x34
        sample_data, notes, tempo, music = load_from_binary(data[5:])
        output_data, channels_data = create_outputdata(tempo, music, sample_data,notes)
        process(channels_data, video_file)
        audio_proc=' '
        if generate_audio:
            audio_file = inpfilename[:-3] + 'wav'
            audio = pyaudio.PyAudio()
            save_wavfile(audio_file, RATE, audio, output_data)
            audio.terminate()
            audio_proc=f' -i {audio_file} -ar 44100 '

        os.system(f'ffmpeg -i {video_file}{audio_proc}full_{video_file}')

if __name__ == '__main__':
    main()