class CallNode:
    def __init__(self,node_to_call,arguments_nodes):
        self.node_to_call = node_to_call
        self.arguments_node = arguments_nodes

        self.position_start = self.node_to_call.position_start

        if len(self.arguments_node) > 0:
            self.position_end = self.arguments_node[len(self.arguments_node) - 1].position_end
        else:
            self.position_end = self.node_to_call.position_end
            


        