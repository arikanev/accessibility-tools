import datetime
import re
import math
import argparse

length_regexp = 'Duration: (\d{2}):(\d{2}):(\d{2})\.\d+,'
re_length = re.compile(length_regexp)

from subprocess import check_call, PIPE, Popen
import shlex

def get_sec(time_str):
    """Get Seconds from time."""
    try:
        m, s= time_str.split(':')
    except:
        return int(time_str)
    return int(m) * 60 + int(s)

def main():
    filename, table = parse_args()

    split_length = []
    subtitle = []

    with open(table, 'r') as f:
        for line in f.readlines():

            split_length.append(get_sec(line.split()[4]) - get_sec(line.split()[2]))
            subtitle.append(line.split()[1])

            # split_length.append(get_sec(line.split()[6]) - get_sec(line.split()[4]))
            # subtitle.append(" ".join([line.split()[1], line.split()[2], line.split()[3]]))

    p1 = Popen(["ffmpeg", "-i", filename], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    # get p1.stderr as input
    output = Popen(["grep", 'Duration'], stdin=p1.stderr, stdout=PIPE, universal_newlines=True)
    p1.stdout.close()
    matches = re_length.search(output.stdout.read())
    # print(output.stdout.read())
    if matches:
        video_length = int(matches.group(1)) * 3600 + \
                       int(matches.group(2)) * 60 + \
                       int(matches.group(3))
        print("Video length in seconds: {}".format(video_length))
    else:
        print("Can't determine video length.")
        raise SystemExit

    split_count = len(split_length)

    '''
    if split_count == 1:
        print("Video length is less than the target split length.")
        raise SystemExit
    '''

    for n in range(split_count):
        split_start = sum(split_length[:n])
        pth, ext = filename.rsplit(".", 1)
        pth = "segments/" + pth
        cmd = "ffmpeg -i {} -vcodec copy  -strict -2 -ss {} -t {} {}-{}.{}".\
            format(filename, split_start, split_length[n], pth, n, ext)
        print("About to run: {}".format(cmd))
        check_call(shlex.split(cmd), universal_newlines=True)

        if subtitle[n] != "START":
            f = open("{}-seg-{}.srt".format(pth, n), "w")
            f.write('{}\n{}\n{}'.format(1, str(datetime.timedelta(milliseconds=0)) + ",000" + " --> " + str(datetime.timedelta(milliseconds=split_length[n])) + ",000" , subtitle[n]))
            f.close()
            cmd = "ffmpeg -i {}-{}.{} -i {} -c copy -c:s mov_text {}-{}-{}.{}".format(pth, n, ext, "{}-seg-{}.srt".format(pth, n), pth, n, "subs", "mp4")
            print("About to run: {}".format(cmd))
            check_call(shlex.split(cmd), universal_newlines=True)

def parse_args():

    parser = argparse.ArgumentParser(description='args for vid splitting')

    parser.add_argument("-f", "--file", help="file to split, for example sample.avi", type=str)

    parser.add_argument("-t", "--table", help="table to use for splitting video into segments", type=str)

    args = parser.parse_args()

    return args.file, args.table

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
