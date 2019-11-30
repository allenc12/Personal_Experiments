%defines
%expect 2
%verbose

%{
#include <stdio.h>
extern void yyerror(const char *s);
extern int yylex(void);
extern FILE *yyout;
extern char *yytext;
extern int yylineno;
extern int fncount, varcount;
%}

%token	IDENTIFIER I_CONSTANT F_CONSTANT STRING_LITERAL FUNC_NAME SIZEOF
%token	PTR_OP INC_OP DEC_OP LEFT_OP RIGHT_OP LE_OP GE_OP EQ_OP NE_OP
%token	AND_OP OR_OP MUL_ASSIGN DIV_ASSIGN MOD_ASSIGN ADD_ASSIGN
%token	SUB_ASSIGN LEFT_ASSIGN RIGHT_ASSIGN AND_ASSIGN
%token	XOR_ASSIGN OR_ASSIGN
%token	TYPEDEF_NAME ENUMERATION_CONSTANT

%token	TYPEDEF EXTERN STATIC AUTO REGISTER INLINE
%token	CONST RESTRICT VOLATILE
%token	BOOL CHAR SHORT INT LONG SIGNED UNSIGNED FLOAT DOUBLE VOID
%token	COMPLEX IMAGINARY
%token	STRUCT UNION ENUM ELLIPSIS

%token	CASE DEFAULT IF ELSE SWITCH WHILE DO FOR GOTO CONTINUE BREAK RETURN

%token	ALIGNAS ALIGNOF ATOMIC GENERIC NORETURN STATIC_ASSERT THREAD_LOCAL

%start translation_unit
%%

primary_expression
	:	IDENTIFIER
		{
			fprintf(yyout, "IDENTIFIER\t%s\n", yytext);
		}
	|	constant
		{
			fprintf(yyout, "constant\t%s\n", yytext);
		}
	|	string
		{
			fprintf(yyout, "string\t%s\n", yytext);
		}
	|	'(' expression ')'
		{
			fprintf(yyout, "'(' expression ')'\t%s\n", yytext);
		}
	|	generic_selection
		{
			fprintf(yyout, "generic_selection\t%s\n", yytext);
		}
	;

constant
	:	I_CONSTANT
		{
			fprintf(yyout, "I_CONSTANT\t%s\n", yytext);
		}		/* includes character_constant */
	|	F_CONSTANT
		{
			fprintf(yyout, "F_CONSTANT\t%s\n", yytext);
		}
	|	ENUMERATION_CONSTANT
		{
			fprintf(yyout, "ENUM_CONST\t%s\n", yytext);
		}	/* after it has been defined as such */
	;

enumeration_constant		/* before it has been defined as such */
	:	IDENTIFIER
		{
			fprintf(yyout, "IDENTIFIER\t%s\n", yytext);
		}
	;

string
	:	STRING_LITERAL
		{
			fprintf(yyout, "STRING_LITERAL\t%s\n", yytext);
		}
	|	FUNC_NAME
		{
			fprintf(yyout, "FUNC_NAME\t%s\n", yytext);
		}
	;

generic_selection
	:	GENERIC '(' assignment_expression ',' generic_assoc_list ')'
		{
			fprintf(yyout, "GENERIC '(' assignment_expression, generic_assoc_list ')'\t%s\n", yytext);
		}
	;

generic_assoc_list
	:	generic_association
		{
			fprintf(yyout, "generic_association\t%s\n", yytext);
		}
	|	generic_assoc_list ',' generic_association
		{
			fprintf(yyout, "generic_assoc_list , generic_association\t%s\n", yytext);
		}
	;

generic_association
	:	type_name ':' assignment_expression
		{
			fprintf(yyout, "type_name : assignment_expression\t%s\n", yytext);
		}
	|	DEFAULT ':' assignment_expression
		{
			fprintf(yyout, "DEFAULT : assignment_expression\t%s\n", yytext);
		}
	;

postfix_expression
	:	primary_expression
		{
			fprintf(yyout, "primary_expression\t%s\n", yytext);
		}
	|	postfix_expression '[' expression ']'
		{
			fprintf(yyout, "postfix_expression '[' expression ']'\t%s\n", yytext);
		}
	|	postfix_expression '(' ')'
		{
			fprintf(yyout, "postfix_expression '(' ')'\t%s\n", yytext);
		}
	|	postfix_expression '(' argument_expression_list ')'
		{
			fprintf(yyout, "postfix_expression '(' argument_expression_list ')'\t%s\n", yytext);
		}
	|	postfix_expression '.' IDENTIFIER
		{
			fprintf(yyout, "postfix_expression '.' IDENTIFIER\t%s\n", yytext);
		}
	|	postfix_expression PTR_OP IDENTIFIER
		{
			fprintf(yyout, "postfix_expression PTR_OP IDENTIFIER\t%s\n", yytext);
		}
	|	postfix_expression INC_OP
		{
			fprintf(yyout, "postfix_expression INC_OP\t%s\n", yytext);
		}
	|	postfix_expression DEC_OP
		{
			fprintf(yyout, "postfix_expression DEC_OP\t%s\n", yytext);
		}
	|	'(' type_name ')' '{' initializer_list '}'
		{
			fprintf(yyout, "'(' type_name ')' '{' initializer_list '}'\t%s\n", yytext);
		}
	|	'(' type_name ')' '{' initializer_list ',' '}'
		{
			fprintf(yyout, "'(' type_name ')' '{' initializer_list ',' '}'\t%s\n", yytext);
		}
	;

