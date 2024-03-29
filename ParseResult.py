import ParseResult
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None 
        self.advance_count = 0  #keep track of when it is not advance

    def register_advancement(self):
        self.advance_count += 1

    #def register(self, result):
    #   self.advance_count += result.advance_count
    #  if result.error: self.error = result.error
    # return result.node

    def register(self, result):
        self.advance_count += result.advance_count
        if result.error: self.error = result.error
        return result.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:  #if so should override
            self.error = error
        return self