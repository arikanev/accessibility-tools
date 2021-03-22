import multiprocessing
import os
import speech_recognition as sr
import shlex
import subprocess
from subprocess import Popen, check_call
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

    GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "bmi-deep-learning",
  "private_key_id": "e31b4feb8e718e25c5f5fb9700fd7f02b8e1efa2",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCGak/qQnFXnD7i\n8E5D15qwWZ/yeb9xOqyQ43/AhiwVON+yEg62WI44uaDKJOmEkUGfsXxVfRGYeUTH\ndVy603okTCWq5aKrMnDsp1MBtN0sotJnsUkPW1LcdCCbIwdTQw6InNPJ2Iy3rKkg\n0+eVn5spiYwUQy/xMwWFeCP9zBleXHfX2DsGb7DlUnySIm6tmEi4w8O7gu21XOZt\nCwF27AWeJMe6jdTXC+RZ4LPLy41VXI+k6AUouKGmk1Sg1doRs8RdN9uyeK1g0TWw\n/65sk22MX4C4XAOXxcsmflg1oRAiFZsYbQm5O6PU+8UJUUsKhlEtXxs4RS62k+UB\nNNYUxs6pAgMBAAECggEAKf84heSJnkqCuYxEn9zTB6uRFoUkpB+lgEWcik5BosXY\n2r3am+2STjXtf4tF7PYnj1o4k0tW/pFRRJKuTO87V/D0ye8iwqOpdb+X504X1tTu\nsZhKUAKEIr4j2+T3anPmrBd38rZ2zQKk+01KK80pATLpMgGGDrIW1QtjD27ANGNy\n4VvEe/yFPYX9QSXHV3olPDo0Q9Bni8PvU0CGCAiyUyhMV6J5i7MwENTGBi+8Zp+d\njKZc6Kl/IxXSQr30ygT3vy/fNBfafby7AwG4ORBYqJMe/sA0+3WhUYN+u0CNG0wa\neRFJLFM4l37iS0fppn+818nJ+hJLrPo8nzpgWx3R0wKBgQC52FnpJC+R4rZH8xHz\niVdOVUCUdaUbq3oBLXTvdjOTqa2HfkUdKfaOewxppEy/ep4/eIel6GsNOQSZVsNk\n9jG7Y5n/S8w+b++XBLfoU4axZMcKqDD8AYHSSbIcWBCrk1tYyAwvsF/aWZkCeyOp\n0FmUz9IUVizubFiJUZc4S2ZDIwKBgQC5J+YDuTfpIBzC9NqHNynYsnIIJbJFYZbL\nOqZWm4mwXHabaHzWLdvSgQV/+GC1275OBQiIBTTllz8WsqsjsAYcTSq8g8pTLcbG\nTUFGrcSesCi9wIOyuGuBs+ykf8AvGax3PvJ2CO26iHA1aq0D0fiI/NH5DSLcw2dW\n5FGG/TPZwwKBgELKN13rjFEQulPXTo9Iv6C+UMxKD4GHOfysWoco4tZht6SnQ618\nhEimfkqFKrPyHGdRKOb+RWLmJ/n3zZc+R5dB73lpw0h5MBEFOBb91b1xK3twANLA\ns+hgZet71tnixoR8uKx25avyYWQb3zBLWbZ6jdSTN+ij9Zm8Qe2QY3sjAoGAdW7G\nxgnNWkCRvVzK1QO5uMTE6kHuZW7V0yPpp/iSRZb/auXEd5syVrqaIGYKAI3Uj2tF\n0+9pc0yQKPc88C+OUJjoyBPWWRcpgVAyXH+NuxADZwYZAVtSZDsXleWooLbp2d/E\nq/RRwwMSF+8GuOuNdGTVT95zBA2zFztMMg+ZuT0CgYBk+Wfih2LPIOZzeWDjU3Z4\n359qxlZ5pAP3S3OxaBtAhaDZnqTHzOzv6NbJEm95Eh2LoosK57GXDd4Mj7+pz/5I\nmo4EwYbC68lgHXUaI/rXWZuSD0Y7+5ajgmJFgl0S2DqjZBB1bW+NlQj5C1ydIDiv\nruHirq7Bw7T4YcLYE1JQxw==\n-----END PRIVATE KEY-----\n",
  "client_email": "516226124291-compute@developer.gserviceaccount.com",
  "client_id": "110051455929089160649",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/516226124291-compute%40developer.gserviceaccount.com"
}"""

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
            try:
                spoken_answer = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, preferred_phrases=[prompt[idx]]).lower().strip()
                # spoken_answer = r.recognize_google(audio).lower()
                # spoken_answer = r.recognize_sphinx(audio, keyword_entries=[(prompt[idx], 0.8)]).lower().strip()
            except sr.UnknownValueError:
                spoken_answer = ""

            print(spoken_answer, prompt[idx], spoken_answer==prompt[idx])

            if spoken_answer == prompt[idx] or (spoken_answer == 'p' and prompt[idx] == 'pea') or (spoken_answer == 'pi' and prompt[idx] == 'pie'):
                with open('{}.table'.format(table_number), 'a') as table:
                    table.write("{}. {} {} - {}\n".format(idx, spoken_answer, 0, time.time() - start_reco))
                idx += 1

            else:
                with open('{}.table'.format(table_number), 'a') as table:
                    table.write("{}. {} {} - {}\n".format(idx, "GARBAGE", 0, time.time() - start_reco))

def video():

    os.chdir('./vids/')
    num_vids = subprocess.getoutput("ls -1 | wc -l")
    vid_number = int(num_vids) + 1
    p = Popen(shlex.split("ffmpeg -loglevel quiet -f avfoundation -framerate 29.97 -i 0:0 {}.mkv".format(vid_number)), universal_newlines=True)
    if p.poll() is None:
        print("video starting")
    p.wait()
    check_call(shlex.split("ffmpeg -i {}.mkv -vcodec libx264 -acodec libmp3lame -pix_fmt yuv420p {}.MOV".format(vid_number, vid_number)))
    os.remove('{}.mkv'.format(vid_number))
    # os.rename("{}.mp4".format(vid_number), "{}.MOV".format(vid_number))
    return

if __name__=='__main__':

    j1 = multiprocessing.Process(target=video)
    time.sleep(1)
    j2 = multiprocessing.Process(target=audio)

    j1.start()
    j2.start()
