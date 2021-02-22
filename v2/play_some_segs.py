import argparse
import os
from random import shuffle
import subprocess, sys
from sys import platform
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


parser = argparse.ArgumentParser(description='args for playing phoneme segments')
parser.add_argument('--range', '-r', type=int, nargs=2,
                    help='start and end integer range of videos to select. In form start end')
parser.add_argument('--train', '-t', action='store_true', help='enables training mode')
parser.add_argument('--numreps', '-nr', type=int, nargs=1, help='number of repetitions of phonemes during training')
parser.add_argument('--shuffle', '-s', action='store_true', help='shuffles videos randomly')
parser.add_argument('--fname', '-f', type=str, default="", help='name heading of results logfile')

args = parser.parse_args()

if not args.train and args.numreps:
    parser.error('--numreps can only be set when --train flag is enabled.')

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

def pop_up():
    ROOT = tk.Tk()
    ROOT.option_add('*font', 'Helvetica -30')
    Window = Frame(ROOT)
    TextWidget = Text(Window)
    TextWidget.pack()
    Window.pack()
    
    if platform == "linux" or platform == "linux2":
        ROOT.focus_force()
    elif platform == "darwin":
        Window.after(1, lambda: Window.focus_force())

    TextWidget.focus_set()
    ROOT.withdraw()
    return ROOT

segs = []
preds = []
cor_words = []
inc_words = []

if args.shuffle:
    shuffle(idxs)

for root,dirs,video_segments in os.walk('./segments/'):
    if args.train:
        for i in idxs:
            # subprocess.call([opener, 'segments/IMG_4654-{}-subs.mp4'.format(i)])
            for n in range(args.numreps[0]):
                segs.append('segments/IMG_4654-{}-subs.mp4'.format(i))
        subprocess.call(["mpv", '--fs'] + segs)    
    else:
        for i in idxs:
            subprocess.call(["mpv", '--fs', '--sid=no'] + ['segments/IMG_4654-{}-subs.mp4'.format(i)])
            ROOT = pop_up()
            inp = MyDialog(ROOT, "Enter word guess for segment {}: \n".format(i)).result
            with open('segments/IMG_4654-seg-{}.srt'.format(i)) as f:
                contents = f.read()
                print(contents)
                if inp and not inp.isspace() and (inp in contents or inp.lower() in contents or inp.capitalize() in contents):
                    preds.append(1)
                    cor_words.append(inp)
                else:
                    preds.append(0)
                    inc_words.append(inp)
with open('{}_{}-{}.log'.format(args.fname, args.range[0], args.range[1]), 'w') as f:
    f.write("correct: \n {} \nincorrect: \n {}".format(cor_words, inc_words))

prev_WER = None

with open('running_WER.log', 'r') as f:
    for line in f.readlines():
        prev_WER = float(line)

instance_WER = len([i for i in preds if i == 1]) / len(preds)

if prev_WER is not None:
    running_WER = (prev_WER + instance_WER) / 2
else:
    running_WER = instance_WER


with open('summary.log', 'a') as f:
    f.write("{} range {} - {}\ncorrect: \n {} \nincorrect: \n {}\ninstance WER: {}\nrunning WER: {}".format(args.fname, args.range[0], args.range[1], cor_words, inc_words, instance_WER, running_WER))

print(preds)

# calculate and print WER
print("WER (% of correctly guessed words in range {} - {}): {}".format(args.range[0], args.range[1], instance_WER))
print("Running WER: {}".format(running_WER))

with open('running_WER.log', 'w') as f:
    f.write(running_WER)
print("{} range {} - {}\ncorrect: \n {} \nincorrect: \n {}\n".format(args.fname, args.range[0], args.range[1], cor_words, inc_words))
