from TokenType import TokenType
from NumberNode import NumberNode
from BinaryOperationNode import BinaryOperationNode
from InvalidSyntaxError import InvalidSyntaxError
from UnaryOperationNode import UnaryOperationNode
from ParseResult import ParseResult
from VariableAccessNode import VariableAccessNode
from VariableAssignNode import VariableAssignNode

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.token_index = -1
		self.advance()

	def advance(self, ):
		self.token_index += 1
		if self.token_index < len(self.tokens):
			self.current_token = self.tokens[self.token_index]
		return self.current_token



	def parse(self):
		result = self.expression()
		if not result.error and self.current_token.token_type != TokenType.ENDFILE:
			return result.failure(InvalidSyntaxError(
				self.current_token.position_start, self.current_token.position_end,
				"Expected '+', '-', '*', '/', '^', '==', '!=', '<', '>', <=', '>=', 'AND' or 'OR'"
			))
		return result

	def atom(self):
		result = ParseResult()
		token = self.current_token

		if token.token_type in (TokenType.INTEGER, TokenType.FLOAT):
			result.register_advancement()
			self.advance()
			return result.success(NumberNode(token))

		elif token.token_type == TokenType.IDENTIFIER:
			result.register_advancement()
			self.advance()
			return result.success(VariableAccessNode(token))

		elif token.token_type == TokenType.LPAREN:
			result.register_advancement()
			self.advance()
			express = result.register(self.expression())
			if result.error: return result
			if self.current_token.token_type == TokenType.RPAREN:
				result.register_advancement()
				self.advance()
				return result.success(express)
			else:
				return result.failure(InvalidSyntaxError(
					self.current_token.position_start, self.current_token.position_end,
					"Expected ')'"
				))

		return result.failure(InvalidSyntaxError(
			token.positioin_start, token.position_end,
			"Expected int, float, identifier, '+', '-', '('"
		))

	def power(self):
		return self.binary_operation(self.atom, (TokenType.POW, ), self.factor)


	def factor(self):
		result = ParseResult()
		token = self.current_token

		if token.token_type in (TokenType.PLUS, TokenType.MINUS):
			result.register_advancement()
			self.advance()
			factor = result.register(self.factor())
			if result.error: return result
			return result.success(UnaryOperationNode(token, factor))

		return self.power()
	
	def term(self):
		return self.binary_operation(self.factor, (TokenType.MUL, TokenType.DIV))

	def arithmetical_expression(self):
		return self.binary_operation(self.term,(TokenType.PLUS,TokenType.MINUS))
	def comparison_expression(self):
		result = ParseResult()

		if self.current_token.matches(TokenType.KEYWORD, 'NOT'):
			operation_token = self.current_token
			result.register_advancement()
			self.advance()

			node = result.register(self.comparison_expression())
			if result.error: return result
			return result.success(UnaryOperationNode(operation_token, node))
		
		node = result.register(self.binary_operation(self.arithmetical_expression, (TokenType.EQUALSEQUALS, TokenType.NOTEQUALS,TokenType.LESSTHAN, TokenType.GREATERTHAN, TokenType.LESSTHANEQUALS, TokenType.GREATERTHANEQUALS)))
		
		if result.error:
			return result.failure(InvalidSyntaxError(
				self.current_token.position_start, self.current_token.position_end,
				"Expected int, float, identifier, '+', '-', '(' or 'NOT'"
			))

		return result.success(node)

	def expression(self):
		result = ParseResult()

		if self.current_token.matches(TokenType.KEYWORD, 'VAR'):
			result.register_advancement()
			self.advance()

			if self.current_token.token_type != TokenType.IDENTIFIER:
				return result.failure(InvalidSyntaxError(
					self.current_token.position_start, self.current_token.position_end,
					"Expected identifier"
				))

			var_name = self.current_token
			result.register_advancement()
			self.advance()

			if self.current_token.token_type != TokenType.EQUALS:
				return result.failure(InvalidSyntaxError(
					self.current_token.position_start, self.current_token.position_end,
					"Expected '='"
				))

			result.register_advancement()
			self.advance()
			expr = result.register(self.expression())
			if result.error: return result
			return result.success(VariableAssignNode(var_name, expr))

		node = result.register(self.binary_operation(self.comparison_expression, ((TokenType.KEYWORD, 'AND'), (TokenType.KEYWORD, 'OR'))))

		if result.error:
			return result.failure(InvalidSyntaxError(
				self.current_token.position_start, self.current_token.position_end,
				"Expected 'VAR', int, float, identifier, '+', '-', '(' or 'NOT'"
			))

		return result.success(node)

	def binary_operation(self, func_a, operators, func_b=None):
		if func_b == None:
			func_b = func_a
		
		result = ParseResult()
		left = result.register(func_a())
		if result.error: return result

		while self.current_token.token_type in operators or (self.current_token.token_type, self.current_token.token_value) in operators:
			operator_token = self.current_token
			result.register_advancement()
			self.advance()
			right = result.register(func_b())
			if result.error: return result
			left = BinaryOperationNode(left, operator_token, right)

		return result.success(left)
