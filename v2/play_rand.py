import os
from random import randrange
import subprocess, sys
import time

num_segs = len([name for name in os.listdir('./segments/') if os.path.isfile(os.path.join('./segments/', name))])
opener ="open" if sys.platform == "darwin" else "xdg-open"

while input("press enter in command line to cycle videos, any other key to exit:") == '':
    subprocess.call([opener, 'segments/IMG_4654-{}.mp4'.format(randrange(num_segs))])
