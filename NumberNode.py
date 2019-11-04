class NumberNode:
    def __init__(self, token):
        self.token=token

        self.position_start = token.position_start
        self.position_end = token.position_end


    def __repr__(self):
        return f'{self.token}'
    