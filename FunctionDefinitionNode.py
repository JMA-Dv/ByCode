class FunctionDefinitionNode:
    def __init__(self,variable_name,argument_name,body_node):
        self.variable_name = variable_name
        self.argument_name = argument_name
        self.body_node = body_node
        if self.variable_name:
            self.position_start = self.variable_name.position_start
        elif len(self.argument_name) > 0:
            self.position_start = self.argument_name[0].position_start
        else:
            self.position_start = self.body_node.position_start
        

        self.position_end = self.body_node.position_end

        