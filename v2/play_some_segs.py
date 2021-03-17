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

    ok_button = None
    repeat_button = None
    skip_button = None

    def __init__(self, ROOT, text, spell=SpellChecker(language=None), vid=None):
        self.spell = spell
        self.spell.word_frequency.load_text_file('./tables/{}.table'.format(vid))
        super().__init__(ROOT, text)

    def body(self, master):
        self.geometry("800x800")
        tk.Label(master, text="What did speaker just say?").grid(row=0)

        self.e1 = tk.Entry(master)
        self.e1.grid(row=0, column=1)

        return self.e1

    def apply(self):
        first = self.e1.get()
        if len(first) == 0:
            self.skip()
        else:
            self.result = first

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return


        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()


    def skip(self, event=None):
        self.result = "user-skip"
        self.destroy()

    def repeat(self, event=None):
        self.result= "user-repeat"
        self.destroy()

    def validate(self):
        init_inp = self.e1.get()

        if len(init_inp) > 0:
            self.e1.delete(0, tk.END)
            inp = self.spell.correction(init_inp)
            self.e1.insert(0, inp)

            if inp == init_inp:
                return 1

            elif inp != init_inp:
                return 0

        return 1

    def buttonbox(self):
        '''add standard button box.
        override if you do not want the standard buttons
        '''

        box = Frame(self)

        self.ok_button = Button(box, text="OK (enter)", width=11, command=self.ok, default=ACTIVE)
        self.ok_button.pack(side=LEFT, padx=5, pady=5)
        self.repeat_button = Button(box, text="Repeat (space)", width=15, command=self.repeat)
        self.repeat_button.pack(side=LEFT, padx=5, pady=5)
        self.skip_button = Button(box, text="Skip (esc)", width=11, command=self.skip)
        self.skip_button.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<space>", self.repeat)
        self.bind("<Escape>", self.skip)

        box.pack()


def train(vid, idxs, preds, cor_words, inc_words, mod_tr=False, wc=False, segs=[]):

    segs = []

    if mod_tr:

        if wc:

            for i in idxs:
                for n in range(args.numreps):
                    segs.append('--{')
                    segs.append('--sid=no')
                    segs.append('segments/{}-{}-subs.mp4'.format(vid, i))
                    segs.append('--}')
                    segs.append('segments/{}-{}-subs.mp4'.format(vid, i))
                    subprocess.call(["mpv", '--fs'] + segs)
                    inp = input("Please enter 'c' if your guess was correct, 'w' if it was wrong: ")
                    if inp == 'c':
                       preds.append(1)
                    elif inp == 'w':
                       preds.append(0)
                    segs = []
            score(vid, idxs, cor_words, inc_words, trainm=True)
            preds = []

        else:

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


def test(vid, idxs, numreps, preds, cor_words, inc_words):

    for i in idxs:

        try:

            subprocess.call(["mpv", '--fs', '--sid=no'] + ['segments/{}-{}-subs.mp4'.format(vid, i)])
            ROOT = pop_up()
            inp = MyDialog(ROOT, "Enter word guess for segment: \n", vid=vid).result

            print(inp)

            while inp == "user-repeat":
                numreps += 1
                subprocess.call(["mpv", '--fs', '--sid=no'] + ['segments/{}-{}-subs.mp4'.format(vid, i)])
                ROOT = pop_up()
                inp = MyDialog(ROOT, "Enter word guess for segment: \n", vid=vid).result

            if inp == "user-skip":
               preds.append(0)
               with open('segments/{}-seg-{}.srt'.format(vid, i)) as f:
                   contents = f.readlines()[2].lower()
                   print(contents)

               inc_words.append("incorrect: {} | correct: {} | num reps: {}".format(inp, contents, numreps))
               numreps = 0

            else:
               with open('segments/{}-seg-{}.srt'.format(vid, i)) as f:
                   contents = f.readlines()[2].lower()
                   print(contents)

                   if inp.lower() == contents:
                       preds.append(1)
                       cor_words.append("{} | num reps: {}".format(inp, numreps))
                   else:
                       preds.append(0)
                       inc_words.append("incorrect: {} | correct: {} | num reps: {}".format(inp, contents, numreps))
               numreps = 0

        except FileNotFoundError:

            continue

    score(vid, idxs, cor_words, inc_words, trainm=False)

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