argument_expression_list
	:	assignment_expression
		{
			fprintf(yyout, "assignment_expression\t%s\n", yytext);
		}
	|	argument_expression_list ',' assignment_expression
		{
			fprintf(yyout, "argument_expression_list ',' assignment_expression\t%s\n", yytext);
		}
	;

unary_expression
	:	postfix_expression
		{
			fprintf(yyout, "postfix_expression\t%s\n", yytext);
		}
	|	INC_OP unary_expression
		{
			fprintf(yyout, "INC_OP unary_expression\t%s\n", yytext);
		}
	|	DEC_OP unary_expression
		{
			fprintf(yyout, "DEC_OP unary_expression\t%s\n", yytext);
		}
	|	unary_operator cast_expression
		{
			fprintf(yyout, "unary_operator cast_expression\t%s\n", yytext);
		}
	|	SIZEOF unary_expression
		{
			fprintf(yyout, "SIZEOF unary_expression\t%s\n", yytext);
		}
	|	SIZEOF '(' type_name ')'
		{
			fprintf(yyout, "SIZEOF '(' type_name ')'\t%s\n", yytext);
		}
	|	ALIGNOF '(' type_name ')'
		{
			fprintf(yyout, "ALIGNOF '(' type_name ')'\t%s\n", yytext);
		}
	;

unary_operator
	:	'&'
		{
			fprintf(yyout, "'&'\t%s\n", yytext);
		}
	|	'*'
		{
			fprintf(yyout, "'*'\t%s\n", yytext);
		}
	|	'+'
		{
			fprintf(yyout, "'+'\t%s\n", yytext);
		}
	|	'-'
		{
			fprintf(yyout, "'-'\t%s\n", yytext);
		}
	|	'~'
		{
			fprintf(yyout, "'~'\t%s\n", yytext);
		}
	|	'!'
		{
			fprintf(yyout, "'!'\t%s\n", yytext);
		}
	;

cast_expression
	:	unary_expression
		{
			fprintf(yyout, "unary_expression\t%s\n", yytext);
		}
	|	'(' type_name ')' cast_expression
		{
			fprintf(yyout, "'(' type_name ')' cast_expression\t%s\n", yytext);
		}
	;

multiplicative_expression
	:	cast_expression
		{
			fprintf(yyout, "cast_expression\t%s\n", yytext);
		}
	|	multiplicative_expression '*' cast_expression
		{
			fprintf(yyout, "multiplicative_expression '*' cast_expression\t%s\n", yytext);
		}
	|	multiplicative_expression '/' cast_expression
		{
			fprintf(yyout, "multiplicative_expression '/' cast_expression\t%s\n", yytext);
		}
	|	multiplicative_expression '%' cast_expression
		{
			fprintf(yyout, "multiplicative_expression '%%' cast_expression\t%s\n", yytext);
		}
	;

additive_expression
	:	multiplicative_expression
		{
			fprintf(yyout, "multiplicative_expression\t%s\n", yytext);
		}
	|	additive_expression '+' multiplicative_expression
		{
			fprintf(yyout, "additive_expression '+' multiplicative_expression\t%s\n", yytext);
		}
	|	additive_expression '-' multiplicative_expression
		{
			fprintf(yyout, "additive_expression '-' multiplicative_expression\t%s\n", yytext);
		}
	;

shift_expression
	:	additive_expression
		{
			fprintf(yyout, "additive_expression\t%s\n", yytext);
		}
	|	shift_expression LEFT_OP additive_expression
		{
			fprintf(yyout, "shift_expression LEFT_OP additive_expression\t%s\n", yytext);
		}
	|	shift_expression RIGHT_OP additive_expression
		{
			fprintf(yyout, "shift_expression RIGHT_OP additive_expression\t%s\n", yytext);
		}
	;

relational_expression
	:	shift_expression
		{
			fprintf(yyout, "shift_expression\t%s\n", yytext);
		}
	|	relational_expression '<' shift_expression
		{
			fprintf(yyout, "relational_expression '<' shift_expression\t%s\n", yytext);
		}
	|	relational_expression '>' shift_expression
		{
			fprintf(yyout, "relational_expression '>' shift_expression\t%s\n", yytext);
		}
	|	relational_expression LE_OP shift_expression
		{
			fprintf(yyout, "relational_expression LE_OP shift_expression\t%s\n", yytext);
		}
	|	relational_expression GE_OP shift_expression
		{
			fprintf(yyout, "relational_expression GE_OP shift_expression\t%s\n", yytext);
		}
	;

equality_expression
	:	relational_expression
		{
			fprintf(yyout, "relational_expression\t%s\n", yytext);
		}
	|	equality_expression EQ_OP relational_expression
		{
			fprintf(yyout, "equality_expression EQ_OP relational_expression\t%s\n", yytext);
		}
	|	equality_expression NE_OP relational_expression
		{
			fprintf(yyout, "equality_expression NE_OP relational_expression\t%s\n", yytext);
		}
	;

and_expression
	:	equality_expression
		{
			fprintf(yyout, "equality_expression\t%s\n", yytext);
		}
	|	and_expression '&' equality_expression
		{
			fprintf(yyout, "and_expression '&' equality_expression\t%s\n", yytext);
		}
	;

