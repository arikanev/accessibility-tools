import argparse
import os
from random import shuffle
import subprocess, sys
import tkinter as tk
from tkinter import simpledialog
from tkinter import *

class MyDialog(simpledialog.Dialog):
    def body(self, master):
        self.geometry("800x600")
        tk.Label(master, text="What did Sara just say?").grid(row=0)

        self.e1 = tk.Entry(master)
        self.e1.grid(row=0, column=1)
        return self.e1 # initial focus

    def apply(self):
        first = self.e1.get()
        self.result = first


parser = argparse.ArgumentParser(description='Process range.')
parser.add_argument('--range', '-r', type=int, nargs=2,
                    help='start and end integer range of videos to select. In form start end')

args = parser.parse_args()

# num_segs = len([name for name in os.listdir('./segments/') if os.path.isfile(os.path.join('./segments/', name))])

opener ="open" if sys.platform == "darwin" else "xdg-open"

closer ="close" if sys.platform == "darwin" else "xdg-close"

'''
rand_list = []
for i in range(5):
    rand_list.append(randrange(num_segs))
'''


'''
rand_list = []
for i in range(args.range[0], args.range[1]):
    rand_list.append(i)
shuffle(rand_list)
'''

idxs = []
for i in range(args.range[0], args.range[1]):
    idxs.append(i)

ROOT = tk.Tk()
ROOT.option_add('*font', 'Helvetica -30')
Window = Frame(ROOT)
TextWidget = Text(Window)
TextWidget.pack()
Window.pack()
TextWidget.focus_set()
ROOT.withdraw()

segs = []
preds = []
for root,dirs,video_segments in os.walk('./segments/'):
    for i in idxs:
            # subprocess.call([opener, 'segments/IMG_4654-{}-subs.mp4'.format(i)])
        segs.append('segments/IMG_4654-{}-subs.mp4'.format(i))
    # subprocess.call(["mpv", '--fs', '--loop-file=inf'] + segs)    

    for i in idxs:
        subprocess.call(["mpv", '--fs', '--sid=no'] + ['segments/IMG_4654-{}-subs.mp4'.format(i)])
        inp = MyDialog(ROOT, "Enter word guess for segment {}: \n".format(i)).result
        with open('segments/IMG_4654-seg-{}.srt'.format(i)) as f:
            contents = f.read()
            print(contents)
            if inp and not inp.isspace() and (inp in contents or inp.lower() in contents or inp.capitalize() in contents):
                preds.append(1)
            else:
                preds.append(0)
print(preds)
# calculate and print WER
print("WER (% of correctly guessed words): {}".format(len([i for i in preds if i == 1]) / len(preds)))