def score(vid, idxs, cor_words, inc_words, trainm):

    r1, r2  = idxs[0], idxs[len(idxs)-1]

    if trainm:

        acc = len([i for i in preds if i == 1]) / len(preds)

        print("acc for modified training: {}".format(acc))

        with open('training_{}_{}_{}-{}.txt'.format(args.fname, vid, r1, r2), 'w') as f:
            f.write("acc: {}".format(acc))

    else:

        with open('{}_{}_{}-{}.txt'.format(args.fname, vid, r1, r2), 'w') as f:
            f.write("correct: \n {} \nincorrect: \n {}".format(cor_words, inc_words))

        acc = len([i for i in preds if i == 1]) / len(preds)

        with open('{}_summary.txt'.format(args.fname), 'a') as f:
            f.write("\n{} {} range {} - {}\ncorrect: \n {} \nincorrect: \n {}\n acc: {}".format(args.fname, vid, r1, r2, cor_words, inc_words, acc))

        print(preds)

        # calculate and print WER
        print("acc (% of correctly guessed words in range {} - {}): {}".format(r1, r2, acc))

        print("\n{} {} range {} - {}\ncorrect: \n {} \nincorrect: \n {}\n".format(args.fname, vid, r1, r2, cor_words, inc_words))


parser = argparse.ArgumentParser(description='args for playing phoneme segments')
parser.add_argument('--range', '-r', type=int, nargs=2, help='start and end integer range of videos to select. In form start end')
parser.add_argument('--train', '-tr', action='store_true', help='enables training mode')
parser.add_argument('--trainm', '-trm', action='store_true', help='enables modified training mode')
parser.add_argument('--test', '-t', action='store_true', help='enables testing mode')
parser.add_argument('--numreps', '-nr', type=int, nargs=1, default=1, help='number of repetitions of phonemes during training')
parser.add_argument('--shuffle', '-s', action='store_true', help='shuffles videos randomly')
parser.add_argument('--vname', '-v', type=str, default='all', help='name heading of video file')
parser.add_argument('--fname', '-f', type=str, default="lipread", help='name heading of results logfile')
parser.add_argument('--idxs', '-i', type=str, help='indices of specific video segments to select. If used, overrides range argument')
parser.add_argument('--vidxs', '-vi', type=str, help='indices of specific video segments to select across all video files specified. If used, overrides idxs argument.')
parser.add_argument('--wcor', '-wc', action='store_true', help='modified training mode will include some testing features (warm up)')

args = parser.parse_args()


if args.vidxs:
    vidxs = {}
    for i, vi in enumerate(args.vidxs):

        try:

            if vi == 'v':
                cur_vid_idx = int(args.vidxs[i + 1])
                vidxs.update({cur_vid_idx:[]})

            elif vi == 's' and args.vidxs[i + 2].isdigit():
                vidxs[cur_vid_idx].append(int(args.vidxs[i + 1] + args.vidxs[i + 2]))
            elif vi == 's' and not args.vidxs[i + 2].isdigit():
                vidxs[cur_vid_idx].append(int(args.vidxs[i + 1]))

        except IndexError:

           vidxs[cur_vid_idx].append(int(args.vidxs[i + 1]))

elif args.idxs:
    idxs = []
    for i in args.idxs:
        idxs.append(i)

else:
    for i in range(args.range[0], args.range[1]):
        idxs.append(i)

if args.shuffle:
    shuffle(idxs)

if type(args.numreps) == list:
    args.numreps = args.numreps[0]



if vidxs:
    for vid, idxs in vidxs.items():

        numreps = 0
        segs = []
        preds = []

        cor_words, inc_words = [], []

        if args.train and args.test:
            train(vid, idxs, preds, cor_words, inc_words, args.trainm, args.wcor)
            test(vid, idxs, numreps, preds, cor_words, inc_words)
        elif args.train:
            train(vid, idxs, preds, cor_words, inc_words, args.trainm, args.wcor)
        elif args.test:
            test(vid, idxs, numreps, preds, cor_words, inc_words)

elif args.vname == "all":
    vids = []

    for file in os.listdir("./vids/"):
        if file.endswith(".MOV"):
            vids.append(file.strip(".MOV"))

    for vid in vids:

        cor_words, inc_words = [], []

        if args.train and args.test:
            train(vid, idxs, preds, cor_words, inc_words, args.trainm, args.wcor)
            test(vid, idxs, numreps, preds, cor_words, inc_words)
        elif args.train:
            train(vid, idxs, preds, cor_words, inc_words, args.trainm, args.wcor)
        elif args.test:
            test(vid, idxs, numreps, preds, cor_words, inc_words)

else:
    if args.train and args.test:
        train(args.vname, idxs, preds, cor_words, inc_words, args.trainm, args.wcor)
        test(args.vname, idxs, numreps, preds, cor_words, inc_words)
    elif args.train:
        train(args.vname, idxs, preds, cor_words, inc_words, args.trainm, args.wcor)
    elif args.test:
        test(args.vname, idxs, numreps, preds, cor_words, inc_words)
