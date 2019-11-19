from RunTimeError import RunTimeError
class TokenValue:
    def __init__(self):
        self.set_position()
        self.set_context()

    def set_position(self,position_start=None,position_end=None):
        self.position_start=position_start
        self.position_end=position_start
        return self

    def set_context(self,context=None):
        self.context = context
        return self

    def added_to(self,other): #method for adding value to other +
        return None,self.illegal_operation(other)

    def subbed_to(self,other):
        return None,self.illegal_operation(other)

    def multiplied_by(self,other): #method for adding value to other +
        return None,self.illegal_operation(other)
            

    def divided_by(self,other): #method for adding value to other +
        return None,self.illegal_operation(other)
    
    def powed_by(self,other):
        return None,self.illegal_operation(other)

    def get_comparison_equals(self,other):
        return None,self.illegal_operation(other)

    def get_comparison_not_equals(self,other):
        return None,self.illegal_operation(other)
    
    def get_comparison_less_than(self,other):
        return None,self.illegal_operation(other)
    
    def get_comparison_greater_than(self,other):
        return None,self.illegal_operation(other)

    def get_comparison_less_than_equals(self,other):
        return None,self.illegal_operation(other)

    def get_comparison_greater_than_equals(self,other):
        return None,self.illegal_operation(other)

    def notted(self):
        return None,self.illegal_operation()

    def execute(self):
        return None,self.illegal_operation()

    def copy(self):
        raise Exception('No  copy method defined')
    
    def is_true(self):
        return False
    
    def  illegal_operation(self,other = None):
        if not other:  
            other = self
        return RunTimeError(self.position_start,other.position_end,
        'Illegal operation',
        self.context)


