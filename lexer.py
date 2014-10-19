import re
keyword_list = ['define', 'enddef', 'global', 'scheduler', 'if',
                'else', 'elseif', 'endif']

dt_list = ['int', 'float', 'bool', 'process', 'process_list', 'timer']

op_list = ['+', '-', '*', '/', '%', '^', '<', '>',
           '<=', '>=', '==', '!=', '=', '!', 'and', 'or', '::']

specSym_list = ['(', ')', '.', ':', '//', '/*', '*/', ';']


def split( ip ):

    temp = ip.split('\n')   #splits on basis of line
    ret_val = []
    
    for i in temp:
        ret_val = ret_val + i.split(';') #splits on basis of ;

    return ret_val

ip = '''define global():
int MEM_REQUIRED = 2;
int MAX_MEMORY = 1024;
int mem_location = 0;
enddef
define mmu(process proc):
mem_location = proc.pid * 2 - 2;
if (mem_location > MAX_MEMORY - 2):
schedule::exit(proc);
else
memory::reserve(MEM_REQUIRED, mem_location);
proc.assign(mem_location);
endif
enddef'''

print(split(ip))

def lexemize(statement):

    return re.findall("\s*(\d+|\w[\w_]+|[\+-/\*%\^<>=!:\.]+|.)",statement) #uses regex to split statement into constant integers, identifiers, groups of operators
