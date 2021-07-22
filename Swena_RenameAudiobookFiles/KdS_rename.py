import glob
import eyed3.mp3

# select files and modify properties
files = glob.glob('*.mp3')
for idx, file in enumerate(files):
    f = eyed3.mp3.Mp3AudioFile(file)
    f.initTag()
    tag = f.tag
    tag.track_num = idx
    tag.title = tag.album.split(' ')[-1] + ' ' + tag.title
    tag.album = 'Harry Potter und die Kammer des Schreckens'
    tag.artist = 'J.K. Rowling'
    tag.save()
