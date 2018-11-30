import librosa
import numpy
import alsaaudio
import time
import RPi.GPIO as GPIO
import wavio


AUDIO_FS = 44100
PAUSE_TIME = 0.2
PERIOD_SIZE = 32
INPUT_CHANNEL = 1
GPIO_BUTTON_PIN = 18

def cleanAndExit():
    GPIO.cleanup()
    print "\nBye!"
    sys.exit()

int main():

    # initialize microphone
    card = 'sysdefault:CARD=Device'
    num_ms = AUDIO_FS * AUDIO_SEGMENT_TIME
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
    inp.setchannels(INPUT_CHANNEL)
    inp.setrate(AUDIO_FS)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(PERIOD_SIZE)
    signal = []
    is_button_pushed = False
    init_time = 0
    end_time = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # loop and record audio segments from microphone 
    # only while the button is pushed
    while (True):

        try:
            is_button_pushed = not GPIO.input(GPIO_BUTTON_PIN)
            
            if (is_button_pushed):
                if (len(signal) == 0):
                    init_time = time.strftime("%Y%m%d-%H%M%S")
                    print("Starting to record the audio signal...")
                
                total_l = 0
                while (total_l < PAUSE_TIME * AUDIO_FS)
                l, data = inp.read()
                if (l > 0):
                    signal += list(np.fromstring(data, 'int16'))
                    total_l += l
            
            else:
                if (len(signal) > 0):
                    print("Done recording the audio signal!")
                    end_time = time.strftime("%Y%m%d-%H%M%S")
                    file_name = init_time + "-to-" + end_time + ".wav"
                    wavio.write(file_name, np.array(signal), AUDIO_FS)
                    
                    signal = []
                    init_time = 0
                    end_time = 0
        except:
            cleanAndExit()


if __name__ =="__main__":
    main()
