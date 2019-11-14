class ForNode:
    #variable name = variable in the for
    #start value = value that will start
    #end valud = the end of the iteration
    #
    def __init__(self,variable_name,start_value_node,end_value_node,step_value_node, body_node):
        self.variable_name_token = variable_name
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

        self.position_start = self.variable_name_token.position_start
        self.position_end = self.body_node.position_end



