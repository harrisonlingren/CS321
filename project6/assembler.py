#!/usr/bin/python
import sys

# global objects
a_table, c_table, l_table = {}, {}, {}
filepath = ''

# tables for hack conversion of asm elements
# (this is long, hold on to your hats...)
jump_table = {
    'null' : '000',
    'JGT' : '001',
    'JEQ' : '010',
    'JGE' : '011',
    'JLT' : '100',
    'JNE' : '101',
    'JLE' : '110',
    'JMP' : '111'
}

dest_table =  {
    'null' : '000',
    'M' : '001',
    'D' : '010',
    'MD' : '011',
    'A' : '100',
    'AM' : '101',
    'AD' : '110',
    'AMD' : '111'
}

predef_table = {
    'SP' : 0,
    'LCL' : 1,
    'ARG' : 2,
    'THIS' : 3,
    'THAT' : 4,
    'R0' : 0,
    'R1' : 1,
    'R2' : 2,
    'R3' : 3,
    'R4' : 4,
    'R5' : 5,
    'R6' : 6,
    'R7' : 7,
    'R8' : 8,
    'R9' : 9,
    'R10' : 10,
    'R11' : 11,
    'R12' : 12,
    'R13' : 13,
    'R14' : 14,
    'R15' : 15,
    'SCREEN' : 16384,
    'KBD' : 24576
}

comp_table = {
    '0' : '101010',
    '1' : '111111',
    '-1' : '111010',
    'D' : '001100',
    'A' : '110000',
    'M' : '110000',
    '!D' : '001101',
    '!A' : '110001',
    '!M' : '110001',
    '-D' : '001111',
    '-A' : '110011',
    '-M' : '110011',
    'D+1' : '011111',
    '1+D' : '011111',
    '1+A' : '110111',
    'A+1' : '110111',
    '1+M' : '110111',
    'M+1' : '110111',
    '1-D' : '001110',
    'D-1' : '001110',
    '1-A' : '110010',
    'A-1' : '110010',
    '1-M' : '110010',
    'M-1' : '110010',
    'D+A' : '000010',
    'A+D' : '000010',
    'D+M' : '000010',
    'M+D' : '000010',
    'D-A' : '010011',
    'A-D' : '010011',
    'D-M' : '010011',
    'M-D' : '010011',
    'A-D' : '000111',
    'D-A' : '000111',
    'M-D' : '000111',
    'D-M' : '000111',
    'D&A' : '000000',
    'A&D' : '000000',
    'D&M' : '000000',
    'M&D' : '000000',
    'D|A' : '010101',
    'A|D' : '010101',
    'D|M' : '010101',
    'M|D': '010101'
}

def main(fp):
    # read things
    instr = openFile(fp)

    # create the hack instructions with magic (or knowledge
    # ...of computing architecture, take your pick)
    build_l_table(instr)
    build_a_table(instr)
    build_c_table(instr)

    # clean everything up before throwing it away
    hack_instr = translate(instr)
    write_hack(hack_instr, fp)

    # We're done!

# read in asm file and prepare it
def openFile(fp):
    # open file by path fn and read lines to asm_instr
    f = open(fp)
    asm_instr = f.readlines()

    # remove commented-out lines, white space and empty elements
    asm_instr = map(filter_line, asm_instr)
    asm_instr = [ j.strip() for j in [ i for i in asm_instr ] ]
    asm_instr = filter(check_if_empty, asm_instr)

    return asm_instr

# for parsing the asm
def filter_line(a, op='//'):
  idx = a.find(op)
  if idx == -1:
    return a
  elif idx == 0:
    return ''
  else:
    if op == '//':
      a = a[:(idx-1)]
    else:
      a = a[:idx]
  return a

# for parsing the asm
def check_if_empty(a):
    return (a != '')

# convert int to binary
int_to_binary = lambda x: x >= 0 and str(bin(x))[2:] or str(bin(x))[3:]

# correct binary with leading 0s
def fix_bin(inp):
  num = int_to_binary(inp)
  length = len(num)
  diff = 16 - length
  rest = [ '0' for i in range(diff) ]
  rest = ''.join(rest)
  return rest + num

# check if instruction is a, c or l
def check_a_instr(instr):
    return (instr.find('@') != -1)

def check_c_instr(instr):
    return (instr.find('(') == -1 and instr.find('@') == -1)

def check_l_instr(instr):
    return (instr.find('(') != -1 and instr.find(')') != -1)

def check_int(obj, base=10, val=None):
    try:
        return int(obj, base)
    except ValueError:
        return val

# build the a table
def build_a_table(asm_instr):
    step = 16
    for symbol in asm_instr:
        if check_a_instr(symbol):
            value = symbol[1:]
            # if value is integer:
            if check_int(value) is not None:
                a_table[symbol] = fix_bin(int(value))
            # otherwise, if value is variable:
            elif value in predef_table.keys():
                a_table[symbol] = fix_bin(predef_table[value])
            # also check if it's already in l_table:
            elif value in l_table.keys():
                a_table[symbol] = l_table[value]
            # don't repeat your work:
            elif symbol in a_table.keys():
                continue
            # if everything is broken and nothing
            # else works, keep on that grind:
            else:
                a_table[symbol] = fix_bin(step)
                step += 1

# build the c table
def build_c_table(asm_instr):
    for symbol in asm_instr:
        if check_c_instr(symbol):
            semicolon = symbol.find(';')
            equals = symbol.find('=')

            # dest=comp;jump
            if equals != -1 and semicolon != -1:
                dest = symbol[:equals]
                comp = symbol[(equals + 1):semicolon]
                jump = symbol[(semicolon + 1):]
                if comp.find('M') != -1:
                    a_bit = '1'
                else:
                    a_bit = '0'

                c_table[symbol] = '111' + a_bit + comp_table[comp] + dest_table[dest] + jump_table[jump]

            # comp;jump
            if equals == -1 and semicolon != -1:
                comp = symbol[:semicolon]
                jump = symbol[(semicolon + 1):].strip()

                if comp.find('M') != -1:
                    a_bit = '1'
                else:
                    a_bit = '0'

                c_table[symbol] = '111' + a_bit + comp_table[comp] + dest_table['null'] + jump_table[jump]

            # dest=comp
            if equals != -1 and semicolon == -1:
                dest = symbol[:equals]
                comp = symbol[(equals + 1):]

                if comp.find('M') != -1:
                    a_bit = '1'
                else:
                    a_bit = '0'

                c_table[symbol] = '111' + a_bit + comp_table[comp] + dest_table[dest] + jump_table['null']

# build the l table
def build_l_table(asm_instr):
    step = 0
    for symbol in asm_instr:
        if check_l_instr(symbol):
            step -= 1
            l_table[symbol[1:-1]] = fix_bin(step)

# begin to translate the asm to hack
def translate(asm_instr):
    # initialize array for hack instructions
    hack_instr = []
    print('\nAssembly Code:')
    for instr in asm_instr:
        print('  > ' + instr)
        if check_a_instr(instr):
            hack_instr.append(a_table[instr])
        elif check_c_instr(instr):
            hack_instr.append(c_table[instr])
    return hack_instr

# write out hack file
def write_hack(hack_instr, fp):
    hack_fp = filter_line(fp, op='.')
    hack_fp += '.hack'

    hack_file = open(hack_fp, 'w')
    print('\nHack Code:')
    for line in hack_instr:
        print('  > ' + line)
        hack_file.write(line + '\n')

    hack_file.close()

# start the things
if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        main(filepath)
    else:
        print ('Please include the path of your .asm file as an argument')
