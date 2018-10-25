import speech_recognition as sr

recognizer = sr.Recognizer()
microphone = sr.Microphone()
# microphone = sr.Microphone(device_index=1)

if not isinstance(recognizer, sr.Recognizer):
    raise TypeError("`recognizer` must be `Recognizer` instance")

if not isinstance(microphone, sr.Microphone):
    raise TypeError("`microphone` must be `Microphone` instance")

# adjust the recognizer sensitivity to ambient noise and record audio
# from the microphone
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

# send audio.frame_data, audio.sample_rate, audio.sample_width
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