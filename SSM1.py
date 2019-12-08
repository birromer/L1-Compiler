class SSM1:
  def __init__(self):
    self.code  = []
    self.stack = [] 
    self.env   = {}
    self.dump  = []
    
  def step(self, verbose=False):
    
    if self.code == [] and self.dump != []:
      to_restore = self.dump.pop(0) 
      new_code  = to_restore[0]
      new_stack = to_restore[1]
      new_env   = to_restore[2] 
      sv = self.stack.pop(0)
      
      self.code  = new_code
      self.stack = new_stack
      self.env   = new_env
      self.stack.insert(0, sv) 
    
    else:
      instruction = self.code.pop(0)
      
      if instruction[0] == "INT":
        self.stack.insert(0, instruction)

      elif instruction[0] == "BOOL":
        self.stack.insert(0, instruction)
  
      elif instruction[0] == "POP":
        self.stack.pop(0)
        
      elif instruction[0] == "COPY":
        sv = self.stack.pop(0)
        self.stack.insert(0, sv)
        self.stack.insert(0, sv)
      
      elif instruction[0] == "ADD":
        value1 = self.stack.pop(0)
        value2 = self.stack.pop(0)
        self.stack.insert(0, ("INT", value1[1]+value2[1]))
  
      elif instruction[0] == "INV":
        value = self.stack.pop(0)
        
        self.stack.insert(0, ("INT", -value[1]))
  
      elif instruction[0] == "EQ":
        value1 = self.stack.pop(0)
        value2 = self.stack.pop(0)
        self.stack.insert(0, ("BOOL", value1[1] == value2[1]))
  
      elif instruction[0] == "GT":
        value1 = self.stack.pop(0)
        value2 = self.stack.pop(0)
        self.stack.insert(0, ("BOOL", value1[1] > value2[1]))
  
      elif instruction[0] == "AND":
        value1 = self.stack.pop(0)
        value2 = self.stack.pop(0)
        self.stack.insert(0, ("BOOL", value1[1] and value2[1]))
  
      elif instruction[0] == "NOT":
        value = self.stack.pop(0)
        self.stack.insert(0, ("BOOL", not value[1]))
  
      elif instruction[0] == "JUMP":
        i = 1
        n = instruction[1]
        while i <= n:
          self.code.pop(0)
          i += 1
  
      elif instruction[0] == "JMPIFTRUE":
        value = self.stack.pop(0)
        if value[1] == True:
          i = 1
          n = instruction[1]
          while i <= n:
            self.code.pop(0)
            i += 1
  
      elif instruction[0] == "VAR":
        op = instruction[1]
        value = self.env[op]
        self.stack.insert(0, value)
  
      elif instruction[0] == "FUN":
        closure = ("CLOS", self.env, instruction[1], instruction[2])
        self.stack.insert(0, closure)
  
      elif instruction[0] == "RFUN":
        rclosure = ("RCLOS", self.env, instruction[1], instruction[2], instruction[3])
        self.stack.insert(0, rclosure)
  
      elif instruction[0] == "APPLY":
        clos = self.stack.pop(0)
        sv   = self.stack.pop(0)
  
        top_dump = (self.code, self.stack, self.env)
        self.dump.insert(0, top_dump)
    
        if clos[0] == "CLOS":
          new_env  = clos[1]
          new_var  = clos[2]
          new_code = clos[3]
  
          self.code  = new_code
          self.stack = []
          self.env   = new_env                
          self.env[new_var] = sv
          
        elif clos[0] == "RCLOS":
          new_env  = clos[1].copy()
          new_func = clos[2]
          new_var  = clos[3]
          new_code = clos[4]
          
          self.code = new_code
          self.stack = []
          self.env = new_env
          self.env[new_var] = sv
          self.env[new_func] = clos
          
        else:
          print("Something went really wrong :(")

      
  def run(self, code, verbose=False):
    self.code = code
    while not (self.code == [] and self.dump== []):
      self.step()
      if verbose:
        print("\nCurrent code:", self.code)
        print("Current stack:", self.stack)
        print("Current environment:", self.env)
        print("Current dump:", self.dump)

    return self.stack.pop(0)
  
  
