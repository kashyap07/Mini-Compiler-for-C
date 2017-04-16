import ply.yacc as yacc
from lexer import tokens,symbol_table
start = 'start_state'
stack = []
label_stack = []
for_stack = []
temp=0
label_count = 1
quadruples=[]
#print(symbol_table)
def p_start_state(p):
	'start_state : include INT ID OPBRAC CLOSEBRAC OPENFLR iter_stmt CLOSEFLR'
	global result
	result = 'Valid'	
def p_include(p):
	'''include : DER
			|'''
def p_iter_stmt(p):
	'iter_stmt : WHILE OPBRAC for_cond_stmt CLOSEBRAC after_for_stmts'
	#global label_count
	#quadruples.append(['label','0','','L'+str(label_count)])
	#label_stack.append('L'+str(label_count))
	#temp+=1
	#label_count+=1

def p_after_for_stmts(p):
	'''after_for_stmts : OPENFLR stmts CLOSEFLR
			| iter_stmt
			| expr_stmt STATETER stmts
			| printing STATETER stmts
			| assignment STATETER stmts
			| decfloat STATETER stmts
			| declareint STATETER stmts 
			| math STATETER
			| '''
	global label_stack
	global label_count
	global temp

	x2 = label_stack.pop()
	x1 = label_stack.pop()
	quadruples.append(['goto','','',x1])
	
	quadruples.append(['label','','',x2])

def p_stmts(p):
	'''stmts : OPENFLR stmts CLOSEFLR
			| iter_stmt
			| expr_stmt STATETER stmts
			| printing STATETER stmts
			| assignment STATETER stmts
			| decfloat STATETER stmts
			| declareint STATETER stmts
			| math STATETER
			| '''
			
def p_expr_stmt(p):
	'''expr_stmt : assignment_int
			| declare'''
def p_assignment_int(p):
	'''assignment_int : INT ID ASSIGN NUMBER followint
	'''
	global temp
	lineno = p.lineno(1)
	stack.append([p[2],p[4],lineno])

	symbol_table[p[2]]=['ID','int',p[4], lineno]

	quadruples.append(['=',p[4],'',p[2]])
	temp+=1
def p_assignment_int1(p):
	'''assignment_int : INT ID followint
	'''
	global temp
	lineno = p.lineno(2)
	stack.append([p[2],'0',lineno])
	symbol_table[p[2]]=['ID','int','0', lineno]
	quadruples.append(['=','0','',p[2]])
	temp+=1
def p_follow_int(p):
	'''followint : COMMA ID ASSIGN NUMBER followint'''
	global temp
	lineno = p.lineno(2)
	stack.append([p[2],p[4],lineno])
	symbol_table[p[2]]=['ID','int',p[4], lineno]

	quadruples.append(['=',p[4],'',p[2]])
	temp+=1
def p_follow_int1(p):
	'''followint : COMMA ID followint'''
	global temp
	lineno = p.lineno(2)
	stack.append([p[2],'0',lineno])
	symbol_table[p[2]]=['ID','int','0', lineno]

	quadruples.append(['=','0','',p[2]])
	temp+=1
def p_follow_int2(p):
	'''followint : '''

def p_assignment_float(p):
	'''assignment : FLOAT ID ASSIGN NUMBER followfloat
	'''
	global temp
	lineno = p.lineno(1)
	stack.append([p[2],p[4],lineno])

	symbol_table[p[2]]=['ID','float',p[4], lineno]

	quadruples.append(['=',p[4],'',p[2]])
	temp+=1
def p_assignment_float1(p):
	'''assignment : FLOAT ID followfloat
	'''
	global temp
	lineno = p.lineno(2)
	stack.append([p[2],'0.0',lineno])
	symbol_table[p[2]]=['ID','float','0.0', lineno]

	quadruples.append(['=','0.0','',p[2]])
	temp+=1
def p_follow_float(p):
	'''followfloat : COMMA ID ASSIGN NUMBER followfloat'''
	global temp
	lineno = p.lineno(2)
	stack.append([p[2],p[4],lineno])
	symbol_table[p[2]]=['ID','float',p[4], lineno]

	quadruples.append(['=',p[4],'',p[2]])
	temp+=1
def p_follow_float1(p):
	'''followfloat : COMMA ID followfloat'''
	global temp
	lineno = p.lineno(2)
	stack.append([p[2],'0',lineno])
	symbol_table[p[2]]=['ID','float','0.0', lineno]

	quadruples.append(['=','0.0','',p[2]])
	temp+=1
def p_follow_float2(p):
	'''followfloat : '''

def p_assignment_char(p):
	'''assignment : CHAR ID ASSIGN NUMBER follow
	'''
	global temp
	lineno = symbol_table[p[2]]
	symbol_table[p[2]]=['ID','char',p[4], lineno[0]]

	quadruples.append(['=',p[4],'',p[2]])
	temp+=1
def p_declare(p):
	'''declare : ID ASSIGN NUMBER followint'''
	global temp
	lineno = p.lineno(1)
	stack.append([p[1],p[3],lineno])

	quadruples.append(['=',p[3],'',p[1]])
	temp+=1
