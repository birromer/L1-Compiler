from lark import Lark
from lark import exceptions
from lark import Transformer

# l0_parser = Lark(r"""
# 	?term	: term2 | _S* "(" _S* term2 _S* ")" _S*
	
# 	?term2	: _S* "0" _S*										-> zero
# 			| _S* "true" _S*									-> true
# 			| _S* "false" _S*									-> false
# 			| _S* "succ" term									-> succ
# 			| _S* "pred" term									-> pred
# 			| _S* "iszero" _S* term								-> iszero
# 			| _S* "if" _S* term "then" _S* term "else" _S* term	-> if_t_e

# 	_S		: " "
# 			| "\n"
# 			| "\t"

# 	""", start='term')



# | "let rec f:" funtype "= (" function ") in " term 	-> letrec
# ?value	: n | b | function

l1_parser = Lark(r"""
	?term 	: _S* term2 | _S* "(" _S* term2 _S* ")" _S*

	?term2	: n
			| b
			| id 
			| "fn" id ":" type "=>" term 				-> fun
			| term op term 								-> op
			| "if" term "then" term "else" term 		-> if_t_e
			| "apply" term "to" term					-> apply
			| "let" id ":" type "=" term "in" term 		-> let

	?n		: SIGNED_NUMBER _S* -> number

	?b		: "true" _S* 	-> true
			| "false" _S*	-> false
	
	?id		: _S* STRING -> id
	
	?op		: "+" 	-> plus
			| "-" 	-> minus
			| "*" 	-> times
			| ">" 	-> greater
			| ">=" 	-> g_or_eq
			| "==" 	-> equal
			| "!=" 	-> notequal
			| "<=" 	-> l_or_eq
			| "<"	-> less

	?type	: _S* "int"	_S*		-> inttype
			| _S* "bool" _S*	-> booltype
			| funtype

	?funtype : type "->" type	-> funtype

	_S		: " "
			| "\n"
			| "\t"

	STRING	: /([^\s:*]+)/

	%import common.SIGNED_NUMBER

	""", start='term')

class Transf(Transformer):
	term     = tuple
	
	true     = lambda self, _: 'true'
	false    = lambda self, _: 'false'

	plus     = lambda self, _: '+'
	minus    = lambda self, _: '-'
	times    = lambda self, _: '*'
	greater  = lambda self, _: '>'
	g_or_eq  = lambda self, _: '>='
	equal    = lambda self, _: '=='
	notequal = lambda self, _: '!='
	l_or_eq  = lambda self, _: '<='
	less     = lambda self, _: '<'
	
	inttype  = lambda self, _: 'int'
	booltype = lambda self, _: 'bool'
	
	def funtype(self, items):
		return (items[0], items[1])

	def id(self, s):
		(s,) = s
		return str(s)

	def number(self, n):
		(n,) = n
		return int(n)
		
	def op(self, items):
		return (items[0], items[1], items[2])

	def if_t_e(self, items):
		return ('if', items[0], items[1], items[2])

	def apply(self, items):
		return ('apply', items[0], items[1])

	def let(self, items):
		return ('let', items[0], items[1], items[2], items[3])

	def fun(self, items):
		return ('fun', items[0], items[1], items[2])

def parse(sentence):
	# try:
	tree = l1_parser.parse(sentence)
	tree = Transf().transform(tree)
	print(tree)
	# except:
	# 	print('Parsing went wrong')
	# 	return False
	return tree

parse('2 + 3 * 4 - 5 > 0')
parse('if true then 2 + 3 + 4 else 3 - 5')
parse('apply (fn x:int => true) to 3')
parse('let x:int = 3 in x')
# parse('(fn x:int => (if x > 0 then true else false))')
# parse('apply true to true')
# parse('aloalo')