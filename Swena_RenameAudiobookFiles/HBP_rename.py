import glob
import eyed3.mp3

# select files and modify properties
files = glob.glob('*.mp3')
for file in files:
    f = eyed3.mp3.Mp3AudioFile(file)
    f.initTag()
    tag = f.tag
    (trackno, title) = file.split(' - ')
    tag.track_num = trackno
    tag.album = 'Harry Potter und der Halbblutprinz'
    tag.artist = 'J.K. Rowling'
    tag.title = title[:-4]
    tag.save()
