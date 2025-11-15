import ply.yacc as yacc
from analizador_lexico import tokens, lexer, lexical_errors, set_source, find_column

# ESTADO / ESTRUCTURAS
symbol_table = {}  # nombre -> {'type': tipo, 'mutable': bool}
function_table = {}  # nombre -> {'ret': tipo_retorno}
class_table = {}  # nombre -> {'properties': [], 'methods': []}

semantic_errors = []
syntactic_errors = []

# UTILIDADES
def add_sem_error(line, msg):
    """Agregar error semántico"""
    semantic_errors.append(f"[Error Semántico] Línea {line}: {msg}")

# PRECEDENCIA DE OPERADORES
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQEQ', 'NEQ'),
    ('left', 'LT', 'LTE', 'GT', 'GTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'SLASH', 'PERCENT'),
    ('right', 'BANG', 'UMINUS'),
)

# GRAMÁTICA

def p_program(p):
    '''program : stmts'''
    p[0] = ('program', p[1])

def p_stmts(p):
    '''stmts : stmts stmt
             | stmt'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_stmt(p):
    '''stmt : decl
            | assign
            | print
            | if_stmt
            | while_stmt
            | for_stmt
            | when_stmt
            | func_call_stmt
            | return_stmt
            | function_def
            | class_def
            | SEMICOLON'''
    p[0] = p[1]

# SECCIÓN INTEGRANTE 1: Expresiones y Básicos
# Responsable: Luis Vergara - LuisVergaraA

# Declaraciones de variables
def p_decl_init(p):
    '''decl : VAL IDENT EQUAL expr SEMICOLON
            | VAR IDENT EQUAL expr SEMICOLON'''
    mutable = (p[1] == 'var')
    name = p[2]
    line = p.lineno(2)
    
    if name in symbol_table:
        add_sem_error(line, f"Variable '{name}' ya fue declarada")
    else:
        symbol_table[name] = {'type': 'Unknown', 'mutable': mutable}
    
    p[0] = ('decl', p[1], name, p[4])

def p_decl_no_init(p):
    '''decl : VAL IDENT SEMICOLON
            | VAR IDENT SEMICOLON'''
    mutable = (p[1] == 'var')
    name = p[2]
    line = p.lineno(2)
    
    if not mutable:
        add_sem_error(line, f"'val {name}' debe ser inicializada")
    
    if name not in symbol_table:
        symbol_table[name] = {'type': 'Unknown', 'mutable': mutable}
    
    p[0] = ('decl_no_init', p[1], name)

# Asignación
def p_assign(p):
    '''assign : IDENT EQUAL expr SEMICOLON'''
    name = p[1]
    line = p.lineno(1)
    
    if name not in symbol_table:
        add_sem_error(line, f"Variable '{name}' no declarada")
    elif not symbol_table[name]['mutable']:
        add_sem_error(line, f"'{name}' es inmutable (val)")
    
    p[0] = ('assign', name, p[3])

# Impresión
def p_print(p):
    '''print : PRINTLN LPAREN expr RPAREN SEMICOLON'''
    p[0] = ('println', p[3])

# Estructura de control: if-else
def p_if_stmt(p):
    '''if_stmt : IF LPAREN expr RPAREN block
               | IF LPAREN expr RPAREN block ELSE block
               | IF LPAREN expr RPAREN block ELSE if_stmt'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if_else', p[3], p[5], p[7])

def p_block(p):
    '''block : LBRACE stmts RBRACE'''
    p[0] = ('block', p[2])

# Estructura de datos: Lista literal
def p_expr_list_lit(p):
    '''expr : LBRACKET list_elems_opt RBRACKET'''
    p[0] = ('list', p[2])

def p_list_elems_opt(p):
    '''list_elems_opt : list_elems
                      | empty'''
    p[0] = p[1] if p[1] else []

def p_list_elems(p):
    '''list_elems : expr
                  | list_elems COMMA expr'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# Función básica
def p_function_def_simple(p):
    '''function_def : FUN IDENT LPAREN RPAREN block'''
    name = p[2]
    line = p.lineno(2)
    
    if name in function_table:
        add_sem_error(line, f"Función '{name}' ya fue declarada")
    else:
        function_table[name] = {'ret': 'Unit', 'params': []}
    
    p[0] = ('fun_def', name, [], p[5])

# Expresiones aritméticas
def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr STAR expr
            | expr SLASH expr
            | expr PERCENT expr'''
    p[0] = ('binop', p[2], p[1], p[3])

# Expresiones lógicas
def p_expr_logical(p):
    '''expr : expr AND expr
            | expr OR expr'''
    p[0] = ('logical', p[2], p[1], p[3])

# Expresiones relacionales
def p_expr_relational(p):
    '''expr : expr LT expr
            | expr LTE expr
            | expr GT expr
            | expr GTE expr
            | expr EQEQ expr
            | expr NEQ expr'''
    p[0] = ('relational', p[2], p[1], p[3])

# Expresión unaria
def p_expr_unary_not(p):
    '''expr : BANG expr'''
    p[0] = ('unary', '!', p[2])

def p_expr_unary_minus(p):
    '''expr : MINUS expr %prec UMINUS'''
    p[0] = ('unary', '-', p[2])

# Expresión entre paréntesis
def p_expr_group(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

# Literales
def p_expr_literals(p):
    '''expr : INT
            | DOUBLE
            | STRING
            | CHAR
            | TRUE
            | FALSE
            | NULL'''
    p[0] = ('literal', p[1])

def p_expr_ident(p):
    '''expr : IDENT'''
    name = p[1]
    line = p.lineno(1)
    
    if name not in symbol_table:
        add_sem_error(line, f"Variable '{name}' no declarada")
    
    p[0] = ('ident', name)

# FIN SECCIÓN INTEGRANTE 1

#integrante 2
#integrante 3