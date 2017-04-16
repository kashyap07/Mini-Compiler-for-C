import ply.lex as lex
reserved = {'if' : 'KEYWORD',
   'then' : 'KEYWORD',
   'else' : 'KEYWORD',
   'while' : 'WHILE',
   'for': 'FOR',
   'struct':'KEYWORD',

   }
tokens=['PRINT','PRINTF','FLOAT','CHAR','INT','PLUS','MINUS','NUMBER','AOP','RELOP','ID','ASSIGN','LOGOP','OPBRAC','CLOSEBRAC','PFIX','DER','STRLIT','STATETER','COMMA','OPENFLR','CLOSEFLR']+list(set(reserved.values()))
symbol_table={}
for keyword in reserved.keys():
	symbol_table[keyword]=["keyword",keyword,None,None]
symbol_table['int']=['keyword','int',None,None]
symbol_table['float']=['keyword','float',None,None]
symbol_table['char']=['keyword','char',None,None]
symbol_table['printf']=['keyword','printf',None,None]
t_ignore  = ' \t'

t_LOGOP = r'\|\| | && |!= '
t_ASSIGN = r'\='
t_RELOP = r'<= | >= | == |<|>'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_AOP = r' \* | \/ | %'
t_OPBRAC = r'\(  '
t_OPENFLR=r'{'
t_CLOSEFLR=r'}'
t_CLOSEBRAC = r'\) '
t_STATETER = r';'
t_COMMA = r','
def t_PRINT(t):
	r'printf \( \"[,%a-zA-Z0-9 ]*\"  (, [0-9A-za-z])*\)'
	return t
def t_PRINTF(t):
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
def t_DER(t):
	r'\#include<[a-z]+\.h>'
	return t
def t_STRLIT(t):
	r'\"[,%a-zA-Z0-9\*/\\ ]*\"'
	return t	
def t_NUMBER(t):
	r'\d+(.\d+)?'

	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'ID')
	if t.value not in symbol_table.keys():
		symbol_table[t.value]=[t.lineno]
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

#program = open('hello.c', 'r').read()
lexer = lex.lex()

def generateTokens(program):
	#print(program)
	global lexer
	lexer.input(program)
	token=[]
	while True:
		
		tok = lexer.token()
		if not tok:break
		#print(type(tok))
		#token.append((tok.type,tok.value,tok.lineno))
		#print(type(tok.value))
		print(tok)
#generateTokens(program)
#print(symbol_table)	
