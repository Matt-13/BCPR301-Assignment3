# Code passes the PEP8 Check. 4/04/19
# Created by Liam Brydon
import sqlite3


class DataBase:

    def __init__(self, database='assignment.db'):   # pragma: no cover
        self.database = database
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):   # pragma: no cover
        self.conn = sqlite3.connect(self.database)
        print("Finishing connecting to database")

        self.cursor = self.conn.cursor()

    """
    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
    """

    def create_table(self):   # pragma: no cover
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS savedCode(
        codeID INTEGER PRIMARY KEY AUTOINCREMENT,
        timeStamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        code LONGTEXT)""")
        self.conn.commit()

    def data_entry(self, code):   # pragma: no cover
        out = ''

        self.cursor.execute("""INSERT INTO
         savedCode (code) values(?)""", (code,))
        self.cursor.execute("""SELECT MAX(codeID) FROM
         savedCode""")
        max_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT codeID FROM "
                            "savedCode WHERE codeID = (?)", (max_id,))
        identification = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT timeStamp FROM "
                            "savedCode WHERE codeID = (?)", (max_id,))
        time_stamp = self.cursor.fetchone()[0]

        out += "Successfully Submitted to database: \n" + \
               "\tID = {}\n".format(identification - 1) + \
               "\tTimeStamp = {}\n".format(str(time_stamp))
        print(out)
        self.conn.commit()

    def get_code(self, code_id):   # pragma: no cover
        out = ''
        self.cursor.execute("""SELECT MAX(codeID)
         FROM savedCode""")
        max_id = self.cursor.fetchone()[0]
        if int(code_id) >= max_id or int(code_id) <= 0:
            out = "ID doesnt exists in table"
        else:
            self.cursor.execute("SELECT code FROM "
                                "savedCode WHERE codeID = (?)", (code_id,))
            out = self.cursor.fetchone()[0]
        return out
