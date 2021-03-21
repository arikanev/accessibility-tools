import multiprocessing
import os
import speech_recognition as sr
import shlex
import subprocess
from subprocess import check_call
import time

def audio(spoken_answer=None):

    prompt = []

    with open('min_pair_wl.txt', 'r') as wl:

        l = wl.readlines()

    for i in l:

        prompt.append(i.split('/')[0].strip())

    r=sr.Recognizer()

    r.non_speaking_duration = 0.5

    r.pause_threshold = 0.5

    m=sr.Microphone()

    idx = 0

    os.chdir('./tables/')

    num_tables = subprocess.getoutput("ls -1 | wc -l")

    table_number = int(num_tables) + 1

    while True:

        start_reco = time.time()

        with m as source:
            r.adjust_for_ambient_noise(source)
            try:
                print(prompt[idx])
            except IndexError:
                print("press q to quit video")
                return
            audio = r.listen(source)
            spoken_answer = r.recognize_google(audio).lower()
            print(spoken_answer, prompt[idx], spoken_answer==prompt[idx])
            with open('{}.table'.format(table_number), 'a') as table:
                table.write("{}. {} {} - {}\n".format(idx, spoken_answer, 0, time.time() - start_reco))
            idx += 1

def video():

    os.chdir('./vids/')
    num_vids = subprocess.getoutput("ls -1 | wc -l")
    vid_number = int(num_vids) + 1
    check_call(shlex.split("ffmpeg -loglevel quiet -f avfoundation -framerate 29.97 -i 0:0 {}.mkv".format(vid_number)), universal_newlines=True)
    check_call(shlex.split("ffmpeg -i {}.mkv -vcodec libx264 -acodec libmp3lame -pix_fmt yuv420p {}.MOV".format(vid_number, vid_number)))
    os.remove('{}.mkv'.format(vid_number))
    # os.rename("{}.mp4".format(vid_number), "{}.MOV".format(vid_number))
    return

if __name__=='__main__':

    j1 = multiprocessing.Process(target=audio)
    j2 = multiprocessing.Process(target=video)

    j1.start()
    j2.start()
