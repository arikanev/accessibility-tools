import multiprocessing
import speech_recognition as sr
import time
import shlex
from subprocess import check_call


def run(spoken_answer=None):

    r=sr.Recognizer()

    m=sr.Microphone()

    while True:
        with m as source:
            r.adjust_for_ambient_noise(source)
            print("speak")
            start_listen = time.time()
            audio = r.listen(source)
            print("listen duration: {}".format(time.time() - start_listen))
            start_reco = time.time()
            spoken_answer = r.recognize_google(audio)
            print("recognition duration: {}".format(time.time() - start_reco))
            print(spoken_answer)

def record():

    check_call(shlex.split("ffmpeg -loglevel quiet -f avfoundation -framerate 29.97 -i 0:0 out.mkv"), universal_newlines=True)


if __name__=='__main__':

    multiprocessing.Process(target=record).start()
    multiprocessing.Process(target=run).start()
