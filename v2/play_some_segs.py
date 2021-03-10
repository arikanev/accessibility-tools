import argparse
import os
from pathlib import Path
from random import shuffle
from spellchecker import SpellChecker
import subprocess, sys
from sys import platform
import time
import tkinter as tk
from tkinter import simpledialog
from tkinter import *

class MyDialog(simpledialog.Dialog):

    def body(self, master):
        self.geometry("800x600")
        tk.Label(master, text="What did Awesome Person just say?").grid(row=0)

        self.e1 = tk.Entry(master)
        self.e1.grid(row=0, column=1)
        return self.e1 # initial focus

    def apply(self):
        first = self.e1.get()
        self.result = first


def train(vid, mod_tr=False):

    if mod_tr:

        for i in idxs:
            for n in range(args.numreps):
                segs.append('--{')
                segs.append('--sid=no')
                segs.append('segments/{}-{}-subs.mp4'.format(vid, i))
                segs.append('--}')
                segs.append('segments/{}-{}-subs.mp4'.format(vid, i))
        subprocess.call(["mpv", '--fs'] + segs)

        '''
        for i in idxs:
            for n in range(args.numreps):

                subprocess.call(["mpv", '--fs'] + ['segments/{}-{}-subs.mp4'.format(vid, i)])
                time.sleep(.2)
                subprocess.call(["mpv", '--fs', '--sid=no'] + ['segments/{}-{}-subs.mp4'.format(vid, i)])
                time.sleep(.2)
        '''

    else:
        for i in idxs:
            for n in range(args.numreps):
                segs.append('segments/{}-{}-subs.mp4'.format(vid, i))
        subprocess.call(["mpv", '--fs'] + segs)


def test(vid):

    spell = SpellChecker()

    for i in idxs:

        try:

            subprocess.call(["mpv", '--fs', '--sid=no'] + ['segments/{}-{}-subs.mp4'.format(vid, i)])
            ROOT = pop_up()
            inp = MyDialog(ROOT, "Enter word guess for segment: \n").result
            with open('segments/{}-seg-{}.srt'.format(vid, i)) as f:
                contents = f.readlines()[2].lower()
                print(contents)

                misspelled = spell.unknown([inp])

                if len(misspelled) > 0:
                    inp = spell.correction(list(misspelled)[0])

                if inp.lower() == contents:
                    preds.append(1)
                    cor_words.append(inp)
                else:
                    preds.append(0)
                    inc_words.append("incorrect: {} | correct: {}".format(inp, contents))
        except FileNotFoundError:

            continue

    score()


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


def score():

    with open('{}_{}_{}-{}.log'.format(args.fname, args.vname, args.range[0], args.range[1]), 'w') as f:
        f.write("correct: \n {} \nincorrect: \n {}".format(cor_words, inc_words))

    prev_acc = None

    N = 0

    if os.path.isfile('running_acc.log'):
        with open('running_acc.log', 'r') as f:
            for line in f.readlines():
                prev_acc = float(line)
                N += 1
    else:
        Path('running_acc.log').touch()
    instance_acc = len([i for i in preds if i == 1]) / len(preds)

    if prev_acc is not None:
        running_acc = ((prev_acc * N) + instance_acc) / (N + 1)
    else:
        running_acc = instance_acc


    with open('{}_summary.log'.format(args.fname), 'a') as f:
        f.write("\n{} {} range {} - {}\ncorrect: \n {} \nincorrect: \n {}\ninstance acc: {}\nrunning acc: {}".format(args.fname, args.vname, args.range[0], args.range[1], cor_words, inc_words, instance_WER, running_WER))

    print(preds)

    # calculate and print WER
    print("acc (% of correctly guessed words in range {} - {}): {}".format(args.range[0], args.range[1], instance_acc))
    print("Running acc: {}".format(running_acc))

    with open('running_acc.log', 'a') as f:
        f.write(str(running_acc) + '\n')

    print("\n{} {} range {} - {}\ncorrect: \n {} \nincorrect: \n {}\n".format(args.fname, args.vname, args.range[0], args.range[1], cor_words, inc_words))




parser = argparse.ArgumentParser(description='args for playing phoneme segments')
parser.add_argument('--range', '-r', type=int, nargs=2, default=[0, 10], help='start and end integer range of videos to select. In form start end')
parser.add_argument('--train', '-tr', action='store_true', help='enables training mode')
parser.add_argument('--trainm', '-trm', action='store_true', help='enables modified training mode')
parser.add_argument('--test', '-t', action='store_true', help='enables testing mode')
parser.add_argument('--numreps', '-nr', type=int, nargs=1, default=1, help='number of repetitions of phonemes during training')
parser.add_argument('--shuffle', '-s', action='store_true', help='shuffles videos randomly')
parser.add_argument('--vname', '-v', type=str, default="all", help='name heading of video file')
parser.add_argument('--fname', '-f', type=str, default="haptic", help='name heading of results logfile')
parser.add_argument('--idxs', '-i', type=int, nargs='+', help='indices of specific video segments to select. If used, overrides range argument')

args = parser.parse_args()

idxs = []


if args.idxs:
    for i in args.idxs:
        idxs.append(i)

else:
    for i in range(args.range[0], args.range[1]):
        idxs.append(i)


segs = []
preds = []
cor_words = []
inc_words = []

if args.shuffle:
    shuffle(idxs)

if type(args.numreps) == list:
    args.numreps = args.numreps[0]

vids = []

for file in os.listdir("./vids/"):
    if file.endswith(".MOV"):
        vids.append(file.strip(".MOV"))

if args.vname == "all":
    for vid in vids:
        if args.train and args.test:
            train(vid, mod_tr=args.trainm)
            test(vid)
        elif args.train:
            train(vid, mod_tr=args.trainm)
        elif args.test:
            test(vid)
else:
    if args.train and args.test:
        train(args.vname, mod_tr=args.trainm)
        test(args.vname)
    elif args.train:
        train(args.vname, mod_tr=args.trainm)
    elif args.test:
        test(args.vname)