exclusive_or_expression
	:	and_expression
		{
			fprintf(yyout, "and_expression\t%s\n", yytext);
		}
	|	exclusive_or_expression '^' and_expression
		{
			fprintf(yyout, "exclusive_or_expression '^' and_expression\t%s\n", yytext);
		}
	;

inclusive_or_expression
	:	exclusive_or_expression
		{
			fprintf(yyout, "exclusive_or_expression\t%s\n", yytext);
		}
	|	inclusive_or_expression '|' exclusive_or_expression
		{
			fprintf(yyout, "inclusive_or_expression '|' exclusive_or_expression\t%s\n", yytext);
		}
	;

logical_and_expression
	:	inclusive_or_expression
		{
			fprintf(yyout, "inclusive_or_expression\t%s\n", yytext);
		}
	|	logical_and_expression AND_OP inclusive_or_expression
		{
			fprintf(yyout, "logical_and_expression AND_OP inclusive_or_expression\t%s\n", yytext);
		}
	;

logical_or_expression
	:	logical_and_expression
		{
			fprintf(yyout, "logical_and_expression\t%s\n", yytext);
		}
	|	logical_or_expression OR_OP logical_and_expression
		{
			fprintf(yyout, "logical_or_expression OR_OP logical_and_expression\t%s\n", yytext);
		}
	;

conditional_expression
	:	logical_or_expression
		{
			fprintf(yyout, "logical_or_expression\t%s\n", yytext);
		}
	|	logical_or_expression '?' expression ':' conditional_expression
		{
			fprintf(yyout, "logical_or_expression '?' expression ':' conditional_expression\t%s\n", yytext);
		}
	;

assignment_expression
	:	conditional_expression
		{
			fprintf(yyout, "conditional_expression\t%s\n", yytext);
		}
	|	unary_expression assignment_operator assignment_expression
		{
			fprintf(yyout, "unary_expression assignment_operator assignment_expression\t%s\n", yytext);
		}
	;

assignment_operator
	:	'='
		{
			fprintf(yyout, "'='\t%s\n", yytext);
		}
	|	MUL_ASSIGN
		{
			fprintf(yyout, "MUL_ASSIGN\t%s\n", yytext);
		}
	|	DIV_ASSIGN
		{
			fprintf(yyout, "DIV_ASSIGN\t%s\n", yytext);
		}
	|	MOD_ASSIGN
		{
			fprintf(yyout, "MOD_ASSIGN\t%s\n", yytext);
		}
	|	ADD_ASSIGN
		{
			fprintf(yyout, "ADD_ASSIGN\t%s\n", yytext);
		}
	|	SUB_ASSIGN
		{
			fprintf(yyout, "SUB_ASSIGN\t%s\n", yytext);
		}
	|	LEFT_ASSIGN
		{
			fprintf(yyout, "LEFT_ASSIGN\t%s\n", yytext);
		}
	|	RIGHT_ASSIGN
		{
			fprintf(yyout, "RIGHT_ASSIGN\t%s\n", yytext);
		}
	|	AND_ASSIGN
		{
			fprintf(yyout, "AND_ASSIGN\t%s\n", yytext);
		}
	|	XOR_ASSIGN
		{
			fprintf(yyout, "XOR_ASSIGN\t%s\n", yytext);
		}
	|	OR_ASSIGN
		{
			fprintf(yyout, "OR_ASSIGN\t%s\n", yytext);
		}
	;

expression
	:	assignment_expression
		{
			fprintf(yyout, "assignment_expression\t%s\n", yytext);
		}
	|	expression ',' assignment_expression
		{
			fprintf(yyout, "expression ',' assignment_expression\t%s\n", yytext);
		}
	;

constant_expression
	:	conditional_expression	/* with constraints */
		{
			fprintf(yyout, "conditional_expression\t%s\n", yytext);
		}
	;

declaration
	:	declaration_specifiers ';'
		{
			fprintf(yyout, "declaration_specifiers ';'\t%s\n", yytext);
		}
	|	declaration_specifiers init_declarator_list ';'
		{
			fprintf(yyout, "declaration_specifiers init_declarator_list ';'\t%s\n", yytext);
		}
	|	static_assert_declaration
		{
			fprintf(yyout, "static_assert_declaration\t%s\n", yytext);
		}
	;

declaration_specifiers
	:	storage_class_specifier declaration_specifiers
		{
			fprintf(yyout, "storage_class_specifier declaration_specifiers\t%s\n", yytext);
		}
	|	storage_class_specifier
		{
			fprintf(yyout, "storage_class_specifier\t%s\n", yytext);
		}
	|	type_specifier declaration_specifiers
		{
			fprintf(yyout, "type_specifier declaration_specifiers\t%s\n", yytext);
		}
	|	type_specifier
		{
			fprintf(yyout, "type_specifier\t%s\n", yytext);
		}
	|	type_qualifier declaration_specifiers
		{
			fprintf(yyout, "type_qualifier declaration_specifiers\t%s\n", yytext);
		}
	|	type_qualifier
		{
			fprintf(yyout, "type_qualifier\t%s\n", yytext);
		}
	|	function_specifier declaration_specifiers
		{
			fprintf(yyout, "function_specifier declaration_specifiers\t%s\n", yytext);
		}
	|	function_specifier
		{
			fprintf(yyout, "function_specifier\t%s\n", yytext);
		}
	|	alignment_specifier declaration_specifiers
		{
			fprintf(yyout, "alignment_specifier declaration_specifiers\t%s\n", yytext);
		}
	|	alignment_specifier
		{
			fprintf(yyout, "alignment_specifier\t%s\n", yytext);
		}
	;

