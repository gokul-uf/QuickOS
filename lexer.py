import re
keyword_list = ['define', 'enddef', 'global', 'scheduler', 'if',
                'else', 'elseif', 'endif']

dt_list = ['int', 'float', 'bool', 'process', 'process_list', 'timer']

op_list = ['+', '-', '*', '/', '%', '^', '<', '>',
           '<=', '>=', '==', '!=', '=', '!', 'and', 'or', '::']

spec_sym_list = ['(', ')', '.', ':', '//', '/*', '*/', ';']

#classifies each token into a token type
def token_type (input):
    if input in keyword_list:
        return "keyword"
    elif input in dt_list:
        return "datatype"
    elif input in op_list:
        return "operator"
    elif input in specSym_list:
        return "special symbol"
    else:
        return "Not A token"

#takes a list of tokens, classifies and prints according to different token type
def token_count (input):
    TokenType = {"keyword":[] ,"datatype": [], "operator":[],"special symbol":[]}
    for i in input:
        temp = token_type(i)
        TokenType[temp] = TokenType[temp] + i
        

    

#function to split input on basis of newline and ; delimiter
def split( ip ):
    temp = ip.split('\n')   #splits on basis of line

    temp2 = []
    
    for i in temp:
        temp2 = temp2 + i.split(':') #splits on basis of :
    
    ret_val = []
    
    for i in temp2:
        ret_val = ret_val + i.split(';') #splits on basis of ;

    return ret_val

# input:   a string containing a single statement, with the ending ; and : removed
# returns: a list removing all white spaces, grouping all sets of only numbers together, grouping alphabets-number combinations, grouping various
#          operator combos together, and taking any other character like ( on its own
def lexemize(statement):
    return re.findall("\s*(\w+|[\+-/\*%\^<>=!:\.]+|.)",statement)

# input:   a list of lexemes corresponding to a statement
# returns: a list of all symbols that don't form valid operators
def validate_ops(lexd_stmt) :
    return [op for op in lexd_stmt if (op not in op_list and op not in spec_sym_list and not re.match("^[\w_]*$", op))]


# input:   a list of lexemes corresponding to a statement
# returns: a list of all identifiers that are not valid
def validate_ids(lexd_stmt) :
    return [iden for iden in lexd_stmt if re.match("^\w+$", iden) and not re.match("^\d+$", iden) and not re.match("^[A-Z]([A-Z_]*[A-Z])?$|^[a-z]([a-z_]*[a-z])?$", iden)]

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
