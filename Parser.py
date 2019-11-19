from CallNode import CallNode
from FunctionDefinitionNode import FunctionDefinitionNode
from ForNode import ForNode
from WhileNode import WhileNode
from IfNode import IfNode
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

		elif token.matches(TokenType.KEYWORD,'IF'):
			if_expression = result.register(self.if_expression())
			if result.error: return result
			return result.success(if_expression)

		elif token.matches(TokenType.KEYWORD,'FOR'):
			for_expression = result.register(self.for_expression())
			if result.error: return result
			return result.success(for_expression)

		elif token.matches(TokenType.KEYWORD,'WHILE'):
			while_expression = result.register(self.while_expression())
			if result.error: return result
			return result.success(while_expression)

		elif token.matches(TokenType.KEYWORD,'FUN'):
			function_definition = result.register(self.function_definition())
			if result.error: return result
			return result.success(function_definition)



		return result.failure(InvalidSyntaxError(
			token.position_start, token.position_end,
			"Expected int, float, identifier, '+', '-', '(' 'IF', 'FOR', 'WHILE','FUN'"
		))

	def power(self):
		return self.binary_operation(self.call, (TokenType.POW, ), self.factor)

	def call(self):
		result = ParseResult()
		atom = result.register(self.atom())
		if result.error:return result

		if self.current_token.token_type == TokenType.LPAREN:
			result.register_advancement()
			self.advance()
			argument_nodes = []
			
			if self.current_token.token_type == TokenType.RPAREN:
				result.register_advancement()
				self.advance()
			else:
				argument_nodes.append(result.register(self.expression()))
				
				if result.error:
    					return result.failure(InvalidSyntaxError(
							self.current_token.positioin_start,
							self.current_token.position_end,
							"Expected ')', 'VAR', 'IF,'FOR', 'WHILE', 'FUN', 'INTEGER',FLOAT, 'IDENTIFIER'"
						))

				while self.current_token.token_type == TokenType.COMMA:
					result.register_advancement()  
					self.advance()

					argument_nodes.append(result.register(self.expression()))
					if result.error: return result

				if self.current_token.token_type != TokenType.RPAREN:
					return result.failure(InvalidSyntaxError(
						self.current_token.position_start,
						self.current_token.positioin_end,
						f"Expected ',' or ')'"
					))

				result.register_advancement()
				self.advance()
			return result.success(CallNode(atom,argument_nodes))
		return result.success(atom)
	

	def if_expression(self):
		result = ParseResult()
		cases = []
		else_cases = None

		if not self.current_token.matches(TokenType.KEYWORD,'IF'):
			return result.failure(InvalidSyntaxError(
				self.current_token.positioin_start,self.current_token.position_end,
				f"Expected 'IF'"
			))

		result.register_advancement()
		self.advance()

		condition = result.register(self.expression())
		if result.error: return result

		if not self.current_token.matches(TokenType.KEYWORD,'THEN'):
			return result.failure(InvalidSyntaxError(
				self.current_token.positioin_start,self.current_token.positioin_end,
				f"Expected 'THEN' KEYWORD"
			))
		
		result.register_advancement()
		self.advance()

		expression = result.register(self.expression())
		if result.error: return result
		cases.append((condition,expression))

		while self.current_token.matches(TokenType.KEYWORD,'ELIF'):
			result.register_advancement()
			self.advance()

			condition = result.register(self.expression())
			if result.error: return result 

			if not self.current_token.matches(TokenType.KEYWORD,'THEN'):
				return result.failure(InvalidSyntaxError(
					self.current_token.position_start,self.current_token.positioin_end,
					f"Expected 'THEN'"
				))
			
			result.register_advancement()
			self.advance()
			expression = result.register(self.expression())
			if result.error: return result
			cases.append((condition,expression))

		if self.current_token.matches(TokenType.KEYWORD,'ELSE'):
			result.register_advancement()
			self.advance()

			else_cases = result.register(self.expression())
			if result.error: return result

		return result.success(IfNode(cases,else_cases))


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
				"Expected 'VAR','IF', 'FOR', 'WHILE','FUN', int, float, identifier, '+', '-', '(' or 'NOT'"
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

	def for_expression(self):
		result = ParseResult()
		if not self.current_token.matches(TokenType.KEYWORD,'FOR'):
			return result.failure(InvalidSyntaxError(
				self.current_token.position_start,
				self.current_token.position_end,
				f"Expected 'FOR' structure"
			))

		result.register_advancement()
		self.advance()
		if self.current_token.token_type != TokenType.IDENTIFIER:
			return result.failure(InvalidSyntaxError(
				self.current_token.position_start,
				self.current_token.position_end,
				f"Expected identifier"
			))
		variable_name = self.current_token
		result.register_advancement()
		self.advance()

		if self.current_token.token_type != TokenType.EQUALS:
			return result.failure(InvalidSyntaxError(
				self.current_token.position_start,
				self.current_token.position_end,
				f"Expected '=' Token "
			))
		result.register_advancement()
		self.advance()

		start_value = result.register(self.expression())
		if result.error: return result
		
		if not self.current_token.matches(TokenType.KEYWORD,'TO'):
			return result.failure(InvalidSyntaxError(
				self.current_token.position_start,
				self.current_token.position_end,
				f"Expected 'TO' KEYWORD "
			))
		
		result.register_advancement()
		self.advance()

		end_value = result.register(self.expression())
		if result.error: return result

		if self.current_token.matches(TokenType.KEYWORD,'STEP'):
			result.register_advancement()
			self.advance()

			step_value = result.register(self.expression())
			if result.error: return result
		else:
			step_value = None

		if not self.current_token.matches(TokenType.KEYWORD,'THEN'):
			return result.failure(InvalidSyntaxError(
				self.current_token.position_start,
				self.current_token.position_end,
				f"Expected 'THEN' KEYWORD "
			))


		result.register_advancement()
		self.advance()

		body = result.register(self.expression())
		if result.error:return result

		return result.success(ForNode(variable_name,start_value,end_value,step_value,body))

		
	def while_expression(self):
		result = ParseResult()

		if not self.current_token.matches(TokenType.KEYWORD,'WHILE'):
				return result.failure(InvalidSyntaxError(
				self.current_token.position_start,
				self.current_token.position_end,
				f"Expected 'WHILE' KEYWORD "
			))
		result.register_advancement()
		self.advance()

		condition = result.register(self.expression())
		if result.error: return result

		if not self.current_token.matches(TokenType.KEYWORD,'THEN'):
			return result.failure(InvalidSyntaxError(
				self.current_token.position_start,
				self.current_token.position_end,
				f"Expected 'THEN' KEYWORD "
			))

		result.register_advancement()
		self.advance()

		body = result.register(self.expression())

		if result.error: return result

		return result.success(WhileNode(condition,body))

	def function_definition(self):
		result = ParseResult()

		if not self.current_token.matches(TokenType.KEYWORD,'FUN'):
			return result.failure(InvalidSyntaxError(
				self.current_token.position_start,self.current_token.position_end,
				f"Expecrted 'FUN'"
			))

		result.register_advancement()
		self.advance()

		if self.current_token.token_type == TokenType.IDENTIFIER:
			variable_name = self.current_token
			result.result_advancement()
			self.advance()
			if self.current_token.token_type != TokenType.LPAREN:
				return result.failure(InvalidSyntaxError(
					self.current_token.position_start,self.current_token.position_end,
					f"Expected '('"
				))

	def function_definition(self):
		result = ParseResult()

		if not self.current_token.matches(TokenType.KEYWORD,'FUN'):
			return result.failure(InvalidSyntaxError(
				self.current_token.position_start,
				self.current_token.position_end,
				f"Espected 'FUN' token"
			))
		result.register_advancement()
		self.advance()

		if self.current_token.token_type == TokenType.IDENTIFIER:
			variable_name = self.current_token
			result.register_advancement()
			self.advance()
			if self.current_token.token_type  != TokenType.LPAREN:
				return result.failure(InvalidSyntaxError(
					self.current_token.position_start,
					self.current_token.position_end,
					f"Expected ' ( '"
				))

		else:
			variable_name = None
			if self.current_token.token_type != TokenType.LPAREN:
				return result.failure(InvalidSyntaxError(
					self.current_token.position_start,
					self.current_token.position_end,
					f"Expected 'IDENTIFIER' or '()'"
				))

		result.register_advancement()
		self.advance()
		arguments_name_token = []

		if self.current_token.token_type == TokenType.IDENTIFIER:
			arguments_name_token.append(self.current_token)
			self.advance()

			while self.current_token.token_type == TokenType.COMMA:
				result.register_advancement()
				self.advance()

				if self.current_token.token_type != TokenType.IDENTIFIER:
					return result.failure(InvalidSyntaxError(
						self.current_token.position_start,
						self.current_token.position_end,
						f"Expected identifier"
					))

			arguments_name_token.append(self.current_token)
			result.register_advancement()
			self.advance()

			if self.current_token.token_type != TokenType.RPAREN:
				return result.failure(InvalidSyntaxError(
					self.current_token.position_start,
					self.current_token.position_end,
					f"Expected ',' or ')' token"
				))

		else:
			if self.current_token.token_type != TokenType.RPAREN:
				return result.failure(InvalidSyntaxError(
					self.current_token.position_start,
					self.current_token.position_end,
					f"Expected 'IDENTIFIER' or ')'"
				))

		result.register_advancement()
		self.advance()

		if self.current_token.token_type != TokenType.ARROW:
			return result.failure(InvalidSyntaxError(
					self.current_token.position_start,
					self.current_token.position_end,
					f"Expected ' -> ' symbol"
			))

		result.register_advancement()
		self.advance()
		node_to_return = result.register(self.expression())
		if result.error: return result

		return result.success(FunctionDefinitionNode(
			variable_name,
			arguments_name_token,
			node_to_return 
		))