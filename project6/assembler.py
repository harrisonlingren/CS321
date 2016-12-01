def main():
    return 0




def openFile(fn):
    # open file by path fn and read lines to asm_instr
    f = open(fn)
    asm_instr = f.readlines()

    # remove commented-out lines, white space and empty elements
    asm_instr = map(remove_comments, asm_instr)
    asm_instr = [ line.strip for line in [ char for char in asm_instr ] ]
    asm_instr = filter(check_if_empty, asm_instr)

    return asm_instr


def remove_comments(a, op="//"):
  idx = a.find(op)
  if idx == -1:
    return a
  elif idx == 0:
    return ''
  else:
    if op == "//":
      a = a[:(idx-1)]
    else:
      a = a[:idx]
  return a


def check_if_empty(a):
    return (a != '')

def build_a_table():
    return 0

def build_c_table():
    return 0

def build_l_table():
    return 0






def translate(asm_instr):
    # initialize array for hack instructions
    hack_instr = []
    for instr in asm_instr:
        if (instr.find('@') != -1):
            hack_instr.append(a_table[instr])
        elif (isntr.find("(") == -1 and instr.find("@") == -1):
            hack_instr.append(c_table[instr])
        return hack_instr
