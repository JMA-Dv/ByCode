class WhileNode:
    def __init__(self, condition,body_node):
        self.condition = condition
        self.body_node = body_node
        self.position_start = condition.position_start
        self.position_end = body_node.position_end
