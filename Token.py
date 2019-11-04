from Position import Position
class Token:
        def __init__(self,type_, value=None, position_start=None,position_end=None):
            self.token_type = type_
            self.token_value = value
        
            #print('Position start ', str(position_start))
        
            if position_start:
                
                self.position_start=position_start.copy()
                #for ar in dir(position_start):
                 #   print(ar,getattr(position_start,ar))
                    
                self.position_end=position_start.copy()
                self.position_end.advance()

            if position_end:
                self.position_end = position_end
      

        def matches(self,type_,value):
            if self.token_type == type_ and self.token_value == value:
                return (self.token_type and self.token_value)
            #return self.type==type_ and self.value==value


        def __repr__(self):
            if self.token_value: return f'{self.token_type}:{self.token_value}'
            return f'{self.token_type}'