init_declarator_list
	:	init_declarator
		{
			++varcount;
			fprintf(yyout, "init_declarator\t%s\n", yytext);
		}
	|	init_declarator_list ',' init_declarator
		{
			fprintf(yyout, "init_declarator_list ',' init_declarator\t%s\n", yytext);
		}
	;

init_declarator
	:	declarator '=' initializer
		{
			fprintf(yyout, "declarator '=' initializer\t%s\n", yytext);
		}
	|	declarator
		{
			fprintf(yyout, "declarator\t%s\n", yytext);
		}
	;

storage_class_specifier
	:	TYPEDEF	/* identifiers must be flagged as TYPEDEF_NAME */
		{
			fprintf(yyout, "TYPEDEF\t%s\n", yytext);
		}
	|	EXTERN
		{
			fprintf(yyout, "EXTERN\t%s\n", yytext);
		}
	|	STATIC
		{
			fprintf(yyout, "STATIC\t%s\n", yytext);
		}
	|	THREAD_LOCAL
		{
			fprintf(yyout, "THREAD_LOCAL\t%s\n", yytext);
		}
	|	AUTO
		{
			fprintf(yyout, "AUTO\t%s\n", yytext);
		}
	|	REGISTER
		{
			fprintf(yyout, "REGISTER\t%s\n", yytext);
		}
	;

type_specifier
	:	VOID
		{
			fprintf(yyout, "VOID\t%s\n", yytext);
		}
	|	CHAR
		{
			fprintf(yyout, "CHAR\t%s\n", yytext);
		}
	|	SHORT
		{
			fprintf(yyout, "SHORT\t%s\n", yytext);
		}
	|	INT
		{
			fprintf(yyout, "INT\t%s\n", yytext);
		}
	|	LONG
		{
			fprintf(yyout, "LONG\t%s\n", yytext);
		}
	|	FLOAT
		{
			fprintf(yyout, "FLOAT\t%s\n", yytext);
		}
	|	DOUBLE
		{
			fprintf(yyout, "DOUBLE\t%s\n", yytext);
		}
	|	SIGNED
		{
			fprintf(yyout, "SIGNED\t%s\n", yytext);
		}
	|	UNSIGNED
		{
			fprintf(yyout, "UNSIGNED\t%s\n", yytext);
		}
	|	BOOL
		{
			fprintf(yyout, "BOOL\t%s\n", yytext);
		}
	|	COMPLEX
		{
			fprintf(yyout, "COMPLEX\t%s\n", yytext);
		}
	|	IMAGINARY	  	/* non-mandated extension */
		{
			fprintf(yyout, "IMAGINARY\t%s\n", yytext);
		}
	|	atomic_type_specifier
		{
			fprintf(yyout, "atomic_type_specifier\t%s\n", yytext);
		}
	|	struct_or_union_specifier
		{
			fprintf(yyout, "struct_or_union_specifier\t%s\n", yytext);
		}
	|	enum_specifier
		{
			fprintf(yyout, "enum_specifier\t%s\n", yytext);
		}
	|	TYPEDEF_NAME		/* after it has been defined as such */
		{
			fprintf(yyout, "TYPEDEF_NAME\t%s\n", yytext);
		}
	;

struct_or_union_specifier
	:	struct_or_union '{' struct_declaration_list '}'
		{
			fprintf(yyout, "struct_or_union '{' struct_declaration_list '}'\t%s\n", yytext);
		}
	|	struct_or_union IDENTIFIER '{' struct_declaration_list '}'
		{
			fprintf(yyout, "struct_or_union IDENTIFIER '{' struct_declaration_list '}'\t%s\n", yytext);
		}
	|	struct_or_union IDENTIFIER
		{
			fprintf(yyout, "struct_or_union IDENTIFIER\t%s\n", yytext);
		}
	;

struct_or_union
	:	STRUCT
		{
			fprintf(yyout, "STRUCT\t%s\n", yytext);
		}
	|	UNION
		{
			fprintf(yyout, "UNION\t%s\n", yytext);
		}
	;

struct_declaration_list
	:	struct_declaration
		{
			fprintf(yyout, "struct_declaration\t%s\n", yytext);
		}
	|	struct_declaration_list struct_declaration
		{
			fprintf(yyout, "struct_declaration_list struct_declaration\t%s\n", yytext);
		}
	;

struct_declaration
	:	specifier_qualifier_list ';'	/* for anonymous struct/union */
		{
			fprintf(yyout, "specifier_qualifier_list ';'	/* for anonymous struct/union */\t%s\n", yytext);
		}
	|	specifier_qualifier_list struct_declarator_list ';'
		{
			fprintf(yyout, "specifier_qualifier_list struct_declarator_list ';'\t%s\n", yytext);
		}
	|	static_assert_declaration
		{
			fprintf(yyout, "static_assert_declaration\t%s\n", yytext);
		}
	;

specifier_qualifier_list
	:	type_specifier specifier_qualifier_list
		{
			fprintf(yyout, "type_specifier specifier_qualifier_list\t%s\n", yytext);
		}
	|	type_specifier
		{
			fprintf(yyout, "type_specifier\t%s\n", yytext);
		}
	|	type_qualifier specifier_qualifier_list
		{
			fprintf(yyout, "type_qualifier specifier_qualifier_list\t%s\n", yytext);
		}
	|	type_qualifier
		{
			fprintf(yyout, "type_qualifier\t%s\n", yytext);
		}
	;

