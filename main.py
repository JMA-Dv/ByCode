import Lexer
from Parser import Parser
from Token import Token
from IllegalCharError import IllegalCharError
while True:
    text = input('Compiler> ')
    
    result,error = Lexer.run('<file> ',text)
    
    if error: 
        print(error.as_string())
    elif result: 
        print(result)