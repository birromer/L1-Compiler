############################################# SUMMARY #############################################
# a sentence will be parsed and accepted or denied according to the Context-Free Grammar of L0
# if it is a term of L0, it will have its type inferred
# if it is well-typed, it will follow to the big step evaluation

import parserlark
import argparse

def is_numerical_value(tree):
	if tree == '0':
		return True
	elif tree[0] == 'succ' and is_numerical_value(tree[1]):
		return True
	else:
		return False

def is_value(tree):
	return True if tree == 'true' or tree == 'false' or is_numerical_value(tree) else False

# this function will receive a term of L0 and decide wheter it is well-typed
def type_infer(tree):
	
	if tree == '0':
		return 'Nat'																		# T-Zero

	elif tree == 'true':
		return 'Bool'																		# T-True

	elif tree == 'false':
		return 'Bool'																		# T-False

	elif tree[0] == 'succ':
		if type_infer(tree[1]) == 'Nat':
			return 'Nat'																	# T-Succ
		else:
			return False

	elif tree[0] == 'pred':
		if type_infer(tree[1]) == 'Nat':
			return 'Nat'																	# T-Pred
		else:
			return False

	elif tree[0] == 'iszero':
		if type_infer(tree[1]) == 'Nat':
			return 'Bool'																	# T-IsZero
		else:
			return False

	elif tree[0] == 'if':
		T = type_infer(tree[2])
		if type_infer(tree[1]) == 'Bool' and type_infer(tree[3]) == T:						# T-If
			return T
		else:
			return False

# here we assume the terms (trees) are well-typed, which will be guaranteed by type_infer
def small_step(tree):

	if is_value(tree):
		return False

	elif tree[0] == 'succ':
		return ('succ', small_step(tree[1]))												# E-Succ

	elif tree[0] == 'pred':
		if tree[1] == '0':
			return '0'																		# E-PredZero
		elif len(tree[1]) == 2 and tree[1][0] == 'succ' and is_numerical_value(tree[1][1]):
			return tree[1][1]																# E-PredSucc
		else:
			return ('pred', small_step(tree[1]))											# E-Pred

	elif tree[0] == 'iszero':
		if tree[1] == '0':
			return 'true'																	# E-IsZeroZero
		elif len(tree[1]) == 2 and tree[1][0] == 'succ' and is_numerical_value(tree[1][1]):
			return 'false'																	# E-IsZeroSucc
		else:
			return ('iszero', small_step(tree[1]))											# E-IsZero
	
	elif tree[0] == 'if':
		if tree[1] == 'true':
			return tree[2]																	# E-IfTrue
		elif tree[1] == 'false':
			return tree[3]																	# E-IfFalse
		else:
			return ('if', small_step(tree[1]), tree[2], tree[3])							# E-If


# in the L0 language it is proven that multiple small step and big step are compatible
def big_step(tree):
	while True:
		step = small_step(tree)
		if step == False:
			return tree
		else:
			tree = step

def tupletotext(tree):

	if type(tree) is tuple:
		sentence = tree[0]
		for i in range(1,len(tree)):
			sentence = sentence + ' ' + tupletotext(tree[i])
	elif type(tree) is str:
		sentence = tree

	return sentence

def interpret(sentence):
	
	tree = parserlark.parse(sentence)

	if tree == False:
		return False
	if type_infer(tree) == False:
		return False

	tree = big_step(tree)

	return tupletotext(tree)

if __name__ == '__main__':
	argparser = argparse.ArgumentParser()
	argparser.add_argument('-f', '--file', type=str, help='File to read sentence from', default=None)
	argparser.add_argument('-s', '--sentence', type=str, help='Sentence to read', default=None)
	args = argparser.parse_args()

	if args.file is not None:
		try:
			sentence = open(args.file,'r').read()
		except:
			exit()
	elif args.sentence is not None:
		try:
			sentence = args.sentence
		except:
			exit()
	else:
		try:
			sentence = input('Insert sentence to read: ')
		except:
			exit()

	print(interpret(sentence))
	exit()