def p_declareint(p):
	'''declareint : ID ASSIGN NUMBER '''
	global temp
	print("-------------",p[1])
	lineno = symbol_table[p[1]]
	stack.append([p[1],p[3],lineno])

	quadruples.append(['=',p[3],'',p[1]])
	temp+=1
def p_declarefloat(p):
	'''decfloat : ID ASSIGN NUMBER '''
	print("-------------",p[1])
	global temp
	lineno = p.lineno(1)
	stack.append([p[1],p[3],lineno])

	quadruples.append(['=',p[3],'',p[1]])
	temp+=1

def p_for_cond_stmt(p):
	'''for_cond_stmt : ID RELOP ID
			| ID RELOP NUMBER
			| NUMBER RELOP ID
			| NUMBER RELOP NUMBER
			| cond_stmt LOGOP cond_stmt'''
	global temp
	global label_stack
	global label_count
	quadruples.append(['label','','','L'+str(label_count)])
	label_stack.append('L'+str(label_count))
	quadruples.append([p[2],p[1],p[3],'t'+str(temp)])
	p[0]='t'+str(temp)
	label_count+=1

	quadruples.append(['jmpFalse','L'+str(label_count),'t'+str(temp),''])
	label_stack.append('L'+str(label_count))

	temp+=1
	label_count+=1


def p_cond_stmt(p):
	'''cond_stmt : ID RELOP ID
			| ID RELOP NUMBER
			| NUMBER RELOP ID
			| NUMBER RELOP NUMBER
			| cond_stmt LOGOP cond_stmt'''
	global temp
	quadruples.append([p[2],p[1],p[3],'t'+str(temp)])
	p[0]='t'+str(temp)
	temp+=1

def p_cond_stmt_absent(p):
	'''cond_stmt : '''
	pass

##################################################
##################################################
#Needs appropriate rule for prefix and postfix: currently ignored
##################################################
##################################################
def p_math(p):
	'''math : pfix ID
			| ID pfix
			| ID PLUS ASSIGN NUMBER
			| ID PLUS ASSIGN ID
			| ID MINUS ASSIGN NUMBER
			| ID MINUS ASSIGN ID
			| ID AOP ASSIGN NUMBER
			| ID AOP ASSIGN ID'''
	global temp
	#quadruples.append([p[2]+p[3],p[1],p[4],'t'+str(temp)])
	#quadruples.append(['=','t'+str(temp),'',p[1]])
	#temp+=1
	for_stack.append(['=','t'+str(temp),'',p[1]])
	for_stack.append([p[2]+p[3],p[1],p[4],'t'+str(temp)])

def p_math_absent(p):
	'''math : '''
	pass
def p_pfix(p):
	'''pfix : PLUS PLUS
			| MINUS MINUS'''
			
def p_printing(p):
	'''printing : PRINT 
			 '''
	c = []
	t = p[1]

	format_specs=p[1].split('"')[1]
	argument_list=p[1].split('"')[2][1:-1]

	t=t.replace('printf','')
	t=t.replace('(','')
	t=t.replace(')','')
	t=t.replace('"','')
	t=t.split(',')
	ty = t[0].strip().split("%")
	for i in range(1,len(ty)):
		if ty[i].strip()=='d':
			c.append(['int',''])
		else:
			c.append(['float',''])
	for i in range(1,len(t)):
		c[i-1][1]=t[i]
	for x in c:
		if x[1] in symbol_table.keys():
			d = symbol_table[x[1]]
			
			if d[1].strip() != x[0].strip():
				print("Error in printf type mismatch id:",x[1]," expected:",d[1]," received:",x[0],"in line:",p.lineno(1))
	#print("-------------------------------",c,t,"----------------------")	
	#quadruples.append(['printf',format_specs,argument_list,'stdout'])
	quadruples.append(['param','','',format_specs])
	quadruples.append(['param','','',argument_list])
	quadruples.append(['call','printf','2',''])


def p_printing1(p):
	'''printing : PRINTF OPBRAC STRLIT follow CLOSEBRAC
	'''
	
def p_follow (p):
	''' follow : COMMA ID follow
			|'''

def p_error(p):
	print("Syntax error in input: %s line number:%s" % (p,str(p.lineno)))
	#sys.exit()

result = 'Invalid'
parser = yacc.yacc()
#program = open('trial.c', 'r').read()
def parse(program):
	global parser
	global result
	res = parser.parse(program,tracking=True)
	return (result,symbol_table,stack)
#parse(program)
#for key in symbol_table.keys():
#	print(key, ':',  symbol_table[key])
#print("------SEMANTIC PHASE ----------------------------------------")
for x in stack :
	if x[0] in symbol_table.keys():
		value = symbol_table[x[0]]
		if value[1]=='int' and ('.' in x[1]):
			print("Error: ID",x[0]," |lineno : ",x[2],"| expected value type : int | found : float")


#while True:
#   try:
#       s = input('calc > ')
#   except EOFError:
#       break
#   if not s: continue
#   result = parser.parse(s)
 #  print(result)
#print(tokens)
