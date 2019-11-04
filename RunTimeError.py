import Error
from arrows import *
class RunTimeError(Error.Error):
    def __init__(self,position_start, position_end, details,context):
        super().__init__(position_start, position_end,'Runtime Error ', details)
        self.context = context
        

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}\n'
        result +='\n\n' + arrows(self.position_start.file_text, self.position_start, self.position_end)
        return result
            
    def generate_traceback(self):
        result =''
        position = self.position_start
        contex = self.context

        while contex:
            result = f'  File{position.file_name}, line {str(position.line+1)},in {contex.display_name}\n'+result 
            position = contex.parent_entry_position
            contex = contex.parent
        
        return 'Traceback (most recent call last):\n '+ result