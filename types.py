#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 15:29:59 2019

@author: birromer
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def type_infer(tree: tuple, env: dict):
	
	if type( tree ) != tuple:
		tree = ( tree, )

	if len(tree) == 1:																	# leaf node
		if type( tree[0] ) == int:												# T-Int
			return 'int'
		elif tree[0] == True or tree[0] == False:					# T-Bool
			return 'bool'
		else:																							# T-Var
			if tree[0] in env.keys():
				return env[tree[0]]
			else:
				return False
		return False
	else:
		if tree[0] == '+' or tree[0] == '-' or tree[0] == '*':		# T-op (+, -, *)
			if type_infer( tree[1], env ) == 'int' and type_infer( tree[2], env ) == 'int':
				return 'int'
			else:
				return False
		elif tree[0] == '>=' or tree[0] == '>' or	tree[0] == '<' or tree[0] == '<=' or tree[0] == '==' or tree[0] == '!=':     # T-op (>=, >, <, <=)
			if type_infer( tree[1], env ) == 'int' and type_infer( tree[2], env ) == 'int':
				return 'bool'
			else:
				return False
		elif tree[0] == 'if':															# T-If
			if type_infer( ( tree[1] ), env ) == 'bool':
				a_type = type_infer( tree[2], env )
				b_type = type_infer( tree[3], env )
				if a_type == b_type:
					return a_type
				else:
					return False
			else:
				return False
		elif tree[0] == 'fn':															# T-Fun
			return ( tree[2], type_infer( tree[3], dict(env, **{ tree[1] : tree[2] } ) ) )
		elif tree[0] == 'let':														# T-Let
			t = tree[2]
			if type_infer( tree[3], dict( env, **{ tree[1] : tree[2] } ) ) == t:
				return type_infer( tree[4], dict( env, **{ tree[1] : tree[2] } ) )
			else:
				return False
		elif tree[0] == 'letrec':												# T-LetRec
			#[f : (T1->T2)]
			env[tree[1]] = (tree[2], tree[3])
			fn = tree[4]
			# x : T1
			env[fn[1]] = fn[2]       
			if(fn[2] == tree[2] and type_infer( fn[3], env ) == tree[3] ):
				return (type_infer ( tree[5], env ) )
			else:
				return False
		elif tree[0] == '@':														# T-App
			e1_type = type_infer( tree[1], env )
			if type( e1_type ) != tuple:
				 e1_type = ( e1_type, )
			e2_type = type_infer( tree[2], env )
			if len(e1_type) == 2:
				if e1_type[0] == e2_type:
					return e1_type[1]
				else:
					return False
			else:
				return False

	return False
  
  
  
if __name__ == "__main__":
  def test_result(result, expected):
    if result == expected:
      print("Test passed")
    else:
      print("Test failed")
  
  test0     = ( 0, )
  result    = type_infer( test0, {} )
  expected = 'int'
  test_result(result, expected)
  
  testTrue = ( True, )
  result   = type_infer( testTrue, {} )
  expected = 'bool'
  test_result(result, expected)
  
  
  testFalse = ( False, )
  result    = type_infer( testFalse, {} )
  expected  = 'bool'
  test_result(result, expected)
  
  testIf   = ( 'if', True, 0, 1 )
  result   = type_infer( testIf, {} ) 
  expected = 'int'
  test_result(result, expected)
  
  testIf2  = ( 'if', False, True, False )
  result   = type_infer( testIf2, {} )
  expected = 'bool' 
  test_result(result, expected)
  
  testVar  = ( 'x' )
  result   = type_infer( testVar, {} ) 
  expected = False
  test_result(result, expected)
  result   = type_infer( testVar, { 'x': 'int' } ) 
  expected = 'int'
  test_result(result, expected)
  
  testSum  = ( '+', testIf, 1 )
  result   = type_infer( testSum, {} ) 
  expected = 'int'
  test_result(result, expected)
  
  testFun  = ( 'fn', 'x', 'bool', ( 'if', 'x', 0, 1 )) 
  result   = type_infer( testFun, {} ) 
  expected = ('bool', 'int')
  test_result(result, expected)
  
  testApp  = ( '@', testFun, True )
  result   = type_infer( testApp, {} ) 
  expected = 'int'
  test_result(result, expected)
  
  testLet  = ('let', 'x', 'int', ('+', 3, ('+', 3, 4)), ('if', ('>', 'x', 0), True, False))
  result   = type_infer( testLet, {} ) 
  expected = 'bool'
  test_result(result, expected)
  
  testLetRec = ('letrec', 'foo', 'int', 'int', ('fn', 'x' , 'int',('if', ('>', 'x', 0), ('@', 'foo', ('-', 'x', 1) ), 0 ) ), ('@', 'foo', 3 ) )
  result     = type_infer( testLetRec, {} ) 
  expected   = 'int'
  test_result(result, expected)