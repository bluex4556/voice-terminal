import speech_recognition as sr
import pyaudio
import time
import sys
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 4

def recognizespeech():
    r =sr.Recognizer()
    audiosource = sr.AudioFile('output.wav')
    with audiosource as source:
        audio = r.record(source)
    #Prints the recognized data
    return r.recognize_google(audio)

def readwavfile():
    #opens a wav file
    wf = wave.open('output.wav','rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

    data = wf.readframes(CHUNK)


    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    

    stream.stop_stream()
    stream.close()

    p.terminate()

def makewavfile():
    p = pyaudio.PyAudio()
    WAVE_OUTPUT_FILENAME = "output.wav"

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

makewavfile()
readwavfile()
print(recognizespeech())
