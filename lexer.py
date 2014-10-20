import re

keyword_list = ['define', 'enddef', 'global', 'scheduler', 'if',
                'else', 'elseif', 'endif']

dt_list = ['int', 'float', 'bool', 'process', 'process_list', 'timer']

op_list = ['+', '-', '*', '/', '%', '^', '<', '>',
           '<=', '>=', '==', '!=', '=', '!', 'and', 'or', '::']

spec_sym_list = ['(', ')', '.', ':', '//', '/*', '*/', ';',',']


#classifies each token into a token type
#input: a token
#output: A string with token type
def token_type (input):
    if input in keyword_list:
        return "keyword"
    elif input in dt_list:
        return "datatype"
    elif input in op_list:
        return "operator"
    elif input in spec_sym_list:
        return "special symbol"
    else:
        return "Not A token"
'''
<assignment> -> id = <opern>; | id = <fn_call>
<fn_call> -> id . id (<arg_list>); | memory :: id(<arg_list>); | schedule :: id(<arg_list>);
<arg_list> -> <arg_list2> | e
<arg_list2> -> id, | <fn_call>, | id | <fn_call>
<opern> -> <opern> + <a_opern> | <opern> - <a_opern> | <a_opern> 
<a_opern> -> <a_opern> * <b_opern> | <a_opern> / <b_opern> | 
             <a_opern> % <b_opern> | <b_opern>
<b_opern> ->  <base_id> ^ <b_opern> | <base_id>
<base_id> -> id | <intliteral> | <floatliteral> | <boolliteral> | <fn_call>
'''
#Function to identify if input is a valid arithmetic expression
#Input: list of list of lexemes
#Output: True or False
def isValidArith(input):
    pass	
	
	
#Function to identify if input is a valid assignment statement
#Input: list of list of lexemes
#Output: True or False
def isValidAssign(input):
    if validate_ids(input[0]) == [] and input[1] == '=' :
        if isFuncCall(input[2:]):
            return True
        elif isValidArith(input[2:]):
            return True
    return False


#takes a list of lexemes, classifies and prints according to different token type
#input : set of identified tokens
#output: Nothing, classifies tokens as keyword, datatype.etc and prints them
def token_count (input):
    TokenType = {"keyword":set() ,"datatype": set(), "operator":set(),"special symbol":set(),"identifier":set()}
    
    for i in input:
        temp = token_type(i)
        if not temp == 'Not A token':
            TokenType[temp].add(i)
        else:
            TokenType["identifier"].add(i)

    temp_str = ''
    for i in TokenType:
        temp_str = ''
        print i+'s'
        for j in TokenType[i]:
            temp_str = temp_str + '   ' + j
        print temp_str,'\n'
        

#function to split input on basis of newline and ; delimiter
def split( ip ):

    n = len(ip)
    i = 0
    temp2 = ""
    # converts : to \n for splitting on basis of :,
    # and ensuring that :: are not removed
    while i<n:
        if ip[i] == ':':
            if i + 1<n:
                if ip[i + 1] != ':':
                    if i - 1 >= 0:
                        if ip[i - 1] != ':':
                            temp2 += '\n'
                        else:
                            temp2 += ip[i]
                    else:
                        temp2 += ip[i]
                else:
                     temp2 += ip[i]   
            else:
                temp2 += '\n'
        else:
            temp2 += ip[i]
        i += 1        

    temp = temp2.split('\n')   #splits on basis of line
          
    ret_val = []
    
    for i in temp:
        ret_val = ret_val + i.split(';') #splits on basis of ;

    return ret_val

def remove_comments( ip ):
    n = len(ip)
    i = 0
    commfree = ""
    while i<n:
        if ip[i] == '"':
            commfree = commfree + ip[i]
            while ip[i] != '"' and i<n:
                commfree = commfree + ip[i]
                i+=1
            commfree = commfree + ip[i]
            i +=1
            continue
        elif ip[i] == '/' and i+1 <n:
            if ip[i+1] == '/':
                i += 1
                while i<n and ip[i] != '\n':
                    i+=1
                i += 1
                continue
            elif ip[i+1] == '*':
                i += 2
                while i<n:
                    if ip[i] == '*':
                        i += 1
                        if ip[i] == '/':
                            i += 1
                            break
                    i += 1
                continue
            else:
                commfree = commfree + ip[i]
                i += 1
                continue
        else:
            commfree = commfree + ip[i]
            i += 1
    return commfree

#userInput = sys.stdin.readlines()
#print(remove_comments(userInput))

