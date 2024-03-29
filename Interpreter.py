from RunTimeResult import RunTimeResult
from TokenType import TokenType
from Number import Number
from RunTimeError import RunTimeError
#refactored
class Interpreter:
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
            result, error = left.multed_by(right)
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

    def visit_UnaryOpNode(self, node, context):
        response = RunTimeResult()
        number = response.register(self.visit(node.node, context))
        if response.error: return response

        error = None

        if node.operation_token.token_type == TokenType.MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.operation_token.matches(TokenType.KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return response.failure(error)
        else:
            return response.success(number.set_position(node.position_start, node.position_end))