import os
from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=qTqfptkcpcY')
# yt = YouTube('https://www.dailymotion.com/video/x5e87lo')

yt.streams \
  .filter(progressive=True, file_extension='mp4') \
  .order_by('resolution') \
  .desc() \
  .first() \
  .download()

os.rename('Jolly Phonics 42 letter sounds.mp4', 'jolly_phonics.mp4')