struct_declarator_list
	:	struct_declarator
		{
			fprintf(yyout, "struct_declarator\t%s\n", yytext);
		}
	|	struct_declarator_list ',' struct_declarator
		{
			fprintf(yyout, "struct_declarator_list ',' struct_declarator\t%s\n", yytext);
		}
	;

struct_declarator
	:	':' constant_expression
		{
			fprintf(yyout, "':' constant_expression\t%s\n", yytext);
		}
	|	declarator ':' constant_expression
		{
			fprintf(yyout, "declarator ':' constant_expression\t%s\n", yytext);
		}
	|	declarator
		{
			fprintf(yyout, "declarator\t%s\n", yytext);
		}
	;

enum_specifier
	:	ENUM '{' enumerator_list '}'
		{
			fprintf(yyout, "ENUM '{' enumerator_list '}'\t%s\n", yytext);
		}
	|	ENUM '{' enumerator_list ',' '}'
		{
			fprintf(yyout, "ENUM '{' enumerator_list ',' '}'\t%s\n", yytext);
		}
	|	ENUM IDENTIFIER '{' enumerator_list '}'
		{
			fprintf(yyout, "ENUM IDENTIFIER '{' enumerator_list '}'\t%s\n", yytext);
		}
	|	ENUM IDENTIFIER '{' enumerator_list ',' '}'
		{
			fprintf(yyout, "ENUM IDENTIFIER '{' enumerator_list ',' '}'\t%s\n", yytext);
		}
	|	ENUM IDENTIFIER
		{
			fprintf(yyout, "ENUM IDENTIFIER\t%s\n", yytext);
		}
	;

enumerator_list
	:	enumerator
		{
			fprintf(yyout, "enumerator\t%s\n", yytext);
		}
	|	enumerator_list ',' enumerator
		{
			fprintf(yyout, "enumerator_list ',' enumerator\t%s\n", yytext);
		}
	;

enumerator	/* identifiers must be flagged as ENUMERATION_CONSTANT */
	:	enumeration_constant '=' constant_expression
		{
			fprintf(yyout, "enumeration_constant '=' constant_expression\t%s\n", yytext);
		}
	|	enumeration_constant
		{
			fprintf(yyout, "enumeration_constant\t%s\n", yytext);
		}
	;

atomic_type_specifier
	:	ATOMIC '(' type_name ')'
		{
			fprintf(yyout, "ATOMIC '(' type_name ')'\t%s\n", yytext);
		}
	;

type_qualifier
	:	CONST
		{
			fprintf(yyout, "CONST\t%s\n", yytext);
		}
	|	RESTRICT
		{
			fprintf(yyout, "RESTRICT\t%s\n", yytext);
		}
	|	VOLATILE
		{
			fprintf(yyout, "VOLATILE\t%s\n", yytext);
		}
	|	ATOMIC
		{
			fprintf(yyout, "ATOMIC\t%s\n", yytext);
		}
	;

function_specifier
	:	INLINE
		{
			fprintf(yyout, "INLINE\t%s\n", yytext);
		}
	|	NORETURN
		{
			fprintf(yyout, "NORETURN\t%s\n", yytext);
		}
	;

alignment_specifier
	:	ALIGNAS '(' type_name ')'
		{
			fprintf(yyout, "ALIGNAS '(' type_name ')'\t%s\n", yytext);
		}
	|	ALIGNAS '(' constant_expression ')'
		{
			fprintf(yyout, "ALIGNAS '(' constant_expression ')'\t%s\n", yytext);
		}
	;

declarator
	:	pointer direct_declarator
		{
			fprintf(yyout, "pointer direct_declarator\t%s\n", yytext);
		}
	|	direct_declarator
		{
			fprintf(yyout, "direct_declarator\t%s\n", yytext);
		}
	;

direct_declarator
	:	IDENTIFIER
		{
			fprintf(yyout, "IDENTIFIER\t%s\n", yytext);
		}
	|	'(' declarator ')'
		{
			fprintf(yyout, "'(' declarator ')'\t%s\n", yytext);
		}
	|	direct_declarator '[' ']'
		{
			fprintf(yyout, "direct_declarator '[' ']'\t%s\n", yytext);
		}
	|	direct_declarator '[' '*' ']'
		{
			fprintf(yyout, "direct_declarator '[' '*' ']'\t%s\n", yytext);
		}
	|	direct_declarator '[' STATIC type_qualifier_list assignment_expression ']'
		{
			fprintf(yyout, "direct_declarator '[' STATIC type_qualifier_list assignment_expression ']'\t%s\n", yytext);
		}
	|	direct_declarator '[' STATIC assignment_expression ']'
		{
			fprintf(yyout, "direct_declarator '[' STATIC assignment_expression ']'\t%s\n", yytext);
		}
	|	direct_declarator '[' type_qualifier_list '*' ']'
		{
			fprintf(yyout, "direct_declarator '[' type_qualifier_list '*' ']'\t%s\n", yytext);
		}
	|	direct_declarator '[' type_qualifier_list STATIC assignment_expression ']'
		{
			fprintf(yyout, "direct_declarator '[' type_qualifier_list STATIC assignment_expression ']'\t%s\n", yytext);
		}
	|	direct_declarator '[' type_qualifier_list assignment_expression ']'
		{
			fprintf(yyout, "direct_declarator '[' type_qualifier_list assignment_expression ']'\t%s\n", yytext);
		}
	|	direct_declarator '[' type_qualifier_list ']'
		{
			fprintf(yyout, "direct_declarator '[' type_qualifier_list ']'\t%s\n", yytext);
		}
	|	direct_declarator '[' assignment_expression ']'
		{
			fprintf(yyout, "direct_declarator '[' assignment_expression ']'\t%s\n", yytext);
		}
	|	direct_declarator '(' parameter_type_list ')'
		{
			fprintf(yyout, "direct_declarator '(' parameter_type_list ')'\t%s\n", yytext);
		}
	|	direct_declarator '(' ')'
		{
			fprintf(yyout, "direct_declarator '(' ')'\t%s\n", yytext);
		}
	|	direct_declarator '(' identifier_list ')'
		{
			fprintf(yyout, "direct_declarator '(' identifier_list ')'\t%s\n", yytext);
		}
	;

