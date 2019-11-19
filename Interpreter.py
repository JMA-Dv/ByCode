from Function import Function
from RunTimeResult import RunTimeResult
from TokenType import TokenType
from Number import Number
from RunTimeError import RunTimeError
#refactored
class Interpreter:
    def __init__(self):
        pass

    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
         raise Exception(f'No visit_{type(node).__name__} method defined')

    ###################################

    def visit_NumberNode(self, node, context):
        return RunTimeResult().success(
            Number(node.token.token_value).set_context(context).set_position(node.position_start, node.position_end)
        )

    def visit_VariableAccessNode(self, node, context):
        res = RunTimeResult()
        var_name = node.variable_name_token.token_value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RunTimeError(
                node.position_start, node.position_end,
                f"'{var_name}' is not defined",
                context
            ))

        value = value.copy().set_position(node.position_start, node.position_end)
        return res.success(value)

    def visit_VariableAssignNode(self, node, context):
        result = RunTimeResult()
        variabl_name = node.variable_name_token.token_value
        value = result.register(self.visit(node.value_node, context))
        if result.error: return result

        context.symbol_table.set(variabl_name, value)
        return result.success(value)

    def visit_BinaryOperationNode(self, node, context):
        response = RunTimeResult()
        left = response.register(self.visit(node.left_node, context))
        if response.error: return response
        right = response.register(self.visit(node.right_node, context))
        if response.error: return response

        if node.operation_token.token_type == TokenType.PLUS:
            result, error = left.added_to(right)
        elif node.operation_token.token_type == TokenType.MINUS:
            result, error = left.subbed_by(right)
        elif node.operation_token.token_type == TokenType.MUL:
            result, error = left.multiplied_by(right)
        elif node.operation_token.token_type == TokenType.DIV:
            result, error = left.dived_by(right)
        elif node.operation_token.token_type == TokenType.POW:
            result, error = left.powed_by(right)
        elif node.operation_token.token_type == TokenType.EQUALSEQUALS:
            result, error = left.get_comparison_equals(right)
        elif node.operation_token.token_type == TokenType.NOTEQUALS:
            result, error = left.get_comparison_not_equals(right)
        elif node.operation_token.token_type == TokenType.LESSTHAN:
            result, error = left.get_comparison_less_than(right)
        elif node.operation_token.token_type == TokenType.GREATERTHAN:
            result, error = left.get_comparison_greater_than(right)
        elif node.operation_token.token_type == TokenType.LESSTHANEQUALS:
            result, error = left.get_comparison_less_than_equals(right)
        elif node.operation_token.token_type == TokenType.GREATERTHANEQUALS:
            result, error = left.get_comparison_greater_than_equals(right)
        elif node.operation_token.matches(TokenType.KEYWORD, 'AND'):
            result, error = left.anded_by(right)
        elif node.operation_token.matches(TokenType.KEYWORD, 'OR'):
            result, error = left.ored_by(right)

        if error:
            return response.failure(error)
        else:
            return response.success(result.set_position(node.position_start, node.position_end))

    def visit_UnaryOperationNode(self, node, context):
        response = RunTimeResult()
        number = response.register(self.visit(node.node, context))
        if response.error: return response

        error = None

        if node.operation_token.token_type == TokenType.MINUS:
            number, error = number.multiplied_by(Number(-1))
        elif node.operation_token.matches(TokenType.KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return response.failure(error)
        else:
            return response.success(number.set_position(node.position_start, node.position_end))

    def visit_IfNode(self,node,context):
        result = RunTimeResult()

        for condition,expression in node.cases:
            condition_value = result.register(self.visit(condition,context))
            if result.error: return result

            if condition_value.is_true():
                expression_value = result.register(self.visit(expression,context))
                if result.error: return result
                return result.success(expression_value)

        if node.else_case:
            else_value = result.register(self.visit(node.else_case,context))
            if result.error: return result
            return result.success(else_value)

        return result.success(None)
 
    def visit_ForNode(self,node,context):
        result = RunTimeResult()

        start_value = result.register(self.visit(node.start_value_node,context))
        if result.error: return result

        end_value = result.register(self.visit(node.end_value_node,context))
        if result.error: return result

        
        if node.step_value_node:
            step_value = result.register(self.visit(node.step_value_node,context))
            if result.error: return result
        else:
            step_value = Number(1)

        i =  start_value.value#watch this

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.variable_name_token.token_value,Number(i))
            i += step_value.value

            result.register(self.visit(node.body_node,context))
            if result.error: return result

        return result.success(None)
            
    def visit_FunctionDefinitionNode(self,node,context):
        result = RunTimeResult()

        function_name = node.variable_name.token_value if node.variable_name else None
        body_node = node.body_node
        argument_names = [argument_name.token_value for argument_name in node.argument_name]
        function_value = Function(function_name,body_node,argument_names).set_context(context).set_position(node.position_start,node.position_end)

        if node.variable_name:
            context.symbol_table.set(function_name,function_value)

        return result.success(function_value)

    def visit_CallNode(self,node,context):
        result = RunTimeResult()
        arguments = []

        value_to_call = result.register(self.visit(node.node_to_call,context))
        if result.error: return result

        value_to_call = value_to_call.copy().set_position(node.position_start,node.position_start)

        for argument_node in node.arguments_node:
            arguments.append(result.register(self.visit(argument_node,context)))
            if result.error: return result

        return_value = result.register(value_to_call.execute(arguments))
        if result.error: return result
        return result.success(return_value)





    def visit_WhileNode(self,node,context):
        result = RunTimeResult()

        while True:
            condition = result.register(self.visit(node.condition,context))
            if result.error: return result

            if not condition.is_true():break

            result.register(self.visit(node.body_node,context))
            if result.error: return result

        return result.success(None)
