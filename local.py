import speech_recognition as sr
import time
import numpy as np
import sys
import paramiko
from scp import SCPClient

def main():

    ########################### RUNNING RNN LOCALLY ###########################
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    local_start_time = time.time()
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    local_end_time = time.time()
    
    try:
        print("TRANSLATION: "+str(response['transcription']))
    except:
        pass

    ########################## SENDING DATA TO REMOTE SERVER ##########################
    saving_start_time = time.time()
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname="172.20.10.2",username="tushitagupta",password="i8MyDog2!")
    scp = SCPClient(client.get_transport())

    with open("audio.wav", "wb") as d:
        d.write(audio.get_wav_data())

    scp.put("audio.wav", "Documents/eac-project/audio.wav")

    saving_end_time = time.time()

    print("LOCAL COMPUTATION: " + str(local_end_time-local_start_time))
    print("SEND TO REMOTE SERVER: " + str(saving_end_time-saving_start_time))

if __name__ == '__main__':
    main()