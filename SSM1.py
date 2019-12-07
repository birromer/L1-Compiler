# -*- coding: utf-8 -*-

class SSM1:
  def __init__(self):
    self.code  = []
    self.stack = [] 
    self.env   = []
    self.dump  = []
    
  def step(self):
    
    if self.code == []:
      to_restore = self.dump.pop(0) 
      new_code  = to_restore[0]
      new_stack = to_restore[1]
      new_env   = to_restore[2] 
      sv = self.stack.pop(0)
      
      self.code  = new_code
      self.stack = new_stack
      self.env   = new_env
      self.stack.insert(0, sv) 
    
    instruction = self.code.pop(0)
    if instruction[0] == "INT":
      self.stack.insert(0, instruction)

    elif instruction[0] == "BOOL":
      self.stack.insert(0, instruction)

    elif instruction[0] == "POP":
      self.stack.pop(0)
    
    elif instruction[0] == "ADD":
      value1 = self.stack.pop(0)
      value2 = self.stack.pop(0)
      self.stack.insert(0, ("INT", value1[1]+value2[1]))

    elif instruction[0] == "INV":
      value = self.stack.pop(0)
      self.stack.insert(0, ("INT", -value))

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
      if value1 == False:
        self.stack.pop(0)
        self.stack.insert(0, ("BOOL", False))
      else:
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

    elif instruction[0] == "JUMPIFTRUE":
      value = self.stack.pop(0)
      if value == True:
        i = 1
        n = instruction[1]
        while i <= n:
          self.code.pop(0)
          i += 1  

    elif instruction[0] == "VAR":
      op = self.code.pop(0)
      value = self.enviroment[op]
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
        new_env  = clos[0]
        new_var  = clos[1]
        new_code = clos[2]

        self.code  = new_code
        self.stack = []
        self.env   = new_env                
        self.env[new_var] = sv
        
      elif clos[0] == "RCLOS":
        new_env  = clos[0]
        new_func = clos[1]
        new_var  = clos[2]
        new_code = clos[3]
        
        self.code = new_code
        self.stack = []
        self.env = new_env
        self.env[new_var] = sv
        self.env[new_func] = ("RCLOS", new_env, new_func, new_var, new_code)
        
      else:
        print("deu bem ruim")
      
  def run(self, code):
    self.code = code
    while not (self.code == [] and self.code == []):
      self.step()
    
    return self.stack.pop(0)
      
if __name__ == "__main__":
  ssm1 = SSM1()
  
  code = compileSSM1(('let', 'x', 'int', ('+', 3, ('+', 3, 4)), ('if', True, True, False)))
  res = ssm1.run(code)
  
  print(res