pointer
	:	'*' type_qualifier_list pointer
		{
			fprintf(yyout, "'*' type_qualifier_list pointer\t%s\n", yytext);
		}
	|	'*' type_qualifier_list
		{
			fprintf(yyout, "'*' type_qualifier_list\t%s\n", yytext);
		}
	|	'*' pointer
		{
			fprintf(yyout, "'*' pointer\t%s\n", yytext);
		}
	|	'*'
		{
			fprintf(yyout, "'*'\t%s\n", yytext);
		}
	;

type_qualifier_list
	:	type_qualifier
		{
			fprintf(yyout, "type_qualifier\t%s\n", yytext);
		}
	|	type_qualifier_list type_qualifier
		{
			fprintf(yyout, "type_qualifier_list type_qualifier\t%s\n", yytext);
		}
	;


parameter_type_list
	:	parameter_list ',' ELLIPSIS
		{
			fprintf(yyout, "parameter_list ',' ELLIPSIS\t%s\n", yytext);
		}
	|	parameter_list
		{
			fprintf(yyout, "parameter_list\t%s\n", yytext);
		}
	;

parameter_list
	:	parameter_declaration
		{
			fprintf(yyout, "parameter_declaration\t%s\n", yytext);
		}
	|	parameter_list ',' parameter_declaration
		{
			fprintf(yyout, "parameter_list ',' parameter_declaration\t%s\n", yytext);
		}
	;

parameter_declaration
	:	declaration_specifiers declarator
		{
			fprintf(yyout, "declaration_specifiers declarator\t%s\n", yytext);
		}
	|	declaration_specifiers abstract_declarator
		{
			fprintf(yyout, "declaration_specifiers abstract_declarator\t%s\n", yytext);
		}
	|	declaration_specifiers
		{
			fprintf(yyout, "declaration_specifiers\t%s\n", yytext);
		}
	;

identifier_list
	:	IDENTIFIER
		{
			fprintf(yyout, "IDENTIFIER\t%s\n", yytext);
		}
	|	identifier_list ',' IDENTIFIER
		{
			fprintf(yyout, "identifier_list ',' IDENTIFIER\t%s\n", yytext);
		}
	;

type_name
	:	specifier_qualifier_list abstract_declarator
		{
			fprintf(yyout, "specifier_qualifier_list abstract_declarator\t%s\n", yytext);
		}
	|	specifier_qualifier_list
		{
			fprintf(yyout, "specifier_qualifier_list\t%s\n", yytext);
		}
	;

abstract_declarator
	:	pointer direct_abstract_declarator
		{
			fprintf(yyout, "pointer direct_abstract_declarator\t%s\n", yytext);
		}
	|	pointer
		{
			fprintf(yyout, "pointer\t%s\n", yytext);
		}
	|	direct_abstract_declarator
		{
			fprintf(yyout, "direct_abstract_declarator\t%s\n", yytext);
		}
	;

