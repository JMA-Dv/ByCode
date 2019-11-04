import Error
class InvalidSyntaxError(Error.Error):
    def __init__(self,position_start, position_end, details=''):
        super().__init__(position_start, position_end,'Syntaxis invalida', details)