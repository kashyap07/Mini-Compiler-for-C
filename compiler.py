#!usr/bin/env python
# @Author: Suhas Kashyap
# @Date: 2017-03-06

# C compiler using python
# Compiler Design mini-project
# emphasis on while loops


# TODO:
# 	1. remove comments
# 	2. handle string literals having comments in them

import re
import sys

TOKEN_TYPES = ['KEY_WORD', 'IDENTIFIER', 'DIGIT_CONSTANT', 'OPERATOR', 'SEPARATOR', 'STRING_LITERAL']

DETAIL_TOKEN_TYPES = {
	'include': 'INCLUDE', 'int': 'INT', 'float': 'FLOAT', 'char': 'CHAR', 'double': 'DOUBLE', 'for': 'FOR', 'if': 'IF', 'else': 'ELSE',
    'while': 'WHILE', 'do': 'DO', 'return': 'RETURN', '=': 'ASSIGN', '&': 'ADDRESS',
    '<': 'LT', '>': 'GT', '++': 'SELF_PLUS', '--': 'SELF_MINUS', '+': 'PLUS', '-': 'MINUS', '*': 'MUL', '/': 'DIV', '>=': 'GET', '<=': 'LET', '(': 'LCURV_BRACKET',
    ')': 'RCURV_BRACKET', '{': 'LFLR_BRACKET', '}': 'RFLR_BRACKET', '[': 'LSQR_BRACKET', ']': 'RSQR_BRACKET', ',': 'COMMA', '\"': 'DOUBLE_QUOTE',
    ';': 'SEMICOLON', '#': 'POUND'
}

keywords = [['int', 'float', 'double', 'char', 'void'], ['if', 'for', 'while', 'do', 'else'], ['include', 'return']]

operators = ['=', '&', '<', '>', '++', '--', '+', '-', '*', '/', '>=', '<=', '!=']

delimiters = ['(', ')', '{', '}', '[', ']', ',', '\"', ';']

content = 0


class Token(object):
	# wrapper class
	def __init__(self, type_index, value):
		self.type = DETAIL_TOKEN_TYPES[value] if type_index == 0 or type_index == 3 or type_index == 4 else TOKEN_TYPES[type_index]
		self.value = value

class Lexer(object):
	# Lexical analyzer
	def __init__(self):
		# list to store tokens
		self.tokens = []

	def is_ws(self, index):
		# check if white space
		return content[index] == ' ' or content[index] == '\t' or content[index] == '\n' or content[index] == '\r'

	def skip_ws(self, index):
		# skip the character if whitespace
		# just increment pointer
		while index < len(content) and self.is_ws(index):
			index += 1
		return index

	def print_log(self, style, value):
		# styling and padding
		print('{:>10}'.format('< ' + style) + ' , ' + '{:<10}'.format(value + ' >'))

	def is_keyword(self, value):
		for item in keywords:
			if value in item:
				return True
		return False


	def main(self):
		i = 0
		while i < len(content):
			i = self.skip_ws(i)
			# assuming proper C program
			if content[i] == '#':
				self.tokens.append(Token(4, content[i]))
				i = self.skip_ws(i + 1)
				# analyzing header files
				while i < len(content):
					# match 'include'
					if re.match('include', content[i:]):
						self.tokens.append(Token(0, 'include'))
						# move pointer to character after 7 (include)
						i = self.skip_ws(i + 7)
					# match 'header file: 'file.h' or <file.h>'
					elif content[i] == '\"' or content[i] == '<':
						self.tokens.append(Token(4, content[i]))
						i = self.skip_ws(i + 1)
						if content[i] == '\"':
							close_flag = '\"'
						else:
							close_flag = '>'
						# find the included header file
						lib = ''
						while content[i] != close_flag:
							lib += content[i]
							i += 1
						self.tokens.append(Token(1, lib))
						self.tokens.append(Token(4, close_flag))
						i = self.skip_ws(i + 1)
						break
					else:
						print('include error!')
						exit()
			# check if alphabetical only or starts with _
			elif content[i].isalpha() or content[i] == '_':
				temp = ''
				# check for identifier
				while i < len(content) and (content[i].isalpha() or content[i] == '_' or content[i].isdigit()):
					temp += content[i]
					i += 1
				if self.is_keyword(temp):
					self.tokens.append(Token(0, temp))
				else:
					self.tokens.append(Token(1, temp))
				i = self.skip_ws(i)
			# check if first character is a number
			elif content[i].isdigit():
				temp = ''
				while i < len(content):
					if content[i].isdigit() or (content[i] == '.' and content[i + 1].isdigit()):
						temp += content[i]
						i += 1
					elif not content[i].isdigit():
						if content[i] == '.':
							print('float number error!')
							exit()
						else:
							break
				self.tokens.append(Token(2, temp))
				i = self.skip_ws(i)
			# check if character is a delimter
			elif content[i] in delimiters:
				self.tokens.append(Token(4, content[i]))
				# if string literal, starts with: "
				if content[i] == '\"':
					i += 1
					temp = ''
					while i < len(content):
						if content[i] != '\"':
							temp += content[i]
							i += 1
						else:
							break
					else:
						print('error: can\'t find \"')
						exit()
					self.tokens.append(Token(5, temp))
					self.tokens.append(Token(4, '\"'))
				i = self.skip_ws(i + 1)
			# check id character is an operator
			elif content[i] in operators:
				# for ++ and --
				if (content[i] == '+' or content[i + 1] == content[i]):
					self.tokens.append(Token(3, content[i] * 2))
					i = self.skip_ws(i + 2)
				# for <= and >=
				elif (content[i] == '>' or content[i] == '<') and content[i + 1] == '=':
					self.tokens.append(Token(3, content[i] + '='))
					i = self.skip_ws(i + 2)
				else:
					self.tokens.append(Token(3, content[i]))
					i = self.skip_ws(i + 1)


def lexer():
	lexer = Lexer()
	lexer.main()
	for token in lexer.tokens:
		print('{:>15}'.format(token.type) + ', ' + '{:<10}'.format(token.value))

if __name__ == '__main__':
	file = open('test_input.c', 'r')
	content = file.read()
	lexer()