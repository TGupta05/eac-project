import speech_recognition as sr
from paramiko import SSHClient
from scp import SCPClient
import time

# client = paramiko.SSHClient()
# client.load_system_host_keys()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect(hostname="172.20.10.2",username="tushitagupta",password="i8MyDog2!")
# scp = SCPClient(ssh.get_transport())

recognizer = sr.Recognizer()
microphone = sr.Microphone()

if not isinstance(recognizer, sr.Recognizer):
    raise TypeError("`recognizer` must be `Recognizer` instance")

if not isinstance(microphone, sr.Microphone):
    raise TypeError("`microphone` must be `Microphone` instance")

# adjust the recognizer sensitivity to ambient noise and record audio
# from the microphone
# audio.frame_data, audio.sample_rate, audio.sample_width

local_start_time = time.time()
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)
local_end_time = time.time()
print("Elapsed time for local computation = " + str(local_end_time-local_start_time))

# remote_start_time = time.time()
# scp.put("audio.wav", "audio.wav")
# scp.put("sample_rate.txt", "sample_rate.txt")
# scp.put("sample_width.txt", "sample_width.txt")

# scp.get("audio.wav")
# scp.get("sample_rate.txt")
# scp.get("sample_width.txt")
# remote_end_time = time.time()

# print("Elapsed time for remote computation = " + str(remote_end_time-remote_start_time))

# recreate the audio class as follows:
# audio = sr.AudioData(audio.frame_data, audio.sample_rate, audio.sample_width)

# set up the response object
response = {
    "success": True,
    "error": None,
    "transcription": None
}

# try recognizing the speech in the recording
# if a RequestError or UnknownValueError exception is caught,
#     update the response object accordingly
try:
    response["transcription"] = recognizer.recognize_sphinx(audio)
except sr.RequestError:
    # API was unreachable or unresponsive
    response["success"] = False
    response["error"] = "API unavailable"
except sr.UnknownValueError:
    # speech was unintelligible
    response["error"] = "Unable to recognize speech"

speech = response['transcription']
print(speech)