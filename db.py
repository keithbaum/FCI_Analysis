from tinydb import TinyDB, Query
import os

class DB( object ):
    def __init__(self, path):
        try:
            self.db = TinyDB( path )
        except:
            raise ValueError('Cannot Initialize DB')

    def addDayTable(self, FCIsCollection, aDate):
        tableName = 'FCIs'+aDate.strftime('%Y-%m-%d')
        self.db.table( tableName )
