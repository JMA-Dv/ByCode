from RunTimeError import RunTimeError
class Number:
    def __init__(self, value):
        self.value = value
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
        if isinstance(other,Number):##just to check if is only numbers
            return Number(self.value + other.value).set_context(self.context),None

    def subbed_to(self,other):
        if isinstance(other,Number):##just to check if is only numbers
            return Number(self.value - other.value).set_context(self.context),None

    def multiplied_by(self,other): #method for adding value to other +
        if isinstance(other,Number):##just to check if is only numbers
            return Number(self.value * other.value).set_context(self.context),None

    def divided_by(self,other): #method for adding value to other +
        if isinstance(other,Number):##just to check if is only numbers
            if other.value ==0:
                return None, RunTimeError(other.position_start,other.position_end,
                'Division by zero',self.context)
            
        return Number(self.value / other.value).set_context(self.context),None
    
    def powed_by(self,other):
        if isinstance(other, Number):
            return Number(self.value** other.value).set_context(self.context),None

    def get_comparison_equals(self,other):
        if isinstance(other,Number):
            return Number(int(self.value == other.value)).set_context(self.context),None

    def get_comparison_not_equals(self,other):
        if isinstance(other,Number):
            return Number(int(self.value != other.value)).set_context(self.context),None
    
    def get_comparison_less_than(self,other):
        if isinstance(other,Number):
            return Number(int(self.value < other.value)).set_context(self.context),None
    
    def get_comparison_greater_than(self,other):
        if isinstance(other,Number):
            return Number(int(self.value > other.value)).set_context(self.context),None

    def get_comparison_less_than_equals(self,other):
        if isinstance(other,Number):
            return Number(int(self.value <= other.value)).set_context(self.context),None

    def get_comparison_greater_than_equals(self,other):
        if isinstance(other,Number):
            return Number(int(self.value >= other.value)).set_context(self.context),None

    def notted(self):
        return Number(1 if self.value ==0 else 0).set_context(self.context),None

    def andedd_by(self,other):
        if isinstance(other,Number):
            return Number(int(self.value and other.value)).set_context(self.context),None
    def orted_by(self,other):
        if isinstance(other,Number):
            return Number(int(self.value or other.value)).set_context(self.context),None

    
    def copy(self):
        copy = Number(self.value)
        copy.set_position(self.position_start,self.position_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)