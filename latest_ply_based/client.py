import comments

import syntax_phase
import sys
import os

from pprint import pprint

# global variables
tokens = []
symbolTable = {}
count=0
def lexicalPhase(program):
	global symbolTable
	global tokens
	program = comments.removeComments(program)
	#tokens = lexer.generateTokens(program)
	#return tokens


def syntaxPhase(program):
	program = comments.removeComments(program)
	result = syntax_phase.parse(program)
	return result

def printcheck(token):
	if token[0]=='PRINT':
			#print(token[1])
			t=token[1]
			t=t.replace('printf','');
			t=t.replace('(','')
			t=t.replace(')','')
			t=t.replace('"','')
			#print(t)
			t=t.split(',')
			#print(t)
			ty = t[0].strip().split("%")
			#print(ty)
			for i in range(1,len(ty)):
				#print(ty[i])
				if ty[i].strip()=='d':
					c.append(['int',''])
				else:
					c.append(['float',''])
				#print(c)
			for i in range(1,len(t)):
				c[i-1][1]=t[i]
			#print(c)
			for x in c:
				#print(x)
				if x[1] in symbolTable.keys():
					d = symbolTable[x[1]]
					#print(x[0])
					#print(d)
					#print(d[2])
					#print(type
					#print(type(d[2][0]).__name__,x[0])
					if (type(d[2][0])).__name__ != x[0]:

						print("Error in printf type mismatch id:",x[1]," expected:",type(d[2][0]).__name__," received:",x[0],"in line:",token[2])	
	
# returns list of errors - id, type, expected type, line number
def typeCheck(stack,symbol_table):
	print(stack)
	for x in stack :
		if x[0] in symbol_table.keys():
			value = symbol_table[x[0]]
			if value[1]=='int' and ('.' in x[1]):
				print("Error: ID",x[0]," |lineno : ",x[2],"| expected value type : int | found : float")

if __name__=='__main__':
	#program = open(input('Enter filename:')).read()
	program = open(sys.argv[1]).read()

	#print(program)

	# lexical phase
	#print('Lexical Phase:\n')
	#tokens = lexicalPhase(program)
	#print()
	#c=[]
	#print('Tokens:')
	#for token in tokens:
	#	print(token)
				

	os.system('clear')

	# syntax phase
	#print('\nSyntax Phase:\n')
	result = syntaxPhase(program)
	print('Program is: ', result[0])
	#print('-'*50)
	
	#print('-'*50)
	#print('Symbol Table:')
	#for x in syntax_phase.symbol_table:
	#	print(x,'   ',syntax_phase.symbol_table[x])
	#pprint(result[1])
	#print('-'*50)

	# semantic phase
	#print('\nSemantic Phase:\n')
	#typeCheck(result[2],result[1])
	
	#print('-' * 50)

	if result[0] == 'Invalid':
		pass
	else:
		# Intermmediate code
		print('\nIntermmediate code:\n')
		print('OP\tARG1\tARG2\tRESULT')
		for quadruple in syntax_phase.quadruples:
			print('%s\t%s\t%s\t%s' % (quadruple[0],quadruple[1],quadruple[2],quadruple[3]))
