class BinaryOperationNode:
    def __init__(self, left_node, operation_token, right_node):
            self.left_node = left_node
            self.operation_token = operation_token 
            self.right_node = right_node

            self.position_start = self.left_node.position_start
            self.position_end = self.right_node.position_end


    def __repr__(self):
        return f'({self.left_node}, {self.operation_token}, {self.right_node})'