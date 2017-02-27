'''
	compiler design mini project
	mini compielr for c written in python
	focus on while loops

	tokenizer to tokenize input C code
	uses python re module

	input: C code
	output: tokens as tuples
'''
import sys
import re

scanner = re.Scanner([
	# comment
	(r'//.*?(\r\n?|\n)|/\*.*?\*/', None),

	# keywords
	(r'auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|return|short|signed|sizeof|static|struct|switch|switch|typedef|union|unsigned|void|volatile|while', lambda scanner, token: ('KEYWORD', token)),

	(r'[0-9]+', lambda scanner, token: ('INT', token)),

	# parentheses
	(r'\(|\{', lambda scanner, token: ('OPEN_PAREN', token)),
	(r'\)|\}', lambda scanner, token: ('CLOSE_PAREN', token)),

	# string
	#(r'\*?(\*\*)?[A-Za-z_][A-Za-z0-9_]*', lambda scanner, token: ('IDENTIFIER', token)),	
	(r'[A-Za-z_][A-Za-z0-9_]*', lambda scanner, token: ('IDENTIFIER', token)),
	(r'\"(\\.|[^\\"])*\"', lambda scanner, token: ('LITERAL', token[1:-1])),
	#(r'(\"\\.|[^\\"]*\")', lambda scanner, token: ('LITERAL', token[1:-1])),
	
	# operators
	(r'\.\.\.', lambda scanner, token: ('ELLIPSIS', token)),
	(r'\+=', lambda scanner, token: ('ADD_ASSIGN', token)),
	(r'-=', lambda scanner, token: ('SUB_ASSIGN', token)),
	(r'\*=', lambda scanner, token: ('MUL_ASSIGN', token)),
	(r'/=', lambda scanner, token: ('DIV_ASSIGN', token)),
	(r'%=', lambda scanner, token: ('MOD_ASSIGN', token)),
	(r'\+\+', lambda scanner, token: ('INC_OP', token)),
	(r'--', lambda scanner, token: ('DEC_OP', token)),
	(r'->', lambda scanner, token: ('PTR_OP', token)),
	(r'&&', lambda scanner, token: ('AND_OP', token)),
	(r'\|\|', lambda scanner, token: ('OR_OP', token)),
	(r'<=', lambda scanner, token: ('LE_OP', token)),
	(r'>=', lambda scanner, token: ('GE_OP', token)),
	(r'==', lambda scanner, token: ('EQ_OP', token)),
	(r'!=', lambda scanner, token: ('NE_OP', token)),
	(r';', lambda scanner, token: ('TERMINATOR', token)),
	(r',', lambda scanner, token: ('SEPERATOR', token)),
	(r'=', lambda scanner, token: ('ASSIGN_OP', token)),
	(r'\+', lambda scanner, token: ('ADD_OP', token)),
	(r'-', lambda scanner, token: ('SUB_OP', token)),
	(r'/', lambda scanner, token: ('ADD_OP', token)),

	# currently unknown
	(r'\*', lambda scanner, token: ('STAR', token)),

	# whitespace
	(r'( |\n|\t)*', None),
])


if __name__ == '__main__':
	li = []
	
	with open('test_input.txt') as f:
		test_input = f.readlines()

	for line in range(0, len(test_input)):
		for thing in scanner.scan(test_input[line]):
			for token in thing:
				li.append(list(token) + [line])

	for i in li:
		print(i)