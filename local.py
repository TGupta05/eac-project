import speech_recognition as sr
import time
import numpy as np
import sys

def main():
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

    print(response['transcription'])

    saving_start_time = time.time()
    np.save("audio.npy", audio.frame_data)
    np.save("sample_rate.npy", audio.sample_rate)
    np.save("sample_width.npy", audio.sample_width)
    with open(str(sys.argv[1]), "w+") as d:
        d.write(response['transcription'])

    saving_end_time = time.time()
    print("Elapsed time for saving data = " + str(saving_end_time-saving_start_time))

if __name__ == '__main__':
    main()