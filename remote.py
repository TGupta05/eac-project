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

    remote_start_time = time.time()
    try:
        response["transcription"] = recognizer.recognize_google(audio)
        print("TRANSLATION: "+str(response['transcription']))
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    local_end_time = time.time()
    with open("results.txt", "w+") as d:
        try:
            d.write(response['transcription'])
        except:
            d.write("could not translate")
    remote_end_time = time.time()
    print("REMOTE COMPUTATION = " + str(remote_end_time-remote_start_time))

    ########################## SENDING DATA TO LOCAL DEVICE ##########################
    saving_start_time = time.time()
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname="172.20.10.5",username="pi",password="raspberry")
    scp = SCPClient(client.get_transport())
    scp.put("results.txt", "results.txt")
    saving_end_time = time.time()
    print("SEND TO LOCAL DEVICE: " + str(saving_end_time-saving_start_time))

if __name__ == '__main__':
    main()