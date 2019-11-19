from RunTimeError import RunTimeError
from TokenValue import TokenValue
class Number(TokenValue):
    def __init__(self, value):
        super().__init__()
        self.value = value
        #self.set_position()
        self.set_context()


    def added_to(self,other): #method for adding value to other +
        if isinstance(other,Number):##just to check if is only numbers
            return Number(self.value + other.value).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)

    def subbed_to(self,other):
        if isinstance(other,Number):##just to check if is only numbers
            return Number(self.value - other.value).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)
        

    def multiplied_by(self,other): #method for adding value to other +
        if isinstance(other,Number):##just to check if is only numbers
            return Number(self.value * other.value).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)


    def divided_by(self,other): #method for adding value to other +
        if isinstance(other,Number):##just to check if is only numbers
            if other.value ==0:
                return None, RunTimeError(other.position_start,other.position_end,
                'Division by zero',self.context)
            
            return Number(self.value / other.value).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)

    
    def powed_by(self,other):
        if isinstance(other, Number):
            return Number(self.value** other.value).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)

    def get_comparison_equals(self,other):
        if isinstance(other,Number):
            return Number(int(self.value == other.value)).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)


    def get_comparison_not_equals(self,other):
        if isinstance(other,Number):
            return Number(int(self.value != other.value)).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)
    
    def get_comparison_less_than(self,other):
        if isinstance(other,Number):
            return Number(int(self.value < other.value)).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)
    
    def get_comparison_greater_than(self,other):
        if isinstance(other,Number):
            return Number(int(self.value > other.value)).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)

    def get_comparison_less_than_equals(self,other):
        if isinstance(other,Number):
            return Number(int(self.value <= other.value)).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)

    def get_comparison_greater_than_equals(self,other):
        if isinstance(other,Number):
            return Number(int(self.value >= other.value)).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)

    def notted(self):
        return Number(1 if self.value ==0 else 0).set_context(self.context),None

    def andedd_by(self,other):
        if isinstance(other,Number):
            return Number(int(self.value and other.value)).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)
    def orted_by(self,other):
        if isinstance(other,Number):
            return Number(int(self.value or other.value)).set_context(self.context),None
        else:
            return None,TokenValue.illegal_operation(self.position_start,other.position_end)

    def is_true(self):
        return self.value != 0
    
    def copy(self):
        copy = Number(self.value)
        copy.set_position(self.position_start,self.position_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)