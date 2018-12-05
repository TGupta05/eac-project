import speech_recognition as sr
import time
import numpy as np
import sys
import paramiko
from scp import SCPClient
import wave

def main():

    ########################### RUNNING RNN REMOTELY ###########################
    recognizer = sr.Recognizer()
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    frame_data = sr.AudioFile('audio.wav')

    with frame_data as source:
        audio = recognizer.record(source)
   
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    print("starting translation")
    remote_start_time = time.time()
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    remote_end_time = time.time()
    print("done translating")

    
    ########################## SENDING DATA TO LOCAL DEVICE ##########################
    print("start sending")
    saving_start_time = time.time()
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname="172.20.10.5",username="pi",password="raspberry")

    scp = SCPClient(client.get_transport())
    with open("results.txt", "w+") as d:
        try:
            d.write(response['transcription'])
            print("TRANSLATION: "+str(response['transcription']))
        except:
            d.write("could not translate")

    scp.put("results.txt", "/home/pi/Documents/eac-project/results.txt")

    saving_end_time = time.time()
    print("done sending")

    print("REMOTE COMPUTATION: " + str(remote_end_time-remote_start_time))
    print("SEND TO LOCAL DEVICE: " + str(saving_end_time-saving_start_time))

if __name__ == '__main__':
    main()