class UnaryOperationNode:
    def __init__(self, operation_token, node):
        self.operation_token = operation_token
        self.node = node

        self.position_start = self.operation_token.position_start
        self.position_end = node.position_end
        
    def __repr__(self):
        return f'({self.operation_token}, {self.node})'