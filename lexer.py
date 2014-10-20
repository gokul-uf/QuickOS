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

#function to identify if input is a valid arithmetic expression
#input: list of list of lexemes
#output: True or False
def isValidArith(input):
    if input[-1] not in op_list and input[0] not in op_list:
        flag = 0
        for i in input[1:-1]:
            if flag == 0 and i not in op_list:
                return False
            elif flag == 1 and i in op_list:
                return False
            else:
                if flag == 0:
                    flag = 1
                else:
                    flag = 0
        return True
    return False			

#function to identify if input is a valid assignment statement
#input: list of list of lexemes
#output: True or False
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
        print (i+'s')
        for j in TokenType[i]:
            temp_str = temp_str + '   ' + j
        print (temp_str,'\n')
        

#function to split input on basis of newline and ; delimiter
#input: A string, the program without comments
#output: list of lists with lexemes in each line and statement
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
	
#removes comments
#input: A string, the program itself
#output: A string, with the comments removed
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
#converts the input string into lexemes
#input:   a string containing a single statement, with the ending ; and : removed
#output: a list removing all white spaces, grouping all sets of only numbers together, grouping alphabets-number combinations, grouping various
# operator combos together, and taking any other character like ( on its own
def lexemize(statement):
    return re.findall("\s*(\w+|[\+-/\*%\^<>=!:\.]+|.)",statement)

#Checks if any of the input lexemes are not valid operators	
#input:   a list of lexemes corresponding to a statement
#output: a list of all symbols that don't form valid operators
def validate_ops(lexd_stmt) :
	return [op for op in lexd_stmt if (op not in op_list and op not in spec_sym_list and not re.match("^[\w_]*$", op))]

#Checks if any of the input lexemes are not valid identifiers
#input:   a list of lexemes corresponding to a statement
#output: a list of all identifiers that are not valid
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
#input: two lists
#output: True or False
def comp ( a,b ):
	if len(a) != len(b):
		return False
	for i in range(0,len(b)):
		if a[i] != b[i]:
			return False
	return True
	
#Function to check if input list is a valid variable declaration
#input: list of list containing lexemes
#output: True or False
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

#Function to check if input is a valid logical expression
#Input: list of logical expression
#Output: True or False
def isValidLogicalExpr(input):
    not_e = False
    or_e = False
    and_e = False
    for i in input:
        if i == "not":
            not_e = True
        elif i ==  "and":
            if not_e or or_e or and_e:
                print("Invalid Expression: " + " ".join(input))
                return False
            and_e = True
        elif i == "or":
            if not_e or and_e or or_e:
                print("Invalid Expression: " + " ".join(input))
                return False
            or_e = True
        else:
            and_e = False
            or_e = False
            not_e = False
    return True

#Function to check if input is a valid statement block
#Input: list of statements
#Output: True if the statement block is lexically valid, False otherwise
def isValidStatementBlock(input):
    return True

#Function to check if input 'if's are valid
#Input: list of lexemes that start with an if and end with an endif
#Output: True if the input is lexically valid, False otherwise
def isValidIfStatement(input):
    body = []
    if input[0][0] != "if" or input[0][1] != "(":
        print ("Improper if syntax: " + " ".join(input[0]))
        return False
    open_br = True
    expr_list = []
    
    for  i in input[0][2:]:
        if open_br:
            if i == ")":
                open_br = False
                if not isValidLogicalExpr(expr_list):
                    print ("Improper argument list: (" + " ".join(expr_list) + ")")
                expr_list = []
                continue
            else:
                expr_list += i
                continue

    stmts = []
    for i in input[1:]:
        if i[0] != "elseif" and i[0] != "else" and i[0] != "endif":
            stmts += i
        else:
            isValidStatementBlock(stmts)
            stmts = []
            if i[0] == "elseif":
                if i[1] != "(":
                    print ("Improper elseif syntax- missing (: " + " ".join(i[0]))
                else:
                    if not isValidLogicalExpr(i[2:-1]):
                        print ("Improper argument list: (" + " ".join(i[2:-1]) + ")")
    return True                  
	    
#Function to check if input list is a valid function call
#input: list of list containing lexemes
#output: True or False
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

	
#main function	
if __name__ == "__main__":
    filename = input("Enter a file name: ")
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
    print(lex_str[:-2])
    print('')
    print('')
    print('           Lexemes by Category')
    print('           -------------------')
    print('')

    token_count(lex)       
    
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


