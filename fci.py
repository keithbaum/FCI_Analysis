import datetime

class FCIsCollection( object ):

    def __init__(self):
        self.currentCategory = []
        self._collection = {'Data':{}}

    def addNode( self, node ):
        if self.isCategoryNode( node ):
            self.addCategory( node, not self.isCurrentCategoryFull() )
        else:
            self.addDataNode( node )

    @staticmethod
    def isCategoryNode( node ):
        return 'fecha' not in node
    
    def isCurrentCategoryFull(self):
        if not self.currentCategory:
            return True
        catNode = self.lookForPath( self.currentCategory )
        total = self.sumTotalsForCategory ( catNode )
        return total == catNode.get('patrimonio')

    @staticmethod
    def upperCategory( category ):
        return category[:-1] if category else []

    def addCategory(self, node, isSubcategory):
        newCategory = node['fondo']
        if isSubcategory:
            currCatNode = self.lookForPath( self.currentCategory )
            self.currentCategory = self.currentCategory + [ newCategory ]
        else:
            currCatNode = self.lookForPath( self.upperCategory( self.currentCategory ) )
            self.currentCategory = self.upperCategory( self.currentCategory )+ [ newCategory ]

        currCatNode.get('Data').update( { newCategory : { 'patrimonio':node['patrimonio'], 'Data':{} } } )

    def addDataNode(self, node):
        newCategory = node['fondo']
        currCatNode = self.lookForPath( self.currentCategory )
        currCatNode.get('Data').update( { newCategory : node } )


    def lookForPath(self, path):
        collection = self._collection
        for node in path:
            collection = collection.get( 'Data' ).get ( node )
        return collection

    def sumTotalsForCategory( self, node ):
        if not self.isCategoryNode( node ):
            return float( node['patrimonio'] ) if node['patrimonio'] else 0
        else:
            return sum( [ self.sumTotalsForCategory( nodei ) for nodei in node['Data'].values() ] )

    def _flatten(self,node,path,result={}):
        if 'Data' in node:
            for k,v in node['Data'].items():
                newPath=path+[k]
                result.update( self._flatten(v,newPath,result) )
        else:
            node.update( { 'Categoria' : path[:-1] } )
            key = node.get('fondo','NoName'+(datetime.datetime.now().strftime("%s")))
            node.pop('fondo', None)
            result.update( { key:node } )

        return result
            
    def _flattenedCollection(self):
        return self._flatten( self._collection, [] )

    @property
    def asDict(self):
        return self._flattenedCollection()
