README
======
<note>Please do!! :) </note>

The code to be run is lexer.py.
once started, this will ask for test input file name.

* Give one of the file name mentioned in the "Input Test Files" section

* It will output the following:
	$ List of Lexemes identified in the code.
	$ Category wise list of lexemes.
	$ Whether any Invalid operators are detected
	$ Whether any Invalid identifiers are detected
	
Input Test Files
================
There are five test files in total provided with the code. 
The input test files are present in the same directory as the code.

Files:
------
	* test_ip_1
	* test_ip_2
	* test_ip_3
	* test_ip_4
	* test_ip_5
	
Lexical rules
=============
<program> -> <global><main>
<main> -> <scheduler> | <mmu>

<global> -> define global(): <var_decls><fn_calls> enddef
<var_decls> -> <var_decl><var_decls> | e
<var_decl> -> <data_type> id <initializn>;
<data_type> -> int, float, bool, process, process_list, timer 
<initializn> -> = const | e
<fn_calls> -> <fn_call><fn_calls> | e
<fn_call> -> id . id (<arg_list>); | memory :: id(<arg_list>); | schedule :: id(<arg_list>);
<arg_list> -> <arg_list2> | e
<arg_list2> -> id, | <fn_call>, | id | <fn_call>

<scheduler> -> define scheduler (process_list id): <body> enddef
<mmu> -> define mmu (process id): <body> enddef

<body> -> <condition><body> | <stmt><body> | e
<stmt> -> <assignment> | <fn_call>
<assignment> -> id = <opern>; | id = <fn_call>

<opern> -> <opern> + <a_opern> | <opern> - <a_opern> | <a_opern> 
<a_opern> -> <a_opern> * <b_opern> | <a_opern> / <b_opern> | 
             <a_opern> % <b_opern> | <b_opern>
<b_opern> ->  <base_id> ^ <b_opern> | <base_id>
<base_id> -> id | <intliteral> | <floatliteral> | <fn_call>

<condition> -> if (<bool_exp>): <body> <condition_expanded> endif
<condition_expanded> -> elseif (<bool_exp>): <body> <condition_expanded> | <condition_else>
<condition_else> -> else: <body> | e
<bool_exp> -> <bool_exp> or <bool_exp_and> | <bool_exp_and>
<bool_exp_and> -> <bool_exp_and> and <bool_exp_not> | <bool_exp_not>
<bool_exp_not> -> not <bool_exp_not> | id | <boolliteral>

Code Status
===========
Complete 