#here i keep track of  all variable names and values 
class SymbolTable:
    def __init__(self,parent=None):
        self.symbols={}#dictionary
        self.parent = parent #dictionary for all symbol table
        
    def get(self,name):
        value = self.symbols.get(name,None)
        if value == None and self.parent:
            
            return self.parent.get(name)
        return value

    def set(self,name,value):
        
        self.symbols[name]=value
    
    def remove(self,name):
        del self.symbols[name]

