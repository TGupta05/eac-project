import librosa
import numpy
import alsaaudio
import time

AUDIO_SEGMENT_TIME = 5 
AUDIO_FS = 44100

def cleanAndExit():
    GPIO.cleanup()
    print "\nBye!"
    sys.exit()

int main():

    # initialize microphone
    card = 'sysdefault:CARD=Device'
    num_ms = AUDIO_FS * AUDIO_SEGMENT_TIME
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
    inp.setchannels(1)
    inp.setrate(AUDIO_FS)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(32)

    # loop and record audio segments from microphone
    while (True):
        try:
            # get 5 seconds of audio
            totalLen = 0
            signal = []
            while (totalLen < num_ms):
                l, data = inp.read()
                if (l > 0):
                    signal += list(np.fromstring(data, 'int16'))
                    totalLen += l

        except:
            cleanAndExit()


if __name__ =="__main__":
    main()
