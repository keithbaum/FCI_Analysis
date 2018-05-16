import urllib.request, json
import datetime
from fci import FCIsCollection
from pprint import pprint

class Scrapper:
    def getFCIsCollection( self, aDate ):
        url = self.generateUrlAddress( aDate )
        parser = self.urlParser()
        try:
            urlResponse = urllib.request.urlopen(url).read().decode()
            parsed = parser( urlResponse )
        except:
            return self.emptyCollection()

        data = parsed.get('data') if isinstance( parsed, dict ) else None 
        return self.transformJSONToFCIsCollection( data ) if data else self.emptyCollection()

    def transformJSONToFCIsCollection( self, data ):
        collection = FCIsCollection()
        for node in data:
            collection.addNode( node )
        return collection.asDict

    @staticmethod
    def emptyCollection():
        return {}

    @staticmethod
    def urlParser():
        return json.loads
    
    @staticmethod
    def generateUrlAddress( aDate ):
        return "https://api.cafci.org.ar/estadisticas/informacion/diaria/2/" + aDate.strftime('%Y-%m-%d')




pprint( Scrapper().getFCIsCollection( datetime.date(2018,5,10) ) )