direct_abstract_declarator
	:	'(' abstract_declarator ')'
		{
			fprintf(yyout, "'(' abstract_declarator ')'\t%s\n", yytext);
		}
	|	'[' ']'
		{
			fprintf(yyout, "'[' ']'\t%s\n", yytext);
		}
	|	'[' '*' ']'
		{
			fprintf(yyout, "'[' '*' ']'\t%s\n", yytext);
		}
	|	'[' STATIC type_qualifier_list assignment_expression ']'
		{
			fprintf(yyout, "'[' STATIC type_qualifier_list assignment_expression ']'\t%s\n", yytext);
		}
	|	'[' STATIC assignment_expression ']'
		{
			fprintf(yyout, "'[' STATIC assignment_expression ']'\t%s\n", yytext);
		}
	|	'[' type_qualifier_list STATIC assignment_expression ']'
		{
			fprintf(yyout, "'[' type_qualifier_list STATIC assignment_expression ']'\t%s\n", yytext);
		}
	|	'[' type_qualifier_list assignment_expression ']'
		{
			fprintf(yyout, "'[' type_qualifier_list assignment_expression ']'\t%s\n", yytext);
		}
	|	'[' type_qualifier_list ']'
		{
			fprintf(yyout, "'[' type_qualifier_list ']'\t%s\n", yytext);
		}
	|	'[' assignment_expression ']'
		{
			fprintf(yyout, "'[' assignment_expression ']'\t%s\n", yytext);
		}
	|	direct_abstract_declarator '[' ']'
		{
			fprintf(yyout, "direct_abstract_declarator '[' ']'\t%s\n", yytext);
		}
	|	direct_abstract_declarator '[' '*' ']'
		{
			fprintf(yyout, "direct_abstract_declarator '[' '*' ']'\t%s\n", yytext);
		}
	|	direct_abstract_declarator '[' STATIC type_qualifier_list assignment_expression ']'
		{
			fprintf(yyout, "direct_abstract_declarator '[' STATIC type_qualifier_list assignment_expression ']'\t%s\n", yytext);
		}
	|	direct_abstract_declarator '[' STATIC assignment_expression ']'
		{
			fprintf(yyout, "direct_abstract_declarator '[' STATIC assignment_expression ']'\t%s\n", yytext);
		}
	|	direct_abstract_declarator '[' type_qualifier_list assignment_expression ']'
		{
			fprintf(yyout, "direct_abstract_declarator '[' type_qualifier_list assignment_expression ']'\t%s\n", yytext);
		}
	|	direct_abstract_declarator '[' type_qualifier_list STATIC assignment_expression ']'
		{
			fprintf(yyout, "direct_abstract_declarator '[' type_qualifier_list STATIC assignment_expression ']'\t%s\n", yytext);
		}
	|	direct_abstract_declarator '[' type_qualifier_list ']'
		{
			fprintf(yyout, "direct_abstract_declarator '[' type_qualifier_list ']'\t%s\n", yytext);
		}
	|	direct_abstract_declarator '[' assignment_expression ']'
		{
			fprintf(yyout, "direct_abstract_declarator '[' assignment_expression ']'\t%s\n", yytext);
		}
	|	'(' ')'
		{
			fprintf(yyout, "'(' ')'\t%s\n", yytext);
		}
	|	'(' parameter_type_list ')'
		{
			fprintf(yyout, "'(' parameter_type_list ')'\t%s\n", yytext);
		}
	|	direct_abstract_declarator '(' ')'
		{
			fprintf(yyout, "direct_abstract_declarator '(' ')'\t%s\n", yytext);
		}
	|	direct_abstract_declarator '(' parameter_type_list ')'
		{
			fprintf(yyout, "direct_abstract_declarator '(' parameter_type_list ')'\t%s\n", yytext);
		}
	;

initializer
	:	'{' initializer_list '}'
		{
			fprintf(yyout, "'{' initializer_list '}'\t%s\n", yytext);
		}
	|	'{' initializer_list ',' '}'
		{
			fprintf(yyout, "'{' initializer_list ',' '}'\t%s\n", yytext);
		}
	|	assignment_expression
		{
			fprintf(yyout, "assignment_expression\t%s\n", yytext);
		}
	;

initializer_list
	:	designation initializer
		{
			fprintf(yyout, "designation initializer\t%s\n", yytext);
		}
	|	initializer
		{
			fprintf(yyout, "initializer\t%s\n", yytext);
		}
	|	initializer_list ',' designation initializer
		{
			fprintf(yyout, "initializer_list ',' designation initializer\t%s\n", yytext);
		}
	|	initializer_list ',' initializer
		{
			fprintf(yyout, "initializer_list ',' initializer\t%s\n", yytext);
		}
	;

designation
	:	designator_list '='
		{
			fprintf(yyout, "designator_list '='\t%s\n", yytext);
		}
	;

designator_list
	:	designator
		{
			fprintf(yyout, "designator\t%s\n", yytext);
		}
	|	designator_list designator
		{
			fprintf(yyout, "designator_list designator\t%s\n", yytext);
		}
	;

designator
	:	'[' constant_expression ']'
		{
			fprintf(yyout, "'[' constant_expression ']'\t%s\n", yytext);
		}
	|	'.' IDENTIFIER
		{
			fprintf(yyout, "'.' IDENTIFIER\t%s\n", yytext);
		}
	;

static_assert_declaration
	:	STATIC_ASSERT '(' constant_expression ',' STRING_LITERAL ')' ';'
		{
			fprintf(yyout, "STATIC_ASSERT '(' constant_expression ',' STRING_LITERAL ')' ';'\t%s\n", yytext);
		}
	;

statement
	:	labeled_statement
		{
			fprintf(yyout, "labeled_statement\t%s\n", yytext);
		}
	|	compound_statement
		{
			fprintf(yyout, "compound_statement\t%s\n", yytext);
		}
	|	expression_statement
		{
			fprintf(yyout, "expression_statement\t%s\n", yytext);
		}
	|	selection_statement
		{
			fprintf(yyout, "selection_statement\t%s\n", yytext);
		}
	|	iteration_statement
		{
			fprintf(yyout, "iteration_statement\t%s\n", yytext);
		}
	|	jump_statement
		{
			fprintf(yyout, "jump_statement\t%s\n", yytext);
		}
	;

labeled_statement
	:	IDENTIFIER ':' statement
		{
			fprintf(yyout, "IDENTIFIER ':' statement\t%s\n", yytext);
		}
	|	CASE constant_expression ':' statement
		{
			fprintf(yyout, "CASE constant_expression ':' statement\t%s\n", yytext);
		}
	|	DEFAULT ':' statement
		{
			fprintf(yyout, "DEFAULT ':' statement\t%s\n", yytext);
		}
	;

