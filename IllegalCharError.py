import Error
class IllegalCharError(Error.Error):   
    def __init__(self,position_start, position_end, details):
        super().__init__(position_start, position_end,'Caracter ilegal', details)