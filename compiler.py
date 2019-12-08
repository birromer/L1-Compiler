#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def compileSSM1(tree):

  if type(tree) is not tuple:
    tree = (tree,)

  t0 = tree[0]
  if len(tree) >= 2: t1 = tree[1]
  if len(tree) >= 3: t2 = tree[2]
  if len(tree) >= 4: t3 = tree[3]
  if len(tree) >= 5: t4 = tree[4]
  if len(tree) >= 6: t5 = tree[5]

  if len(tree) == 1:
    if type(t0) is int:           # n
      return [('INT', t0)]
    elif type(t0) is bool:        # b
      return [('BOOL', t0)]
    elif type(t0) is str:         # x
      return [('VAR', t0)]
  else:
    if t0 == '+':                 # op +
      e1 = t1
      e2 = t2
      return compileSSM1(e2) + compileSSM1(e1) + [('ADD',)]
    elif t0 == '-':               # op -
      e1 = t1
      e2 = t2
      return compileSSM1(e2) + [('INV',)] + compileSSM1(e1) + [('ADD',)]  


    elif t0 == '>':               # op >
      e1 = t1
      e2 = t2
      return compileSSM1(e2) + compileSSM1(e1) + [('GT',)]

    elif t0 == '>=':               # op >=
      e1 = t1
      e2 = t2
      Ce1 = compileSSM1(t1)
      Ce2 = compileSSM1(t2)
      n1 = len(Ce2 + Ce1 + [('EQ',)] + [('JMPIFTRUE', 2)] + [('BOOL', False)] + [('JUMP', 1)])
      return Ce2 + Ce1 + [('GT',)] + [('JMPIFTRUE', n1)] + Ce2 + Ce1 + [('EQ',)] + [('JMPIFTRUE', 2)] + [('BOOL', False)] + [('JUMP', 1)] + [('BOOL', True)]


    elif t0 == 'if':              # if
      e1 = t1
      Ce2 = compileSSM1(t2)
      Ce3 = compileSSM1(t3)
      n2 = len(Ce2)
      n3 = len(Ce3)
      return compileSSM1(e1) + [('JMPIFTRUE', n3+1)] + Ce3 + [('JUMP', n2)] + Ce2

    elif t0 == '@':               # apply
      e1 = t1
      e2 = t2
      return compileSSM1(e2) + compileSSM1(e1) + [('APPLY',)]

    elif t0 == 'fn':              # function
      x = t1
      e = t3
      return [('FUN', x, compileSSM1(e))]

    elif t0 == 'let':             # let
      x = t1
      e1 = t3
      e2 = t4
      return compileSSM1(e1) + [('FUN', x, compileSSM1(e2))] + [('APPLY',)]

    elif t0 == 'letrec':
      fid = t1
      fT1 = t2
      fT2 = t3
      fn = t4
      x = fn[1]
      e1 = fn[2]
      e2 = t5
      return [('RFUN', fid, x, compileSSM1(e1))] + [('FUN', fid, compileSSM1(e2))] + [('APPLY',)]

if __name__ == "__main__":
  test1 = ('let', 'x', 'int', ('+', 3, ('+', 3, 4)), ('if', ('>=', 'x', 0), True, False))
  print( compileSSM1(test1) )
  
  # testLetRec = ('letrec', 'foo', 'int', 'int', ('fn', 'x', 'int',('if', True, ('@', 'foo', ('-', 'x', 1) ), 0 ) ), ('@', 'foo', 3 ) )
  # print( compileSSM1(testLetRec) 
