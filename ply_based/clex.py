#!usr/bin/env python
# @Author: Suhas Kashyap
# @Date: 2017-03-20

# Compiler design mini-project
# Mini compielr for c written in python
# Emphasis on while loops

# clex.py

import sys
import re
import ply.lex as lex
from pprint import pprint

token_set = [[]]
count = 0
h = 0

keywords = [
	'auto',
	'break',
	'case',
	'char',
	'const',
	'continue',
	'default',
	'do',
	'double',
	'enum',
	'extern',
	'for',
	'goto',
	'main',
	'long',
	'register',
	'return',
	'short',
	'signed',
	'sizeof',
	'static',
	'struct',
	'switch',
	'typedef',
	'union',
	'unsigned',
	'void',
	'volatile',
	'while',
	]

builtin = [
	'scanf',
	'getc',
	'gets',
	'getchar',
	'puts',
	'putchar',
	'fopen',
	'fclose',
	'putc',
	'fputc',
	'fgets',
	'fputs',
	'fgetc',
	'feof',
	'fgetchar',
	'fprintf',
	'fscanf',
	'fputchar',
	'strncat',
	'strlen',
	'strcat',
	'strcmp',
	'strcmpi',
	'malloc',
	'calloc',
	'realloc',
	'free',
	'exit',
	'floor',
	'ceil',
	'round',
	'sin',
	'cos',
	'exp',
	'log',
	'pow',
	'time',
	]
	

def t_DIRECTIVE(t):
	r'\#include<[a-z]*.h>'
	return t

def t_RELOP(t):
	r'==|>=|>|<=|<|!='
	return t

def t_WHILE(t):
	r'while'
	return t

def t_PRINT(t):
	r'printf'
	return t

def t_INT(t):
	r'int'
	return t

def t_FLOAT(t):
	r'float'
	return t

def t_CHAR(t):
	r'char'
	return t

def t_MAIN(t):
	r'main'
	return t

def t_RETURN(t):
	r'return'
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	if keywords.count(t.value):
		t.type = 'KEYWORD'
	elif builtin.count(t.value):
		t.type = 'BUILTIN'
	else:
		t.type = 'ID'
	return t


# List of token names
tokens = [
	'NUMBER',
	'ADD',
	'SUBTRACT',
	'MULTIPLY',
	'DIVIDE',
	'SEP',
	'EQUALS',
	'COMPEQ',
	'COMPGT',
	'COMPGE',
	'COMPLT',
	'COMPLE',
	'COMPNE',
	'LPAREN',
	'RPAREN',
	'LFPAREN',
	'RFPAREN',
	'LBPAREN',
	'RBPAREN',
	'STRING',
	'ID',
	'KEYWORD',
	'BUILTIN',
	'PLUS',
	'TIMES',
	'MINUS',
	'WHILE',
	'PRINT',
	'INT',
	'FLOAT',
	'RELOP',
	'DECL',
	'MAIN',
	'RETURN',
	'DIRECTIVE',
	'HEADER',
	'FNUMBER',
	'CHARACTER',
	'CHAR',
	'COMMA',
	]


# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_SEP = r';'
t_LBPAREN = r'\['
t_RBPAREN = r'\]'
t_LFPAREN = r'{'
t_RFPAREN = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r"="
t_COMMA = r','

			
# A regular expression rule with some action code
def t_FNUMBER(t):
	r'\d+.\d'
	t.value = float(t.value)
	return t

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_CHARACTER(t):
	r"""'.'"""
	return t

# Define a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_COMMENT(t):
	r'//.*?(\r\n?|\n)|/\*.*?\*/'
	pass
	# No return value. Token discarded

def t_STRING(t):
	r'".*"'
	return t

t_ignore = ' \t'

def t_error(t):
	print('Illegal character ' + t.value[0])
	t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
new_data = open(sys.argv[1]).read()

lexer.input(new_data)
token_set = [[]*100]
count = 0
token_table = []
while True:
	tok = lexer.token()
	if not tok:
		break
	else:
		if tok.value == '{':
			token_set.append([])
			#print(token_set)
			token_set[count].append(tok)
			token_table.append(tok)
			count+=1
		elif tok.value=='}':
			count-=1
			token_set[count].append(tok)
			token_table.append(tok)
		else:
			token_set[count].append(tok)
			token_table.append(tok)


symbol_table = []

# symbol symbol_table contents = 'data type' , 'token name' , 'token value' , 'line number'

i = 0
length = len(token_table)
while i < length:
	some = []
	if token_table[i].type == 'ID' and (token_table[i
			- 1].type == 'INT' or token_table[i - 1].type
			== 'FLOAT' or token_table[i - 1].type == 'CHAR'):
		some.append(token_table[i - 1].value)
		some.append(token_table[i].value)
		if token_table[i + 1].type == 'EQUALS':
			some.append(token_table[i + 2].value)
			some.append(token_table[i].lineno)
			i += 3
		else:
			if token_table[i - 1].type == 'INT':
				some.append(0)
			elif token_table[i - 1].type == 'FLOAT':
				some.append(0.0)
			elif token_table[i - 1].type == 'CHAR':
				some.append('0')
			some.append(token_table[i].lineno)
			i += 1
		symbol_table.append(some)
	elif token_table[i].type == 'PRINT':
		j = i + 1
		count = 0
		some.append('PRINT')
		while token_table[j].type != 'RPAREN':
			if token_table[j].type == 'STRING':
				some.append(token_table[j].value)
			elif token_table[j].type == 'COMMA':
				count += 1
			else:
				pass
			j += 1
		some.append(count)
		some.append(token_table[i].lineno)
		i += 1
		symbol_table.append(some)
	else:
		i += 1


if __name__ == '__main__':
	#pprint(symbol_table)
	#pprint(token_set)
	pprint(token_table)