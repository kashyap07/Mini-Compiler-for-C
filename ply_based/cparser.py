#!usr/bin/env python
# @Author: Suhas Kashyap
# @Date: 2017-03-20

# Compiler design mini-project
# Mini compielr for c written in python
# Emphasis on while loops

# cparser.py

import sys
import re
import time
import ply.yacc as yacc
from pprint import pprint

import clex
tokens = clex.tokens
symbol_table = clex.symbol_table


print('Lexical phase')
time.sleep(0.5)
print('symbol table generated')
pprint(clex.token_table)
print()
pprint(symbol_table)
print()

time.sleep(0.5)
print('Syntax phase')
time.sleep(0.5)
print('No Syntax error\n')

precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE')
)


# semantic phase
def p_SDASH(p):
	'''SDASH : D'''

	print('The grammar is valid')
	print('Semantic phase')
	time.sleep(1)
	flag = True


	for k in symbol_table:
		if k[0] == 'int' and isinstance(k[2], int):
			pass
		elif k[0] == 'float' and isinstance(k[2], float):
			pass
		elif k[0] == 'char' and isinstance(k[2], str):
			pass
		elif k[0] == 'PRINT' and k[1].count('%') == k[2]:
			pass
		else:
			flag = False
	if flag:
		print('The code is semantically correct')
	else:
		print('The code is semantically not correct')



def p_D(p):
	'''
	D   :	DIRECTIVE D 
		|	INT MAIN LPAREN RPAREN LFPAREN S RFPAREN
		|	FLOAT MAIN LPAREN RPAREN LFPAREN S RFPAREN    
	'''

def p_S(p):
	'''
	S   :	WHILE LPAREN B RPAREN LFPAREN S RFPAREN
		|	ASSIGNMENT
		|	FUNCTION
		|	RETURN NUMBER SEP
		|
	'''

def p_B(p):
	'''
	B   :	E RELOP E
		|	E
	'''

def p_E_op(p):
	'''
	E   :	E PLUS E
		|	E MINUS E
		|	E DIVIDE E
		|	E MULTIPLY E
		
	'''
	# to update the symbol table
	if p[2] == '+':
		p[0] = p[1] + p[3]
	if p[2] == '-':
		if not p[1].isdigit():
			for i in symbol_table:
				if p[1] == i[1]:
					p[1] = i[2];
		p[0] = p[1] - p[3]

	if p[2] == '*':
		if not p[1].isdigit():
			for i in symbol_table:
				if p[1] == i[1]:
					p[1] = i[2];
		p[0] = p[1] * p[3]
	if p[2] == '/':
		p[0] = p[1] / p[3]

	for i in symbol_table:
		if p[-2] == i[1]:
			i[2] = p[0]

	#print(p[0])



def p_E_id(p):
	'''
	E   :	ID
	'''
	p[0] = p[1]

def p_E_num(p):
	'''
	E   :	NUMBER
		|	FNUMBER
		|	CHARACTER
	'''    
	p[0] = p[1]

def p_ASSIGNMENT(p):
	'''
	ASSIGNMENT  :	INT ID EQUALS E SEP S
				|	ID EQUALS E SEP S
				|	FLOAT ID EQUALS E SEP S
				|	CHAR ID EQUALS E SEP S
				|	INT ID SEP S
				|	FLOAT ID SEP S
				|	CHAR ID SEP S

	'''

def p_FUNCTION(p):
	'''
	FUNCTION	:	PRINT LPAREN STRING S2 RPAREN SEP S
	'''

def p_S2(p):
	'''
	S2  :	COMMA ID S2
		|
	'''

def p_S1(p):
	'''
	S1  :	INT ID EQUALS E SEP LAST 
		|	ID EQUALS E SEP LAST 
		|	FLOAT ID EQUALS E SEP
		|	PRINT LPAREN STRING S2 RPAREN SEP LAST 
	'''

def p_LAST(p):
	'''
	LAST    :	RETURN NUMBER SEP 
			|	RETURN FNUMBER SEP
			|
	'''
	

def p_error(p):
	print('Syntax Error!')
	print('error in line num: ' + str(p.lineno - k+1))
	print('error at ' + p.type + ' ' + p.value)
	exit()


def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string)	# multi-line comments
    string = re.sub(re.compile("//.*" ) ,"" ,string)	# single line comments
    return string



yacc.yacc()

file = open(sys.argv[1]).read()
s = removeComments(file)
k = len(file.split('\n'))
yacc.parse(s)


print('\nupdated symbol table')
pprint(symbol_table)