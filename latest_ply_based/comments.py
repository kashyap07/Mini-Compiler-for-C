import re

def removeComments(program):
	multiLineComment = '/\*.*?\*/'
	singleLineComment = '//.*?\\n'
	string = '\".*?\"|\'.*?\''
	# 2 groups
	# group1 - string, group2 - comments
	pattern = '(%s)|(%s|%s)' % (string,singleLineComment,multiLineComment)	
	regex = re.compile(pattern,re.MULTILINE|re.DOTALL)
	
	# callback function for every match
	# if group 2 of match is not None(is a comment), replace it with ''
	# if group 2 of match is None(is a string), ignore it
	def _removeComments(match):
		if match.group(2) is not None:
			return ''
		else:
			return match.group(1)

	program = regex.sub(_removeComments,program)
	return program

# read from a file and pass the program to removeComments
if __name__ == '__main__':
	pgm = '''
	int main()
	{
		int a;
		//int a;
		/*bbb*/;
		/*aaa
		bbb
		/* abcdefgh */
		// abcd
		*/

		int b = "a /*bcd*/ //bb ";
		/*
		abcd
		adad
		*/
		int x = 10;
		char c = 'a';
		char d = "a//"/*a//*/aa;
	}
	'''
	res = removeComments(pgm)
	print(res)