compound_statement
	:	'{' '}'
		{
			fprintf(yyout, "'{' '}'\t%s\n", yytext);
		}
	|	'{'  block_item_list '}'
		{
			fprintf(yyout, "'{'  block_item_list '}'\t%s\n", yytext);
		}
	;

block_item_list
	:	block_item
		{
			fprintf(yyout, "block_item\t%s\n", yytext);
		}
	|	block_item_list block_item
		{
			fprintf(yyout, "block_item_list block_item\t%s\n", yytext);
		}
	;

block_item
	:	declaration
		{
			fprintf(yyout, "declaration\t%s\n", yytext);
		}
	|	statement
		{
			fprintf(yyout, "statement\t%s\n", yytext);
		}
	;

expression_statement
	:	';'
		{
			fprintf(yyout, "';'\t%s\n", yytext);
		}
	|	expression ';'
		{
			fprintf(yyout, "expression ';'\t%s\n", yytext);
		}
	;

selection_statement
	:	IF '(' expression ')' statement ELSE statement
		{
			fprintf(yyout, "IF '(' expression ')' statement ELSE statement\t%s\n", yytext);
		}
	|	IF '(' expression ')' statement
		{
			fprintf(yyout, "IF '(' expression ')' statement\t%s\n", yytext);
		}
	|	SWITCH '(' expression ')' statement
		{
			fprintf(yyout, "SWITCH '(' expression ')' statement\t%s\n", yytext);
		}
	;

iteration_statement
	:	WHILE '(' expression ')' statement
		{
			fprintf(yyout, "WHILE '(' exp ')' st\t%s\n", yytext);
		}
	|	DO statement WHILE '(' expression ')' ';'
		{
			// @$.first_column = @1.first_column;
			// @$.first_line = @1.first_line;
			// @$.last_column = @6.last_column;
			// @$.last_line = @6.last_line;
			fprintf(yyout, "DO st WHILE '(' exp ')' ';'\t%s %d.%d-%d.%d\n", yytext, @$.first_line, @$.first_column, @$.last_line, @$.last_column);
		}
	|	FOR '(' expression_statement expression_statement ')' statement
		{
			// @$.first_column = @1.first_column;
			// @$.first_line = @1.first_line;
			// @$.last_column = @5.last_column;
			// @$.last_line = @5.last_line;
			fprintf(yyout, "FOR '(' exp_st exp_st ')' st\t%s %d.%d-%d.%d\n", yytext, @$.first_line, @$.first_column, @$.last_line, @$.last_column);
		}
	|	FOR '(' expression_statement expression_statement expression ')' statement
		{
			// @$.first_column = @1.first_column;
			// @$.first_line = @1.first_line;
			// @$.last_column = @6.last_column;
			// @$.last_line = @6.last_line;
			fprintf(yyout, "FOR '(' exp_st exp_st exp ')' st\t%s %d.%d-%d.%d\n", yytext, @1.first_line, @1.first_column, @6.last_line, @6.last_column);
		}
	|	FOR '(' declaration expression_statement ')' statement
		{
			// @$.first_column = @1.first_column;
			// @$.first_line = @1.first_line;
			// @$.last_column = @5.last_column;
			// @$.last_line = @5.last_line;
			fprintf(yyout, "FOR '(' decl exp_st ')' st\t%s\n", yytext);
		}
	|	FOR '(' declaration expression_statement expression ')' statement
		{
			fprintf(yyout, "FOR '(' decl exp_st exp ')' st\t%s\n", yytext);
		}
	;

jump_statement
	:	GOTO IDENTIFIER ';'
		{
			fprintf(yyout, "GOTO IDENTIFIER ';'\t%s\n", yytext);
		}
	|	CONTINUE ';'
		{
			fprintf(yyout, "CONTINUE ';'\t%s\n", yytext);
		}
	|	BREAK ';'
		{
			fprintf(yyout, "BREAK ';'\t%s\n", yytext);
		}
	|	RETURN ';'
		{
			fprintf(yyout, "RETURN ';'\t%s\n", yytext);
		}
	|	RETURN expression ';'
		{
			fprintf(yyout, "RETURN expression ';'\t%s\n", yytext);
		}
	;

translation_unit
	:	external_declaration
		{
			fprintf(yyout, "external_declaration\t%s\n", yytext);
		}
	|	translation_unit external_declaration
		{
			fprintf(yyout, "translation_unit external_declaration\t%s\n", yytext);
		}
	;

external_declaration
	:	function_definition
		{
			fprintf(yyout, "function_definition\t%s\n", yytext);
		}
	|	declaration
		{
			fprintf(yyout, "declaration\t%s\n", yytext);
		}
	;

function_definition
	:	declaration_specifiers declarator declaration_list compound_statement
		{
			++fncount;
			fprintf(yyout, "declaration_specifiers declarator declaration_list compound_statement\t%s\n", yytext);
		}
	|	declaration_specifiers declarator compound_statement
		{
			++fncount;
			fprintf(yyout, "declaration_specifiers declarator compound_statement\t%s\n", yytext);
		}
	;

declaration_list
	:	declaration
		{
			fprintf(yyout, "declaration\t%s\n", yytext);
		}
	|	declaration_list declaration
		{
			fprintf(yyout, "declaration_list declaration\t%s\n", yytext);
		}
	;

%%

void yyerror(const char *s) {
	fflush(stdout);
	fprintf(stderr, "%d\n%s\n", yylineno, s);
}
