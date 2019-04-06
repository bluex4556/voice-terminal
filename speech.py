from pydub import AudioSegment
from gtts import gTTS
import speech_recognition as sr
import pyaudio
import time
import sys
import wave
import os

#amount of data used at a time
CHUNK = 1024
#input and output to .wav file 
FORMAT = pyaudio.paInt16 
CHANNELS = 2
RATE = 44100
#amont of seconds to record at a time
RECORD_SECONDS = 4

#function to convert speech to text
def recognizespeech():
    #r has the speech recognizer class
    r =sr.Recognizer()
    #takes the audio from the output  
    audiosource = sr.AudioFile('output.wav')
    with audiosource as source:
        audio = r.record(source)
    #Prints the recognized data

    try:
        data = r.recognize_google(audio)
        return data
    except sr.UnknownValueError:
        return ("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        return ("Could not request results from Google Speech Recognition service; {0}".format(e))

def readwavfile():
    #opens a wav file
    wf = wave.open('tts.wav','rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=12700,
                output=True)
    
    #takes data chunks at a time
    data = wf.readframes(CHUNK)

    #reads out data from wav file
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
        
    stream.stop_stream()
    stream.close()

    p.terminate()

def makewavfile():
    p = pyaudio.PyAudio()
    #records from microphone and outputs it to output.wav file
    WAVE_OUTPUT_FILENAME = "output.wav"

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    #gets frame chunks one at a time and appends it
    
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

def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
    audio = r.listen(source)

def saytts(content):
    tts = gTTS(text=content, lang='en')
    tts.save("tts.mp3")
    sound = AudioSegment.from_mp3("tts.mp3")
    sound.export("tts.wav", format="wav")
    readwavfile()

def displaymenu():
    print("------------------------------------------------------------------------------------------------------")
    print("                                            S-H-E-L-L")
    print("-------------------------------------------------------------------------------------------------------")
    print("Options")
    print("[1] Create Directory")
    print("[2] Delete Directory")
    print("[3] Create File")
    print("[4] Delete File")
    print("[5] Rename File")
    print("[6] Display File Content")
    print("[7] Edit File")
    print("[8] Switch Between Speech and Keyboard")
    print("[9] Exit")

def keyboardinput():        
    displaymenu()
    n= int(input('Choose Command>>:  '))
    
    if(n==1):
        x=input('Enter dir name:   ')
        os.mkdir(x)
        saytts("directory added succesfully")
    
    if(n==2):
        x=input('Enter dir name to be deleted:   ')
        try:
            os.rmdir(x)
        except:
            print("Directory doesnt exist")
    
    if(n==3):
        x=input('Enter file-name:   ')
        file=open(x,'w')
    
    if(n==4):
        x=input('Enter file-name to be deleted:   ')
        try:
            os.remove(x)
        except:
            print("File doesnt exist")
    
    if(n==5):
        x=input('Enter old file-name :   ')
        y=input('Enter new file-name       :   ')
        try:
            os.rename(x,y)
        except:
            print("File doesnt exist")
    
    if(n==6):
        x=input('Enter file-name  :   ')
        file=open(x,'r')
        content=file.read()
        print(content)

    if(n==7):
        x=input('Enter file-name    :   ')
        print('\n'*2)
        print("______________________________________________________________________________________")
        print('\n'*2)
        file=open(x,'w')
        y=input('>')
        file.write(y)
        file.close()
    
    if(n==8):
        speechinput()
    if (n==9):
        exit()

def speechinput():    
    displaymenu()
    while True:    
        time.sleep(2)

        makewavfile()
        cspeech = recognizespeech()
        print(cspeech)
        if (cspeech == "make directory" or cspeech=="one"):
            makewavfile()
            x=recognizespeech()
            os.mkdir(x)
            saytts("Directory added successfully")
            print("Directory Added successfully!")

        elif(cspeech=="delete directory" or cspeech=="two"):
            makewavfile()
            x=recognizespeech()
            try:
                os.rmdir(x)
            except:
                print("Directory doesnt exist")

        elif (cspeech=="create file"):
            makewavfile()   
            x=recognizespeech()
            file=open(x,'w')

        elif (cspeech=="delete file"):
            makewavfile()
            x=recognizespeech()
            try:
                os.remove(x)
            except:
                saytts("File does not exist")
                print("File doesnt exist")

        elif (cspeech=="rename file"):
            makewavfile()
            x=recognizespeech()
            try:
                os.remove(x)
            except:
                saytts("File does not exist")
                print("File doesnt exist")

        elif(cspeech=="read file"):
            makewavfile()
            x=recognizespeech()
            file=open(x,'r')
            content=file.read()
            print(content)

        elif(cspeech=="edit file"):
            makewavfile()
            x=recognizespeech()
            print('\n'*2)
            print("______________________________________________________________________________________")
            print('\n'*2)
            file=open(x,'w')
            y=input('>')
            file.write(y)
            file.close()

        elif (cspeech=="keyboard"):
            keyboardinput()

        elif(cspeech=="stop" or cspeech=="exit"):
            exit()
        
        else:
            saytts("command not found")
            print("command not found")


speechinput()