if __name__ == "__main__":
  ssm1 = SSM1()

  class State:
    def __init__(self, code, stack, env, dump):
      self.code = code
      self.stack = stack
      self.env = env
      self.dump = dump
  
  def test_result(test_case, expected, verbose=False):
    if test_case.code:
      inst = test_case.code[0][0]
    else:
      inst = 'DUMP'
  
    ssm1.code  = test_case.code
    ssm1.stack = test_case.stack
    ssm1.env   = test_case.env
    ssm1.dump  = test_case.dump
  
    ssm1.step() 
    
    code_check  = ssm1.code  == expected.code
    stack_check = ssm1.stack == expected.stack
    env_check   = ssm1.env   == expected.env
    dump_check  = ssm1.dump  == expected.dump
  
    if verbose:
      print("\nSSM1")
      print(ssm1.code)
      print(ssm1.stack)
      print(ssm1.env)
      print(ssm1.dump)
      print("\nExpected")
      print(expected.code)
      print(expected.stack)
      print(expected.env)
      print(expected.dump,"\n")
      if ssm1.code != expected.code:
        print("Error in code")
      if ssm1.stack != expected.stack:
        print("Error in stack")
      if ssm1.env != expected.env:
        print("Error in Environment")
      if ssm1.dump != expected.dump:
        print("Error in dump")
  
    if code_check and stack_check and env_check and dump_check:
      print("Test {} passed".format(inst))
    else:
      print("Test {} failed".format(inst))
    
  
  # INT
  test0 = State( [("INT", 0)], [], {}, [] )
  test_result(test0, State( [], [("INT", 0)], {}, [] ) )
  
  # BOOL
  testTrue = State( [("BOOL", True)], [], {}, [] )
  test_result(testTrue, State( [], [("BOOL", True)], {}, []) ) 
  
  # POP
  testPop = State( [("POP", )], [("INT", 1)],  {}, [] )
  test_result(testPop, State( [], [], {}, []) ) 
  
  # COPY
  testCopy = State( [("COPY", )], [("INT", 1)],  {}, [] )  
  test_result(testCopy, State([], [("INT", 1), ("INT", 1)], {}, []) ) 
  
  # ADD
  testSum = State( [("ADD", )], [("INT", 1), ("INT", 10)], {}, [])
  test_result(testSum , State( [], [("INT", 11)], {}, [] ) )
  
  # INV
  testInv = State( [("INV",)], [("INT", 1)], {}, [] )
  test_result(testInv, State ([], [("INT", -1)], {}, []))
  
  # EQ1
  testEq1 = State( [("EQ",)], [("BOOL", True), ("BOOL", True)], {}, [] )
  test_result(testEq1, State ([], [("BOOL", True)], {}, []))
  
  # EQ2
  testEq2 = State( [("EQ",)], [("BOOL", False), ("BOOL", True)], {}, [] )
  test_result(testEq2, State ([], [("BOOL", False)], {}, []))
  
  # GT1
  testGt1 = State( [("GT",)], [("INT", 1), ("INT", 0)], {}, [] )
  test_result(testGt1, State ([], [("BOOL", True)], {}, []))
  
  # GT2
  testGt2 = State( [("GT",)], [("INT", 0), ("INT", 1)], {}, [] )
  test_result(testGt2, State ([], [("BOOL", False)], {}, []))
  
  # AND1
  testAnd1 = State( [("AND", )], [("BOOL", True), ("BOOL", True)], {}, [] )
  test_result(testAnd1, State ([], [("BOOL", True)], {}, []))
  
  # AND2
  testAnd2 = State( [("AND", )], [("BOOL", False), ("BOOL", True)], {}, [] )
  test_result(testAnd2, State ([], [("BOOL", False)], {}, []))
  
  # NOT
  testNot = State( [("NOT", )], [("BOOL", True)], {}, [] )
  test_result(testNot, State ([], [("BOOL", False)], {}, []))
  
  # JUMP
  testJump = State( [("JUMP", 2), ("INT", 1,), ("INT", 2), ("INT", 3)], [], {}, [] )
  test_result(testJump, State ([("INT", 3)], [], {}, []))
  
  # JMPIFTRUE1
  testIf1 = State( [("JMPIFTRUE", 2), ("INT", 1), ("INT", 2), ("INT", 3)], [("BOOL", True)], {}, [])
  test_result(testIf1, State( [("INT", 3)], [], {}, [] ))
  
  # JMPIFTRUE2
  testIf2 = State( [("JMPIFTRUE", 2), ("INT", 1), ("INT", 2), ("INT", 3)], [("BOOL", False)], {}, [])
  test_result(testIf2, State( [("INT", 1), ("INT", 2), ("INT", 3)], [], {}, [] ))
  
  # VAR
  testVar = State( [("VAR", 'x')], [], {'x': ("INT", 10)}, [] )
  test_result(testVar, State ([], [("INT", 10)], {'x': ("INT", 10)}, []))
  
  # FUN
  testFun = State( [("FUN", 'x', [("INT", 2)] )], [], {'x' : ("BOOL", True)}, [] )
  test_result(testFun, State ([], [("CLOS", {'x' : ("BOOL", True)}, 'x', [("INT", 2)])], {'x' : ("BOOL", True)}, []))
  
  # RFUN
  testRfun = State( [("RFUN", 'f', 'x', [("INT", 2)])], [], {}, [] )
  test_result(testRfun, State ([], [("RCLOS", {}, 'f', 'x', [("INT", 2)])], {}, []))
  
  # APPLY1
  testApply1 = State( [("APPLY",)], [("CLOS", {'x' : ("BOOL", True)}, 'z', [("INT", 2)]), ("BOOL", False), ("INT", 42)], {'y': ("INT", 10)}, [] )
  test_result(testApply1, State ([("INT", 2)], [], {'x' : ("BOOL", True), 'z' : ("BOOL", False)}, [([], [("INT", 42)], {'y': ("INT", 10)})]) )
  
  # APPLY2
  testApply2 = State( [("APPLY",), ("COPY", )], [("RCLOS", {'x' : ("BOOL", True)}, 'f', 'z', [("INT", 45), ("BOOL", False)]), ("INT", -99), ("INT", 2)], {'s' : ("INT", 60)}, [] )
  test_result(testApply2, State ([("INT", 45), ("BOOL", False)], [], {'x' : ("BOOL", True), 'z' : ("INT", -99), 'f': ("RCLOS", {'x' : ("BOOL", True)}, 'f', 'z', [("INT", 45), ("BOOL", False)])}, [([("COPY", )], [("INT", 2)], {'s' : ("INT", 60)})] ))
  
  # DUMP
  testDump = State( [], [("INT", 100)], {}, [ ([("POP",)], [("BOOL", True)], {'x': ("INT", 32)}) ] )
  test_result(testDump, State ([("POP",)], [("INT", 100), ("BOOL", True)], {'x': ("INT", 32)}, []))
