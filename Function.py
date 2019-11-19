from SymbolTable import SymbolTable
from Context import Context
from RunTimeResult import RunTimeResult
from TokenValue import TokenValue
from  RunTimeError import RunTimeError
import  Interpreter

class Function(TokenValue):
    def __init__(self,name,body_node,argument_names):
        super().__init__()
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arguments_names = argument_names

    def execute(self,arguments):
        result = RunTimeResult()
        interpreter  = Interpreter.Interpreter()

        new_context = Context(self.name,self.context,self.position_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        if len(arguments) < len(self.arguments_names):
            return result.failure(RunTimeError(self.position_start,self.position_end,
            f"{len(self.arguments_names) - len(arguments)} too few arguments passed into '{self.name}' ",self.context))

        if len(arguments) > len(self.arguments_names):
            return result.failure(RunTimeError(self.position_start,self.position_end,
            f"{len(self.arguments_names) - len(arguments)} too many arguments passed into '{self.name}' ",self.context))

        for i in range(len(arguments)):
            argument_name = self.arguments_names[i]
            argument_value = arguments[i]
            argument_value.set_context(new_context)
            new_context.symbol_table.set(argument_name,argument_value)

        value = result.register(interpreter.visit(self.body_node,new_context))
        if result.error: return result
        return result.success(value)

    def copy(self):
        copy = Function(self.name,self.body_node,self.arguments_names)
        copy.set_context(self.context)
        copy.set_position(self.position_start,self.position_end)
        return copy

    def __repr__(self):
        return f"<finction {self.name}>"
