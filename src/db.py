import sqlite3

class PlayOnDownloaderDb:
    def __init__(self, filepath: str):
        self.con = sqlite3.connect(filepath)
        self.cur = self.con.cursor()
        self.__initialize_db()

    def __initialize_db(self) -> None:
        self.__execute('CREATE TABLE IF NOT EXISTS "files" ("name" STRING, "releaseYear" STRING)')
        self.__execute('CREATE UNIQUE INDEX IF NOT EXISTS "file_index" ON files("name", "releaseYear")')

    def __execute(self, sql: str) -> None:
        try:
            self.con.execute(sql)
        except:
            print('There has been a problem running the sql')
            print(sql)
            exit(1)

    def hasFile(self, name: str, year: str) -> bool:
        if year is None:
            self.cur.execute('SELECT * FROM "files" WHERE name = ? AND releaseYear IS NULL', (name,))
        else:
            self.cur.execute('SELECT * FROM "files" WHERE name = ? AND releaseYear = ?', (name, year))
        return (self.cur.fetchone() is not None)

    def addFile(self, name: str, year: str) -> None:
        try:
            if year is None:
                self.cur.execute('INSERT INTO "files" VALUES (?, NULL)', (name,))
            else:
                self.cur.execute('INSERT INTO "files" VALUES (?, ?)', (name, year))
            self.con.commit()
        except:
            print(f'Could not add "{name}" ({year})')
            exit(1)