# input:   a string containing a single statement, with the ending ; and : removed
# returns: a list removing all white spaces, grouping all sets of only numbers together, grouping alphabets-number combinations, grouping various
#          operator combos together, and taking any other character like ( on its own
def lexemize(statement):
    return re.findall("\s*(\w+|[\+-/\*%\^<>=!:\.]+|.)",statement)

# input:   a list of lexemes corresponding to a statement
# returns: a list of all symbols that don't form valid operators
def validate_ops(lexd_stmt) :
    #i = 0
    #invalid_ops = []
    #for line_op in lexd_stmt:
    #    i+= 1
    #    j = 1
    #    for op in line_op:
    #        if (op not in op_list and op not in spec_sym_list and not re.match("^[\w_]*$", op)):
    #            invalid_ops += [(op,i,j)]
    #        j += len(op)
    #return invalid_ops
    return [op for op in lexd_stmt if (op not in op_list and op not in spec_sym_list and not re.match("^[\w_]*$", op))]


# input:   a list of lexemes corresponding to a statement
# returns: a list of all identifiers that are not valid
def validate_ids(lexd_stmt) :
    inv_id = []
    n = len(lexd_stmt)
    i = 0
    while i < n:
        iden = lexd_stmt[i]
        if re.match("^\w+$", iden) and not re.match("^\d+$", iden) and not re.match("^[A-Z]([A-Z_]*[A-Z])?$|^[a-z]([a-z_]*[a-z])?$", iden):
            if i + 1 < n:
                if lexd_stmt[i+1] != ")":
                    inv_id += [iden]
            else:
                inv_id += [iden]
        i += 1
    return inv_id
    
#function to compare two lists	
def comp ( a,b ):
	if len(a) != len(b):
		return False
	for i in range(0,len(b)):
		if a[i] != b[i]:
			return False
	return True
	
#Function to check if input list is a valid variable declaration
def isVardecl(input):
	if input[0] in dt_list and validate_ids(input[1]) == [] and input[2] == '=' :
		return True
	return False

#Function to check if input is a valid list of arguments
#Input: list of arguments, possibly with ','
#Output: True or False	
def isValidArgList(input):
	temp = [x for x in input if x != [',']]
	if(validate_ids(temp) == []):
		return True
	else:
		return False
		
#Function to check if input list is a valid function call
def isFuncCall(input):
    if validate_ids(input[0]) == [] and input[1] == ["."] and validate_ids(input[2]) == [] and input[3] == ['('] and input[-1] == [')']:
        if(isValidArgList(input[4:-1])):
            return True
        else:
            return False
            
    if input[0] == ["memory"] and input[1] == ["::"] and validate_ids(input[2]) == [] and input[3] == ['('] and input[-1] == [')']:
        if(isValidArgList(input[4:-1])):
            return True
        else:
            return False
		
    if input[0] == ["schedule"] and input[1] == ["::"] and validate_ids(input[2]) == [] and input[3] == ['('] and input[-1] == [')']:
        if(isValidArgList(input[4:-1])):
            return True
        else:
            return False
	
    return False

#Function to verify if the global fn has been defined properly
#input: A list of list of lexemes, one list per lexemes of each line
#output: True/False
def verify_global(ip):
	global_header = ["define","global","(",")"]
	if comp(global_header,ip[0]) == False:	
		return False
	i = 1
	while(cmp(ip[i],["enddef"]) == False):
		if(isVardecl(ip[i]) or isFuncCall(ip[i])) == False:
			return False
		i = i+1
	return True

if __name__ == "__main__":
    filename = raw_input("Enter a file name: ")
    f = open(filename, 'r')
    code = f.read()
    cfree = remove_comments(code)
    sp = split(cfree)
    lex = []

    print('')
    print('')
    print('           All Lexemes')
    print('           -------')
    print('')

    lex_str = ""
    for i in sp:
        if i: 
            lex += lexemize(i)
            lex_str += str(lexemize(i))[1:-1]
            lex_str += ", "
    print(lex_str)[:-2]
    print('')
    print('')
    print('           Lexemes by Category')
    print('           -------')
    print('')

    token_count(lex)       
    #print(lex)
    #print(len(lex))

    inv_op = validate_ops(lex)
    if len(inv_op) > 0:
        print('Invalid ops detected: ' + str(inv_op)[1:-1])
    else:
        print('All ops are valid')

    inv_id = validate_ids(lex)
    if len(inv_id) >0:
        print('Invalid identifiers detected: ' + str(inv_id)[1:-1])
    else:
        print('All identifiers are valid')


