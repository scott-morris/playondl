import os
import sys
import sqlite3
from settings import Config

rootpath = os.path.dirname(__file__)
sys.path.append(os.path.join(rootpath, 'src'))

from app import PlayOn
from db import PlayOnDownloaderDb

settings = Config()
app = PlayOn()
db = PlayOnDownloaderDb(os.path.join(rootpath, 'playondb.sqlite'))

app.login(settings.username, settings.password)
list = app.getDownloadList()

for file in list:
    name = file['Name']
    year = file['ReleaseYear']

    title = name 
    
    if year is not None:
        title += f' ({year})'

    if db.hasFile(name, year):
        print(f'{title} already downloaded. Skipping...')
    else:
        file = app.download(file['ID'], title)
        db.addFile(name, year)

