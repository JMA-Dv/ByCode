from SymbolTable import SymbolTable
from IllegalCharError import IllegalCharError
from Position import Position
from Token import Token
from TokenType import TokenType
from Parser import Parser
from Number import Number
from Interpreter import Interpreter
from Context import Context
from ExpectedCharError import ExpectedCharError
#refactored
class Lexer:
    
	def __init__(self, file_name, text):
		self.file_name = file_name
		self.text = text
		self.position = Position(-1, 0, -1, file_name, text)
		self.current_char = None
		self.advance()
	
	def advance(self):
		self.position.advance(self.current_char)
		self.current_char = self.text[self.position.index] if self.position.index < len(self.text) else None

	def make_tokens(self):
		tokens = []

		while self.current_char != None:
			if self.current_char in ' \t':
				self.advance()
			elif self.current_char in TokenType.DIGITS:
				tokens.append(self.make_number())
			elif self.current_char in TokenType.LETTERS:
				tokens.append(self.make_identifier())
			elif self.current_char == '+':
				tokens.append(Token(TokenType.PLUS, position_start=self.position))
				self.advance()
			elif self.current_char == '-':
				tokens.append(self.make_minus_or_arrow())
				self.advance()
			elif self.current_char == '*':
				tokens.append(Token(TokenType.MUL, position_start=self.position))
				self.advance()
			elif self.current_char == '/':
				tokens.append(Token(TokenType.DIV, position_start=self.position))
				self.advance()
			elif self.current_char == '^':
				tokens.append(Token(TokenType.POW, position_start=self.positon))
				self.advance()
			elif self.current_char == '(':
				tokens.append(Token(TokenType.LPAREN, position_start=self.position))
				self.advance()
			elif self.current_char == ')':
				tokens.append(Token(TokenType.RPAREN, position_start=self.position))
				self.advance()
			elif self.current_char == '!':
				token, error = self.make_not_equals()
				if error: return [], error
				tokens.append(token)
			elif self.current_char == '=':
				tokens.append(self.make_equals())
			elif self.current_char == '<':
				tokens.append(self.make_less_than())
			elif self.current_char == '>':
				tokens.append(self.make_greater_than())
			elif self.current_char == ',':
				tokens.append(Token(TokenType.COMMA, position_start=self.position))
				self.advance()
			else:
				pos_start = self.position.copy()
				char = self.current_char
				self.advance()
				return [], IllegalCharError(pos_start, self.position, "'" + char + "'")

		tokens.append(Token(TokenType.ENDFILE, position_start=self.position))
		return tokens, None

	def make_number(self):
		num_string = ''
		dot_count = 0
		position_start = self.position.copy()

		while self.current_char != None and self.current_char in TokenType.DIGITS + '.':
			if self.current_char == '.':
				if dot_count == 1: break
				dot_count += 1
			num_string += self.current_char
			self.advance()

		if dot_count == 0:
			return Token(TokenType.INTEGER, int(num_string), position_start, self.position)
		else:
			return Token(TokenType.FLOAT, float(num_string), position_start, self.position)

	def make_identifier(self):
		id_string = ''
		position_start = self.position.copy()

		while self.current_char != None and self.current_char in TokenType.LETTERS_DIGITS  + '_':
			id_string += self.current_char
			self.advance()

		token_type = TokenType.KEYWORD if id_string in TokenType.KEYWORDS else TokenType.IDENTIFIER
		return Token(token_type, id_string, position_start, self.position)

	def make_not_equals(self):
		position_start = self.position.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			return Token(TokenType.NOTEQUALS, position_start=position_start, position_end=self.position), None

		self.advance()
		return None, ExpectedCharError(position_start, self.position, "'=' (after '!')")
	
	def make_equals(self):
		token_type = TokenType.EQUALS
		position_start = self.position.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			token_type = TokenType.EQUALSEQUALS

		return Token(token_type, position_start=position_start, position_end=self.position)

	def make_less_than(self):
		token_type = TokenType.LESSTHAN
		position_start = self.position.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			token_type = TokenType.LESSTHANEQUALS

		return Token(token_type, position_start=position_start, position_end=self.position)

	def make_greater_than(self):
		token_type = TokenType.GREATERTHAN
		position_start = self.position.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			token_type = TokenType.GREATERTHANEQUALS

		return Token(token_type, position_start=position_start, position_end=self.position)
	
	def make_minus_or_arrow(self):
		token_type = TokenType.MINUS
		position_start = self.position.copy()
		self.advance()

		if self.current_char == '>':
			self.advance()
			token_type = TokenType.ARROW


		return Token(token_type,position_start = position_start,position_end=self.position)



		

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number(0))
global_symbol_table.set("FALSE", Number(0))
global_symbol_table.set("TRUE", Number(1))

def run (file,text):
	lexer = Lexer(file,text)
	tokens,error = lexer.make_tokens()
	if error: return None,error
	
	#abstract syntax tree
	parser = Parser(tokens)
	abstract_st = parser.parse()
	if abstract_st.error: return None,abstract_st.error

	#run program
	interpreter  = Interpreter()
	context = Context('<basic context>')
	context.symbol_table=global_symbol_table
	result = interpreter.visit(abstract_st.node,context)
	return result.value,result.error


