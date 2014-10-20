Lexical rules:

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
<base_id> -> id | <intliteral> | <floatliteral> | <boolliteral> | <fn_call>
