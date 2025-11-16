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


# ===========================================
# SECCION INTEGRANTE 2: Control de Flujo
# Responsable: [Luis Roca/LuisRoca09]


# --- Estructura de control: while ---
def p_while_stmt(p):
    '''while_stmt : WHILE LPAREN expr RPAREN block'''
    p[0] = ('while', p[3], p[5])

# --- Estructura de control: for con rangos ---
def p_for_stmt(p):
    '''for_stmt : FOR LPAREN IDENT IN expr RPAREN block'''
    var_name = p[3]
    # El iterador se declara implícitamente
    symbol_table[var_name] = {'type': 'Int', 'mutable': False}
    p[0] = ('for', var_name, p[5], p[7])

# --- Operador de rango ---
def p_expr_range(p):
    '''expr : expr RANGE expr'''
    p[0] = ('range', p[1], p[3])

# --- Operador IN ---
def p_expr_in(p):
    '''expr : expr IN expr'''
    p[0] = ('in', p[1], p[3])

# --- Operador IS ---
def p_expr_is(p):
    '''expr : expr IS IDENT'''
    p[0] = ('is', p[1], p[3])

# --- Operador Elvis ---
def p_expr_elvis(p):
    '''expr : expr ELVIS expr'''
    p[0] = ('elvis', p[1], p[3])

# --- Estructura de control: when ---
def p_when_stmt(p):
    '''when_stmt : WHEN LPAREN expr RPAREN LBRACE when_branches RBRACE'''
    p[0] = ('when', p[3], p[6])

def p_when_branches(p):
    '''when_branches : when_branches when_branch
                     | when_branch'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_when_branch(p):
    '''when_branch : expr ARROW block
                   | ELSE ARROW block'''
    if p[1] == 'else':
        p[0] = ('when_else', p[3])
    else:
        p[0] = ('when_case', p[1], p[3])

# --- Función con parámetros y tipo de retorno ---
def p_function_def_params(p):
    '''function_def : FUN IDENT LPAREN params RPAREN COLON IDENT block'''
    name = p[2]
    params = p[4]
    ret_type = p[7]
    line = p.lineno(2)
    
    if name in function_table:
        add_sem_error(line, f"Función '{name}' ya fue declarada")
    else:
        function_table[name] = {'ret': ret_type, 'params': params}
    
    p[0] = ('fun_def_typed', name, params, ret_type, p[8])

def p_params(p):
    '''params : params COMMA param
              | param
              | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_param(p):
    '''param : IDENT COLON IDENT'''
    p[0] = ('param', p[1], p[3])

# --- Return statement ---
def p_return_stmt(p):
    '''return_stmt : RETURN expr SEMICOLON
                   | RETURN SEMICOLON'''
    if len(p) == 4:
        p[0] = ('return', p[2])
    else:
        p[0] = ('return', None)

# --- Llamada a función ---
def p_func_call_stmt(p):
    '''func_call_stmt : func_call SEMICOLON'''
    p[0] = p[1]

def p_func_call(p):
    '''func_call : IDENT LPAREN args RPAREN'''
    name = p[1]
    line = p.lineno(1)
    
    if name not in function_table and name != 'println':
        add_sem_error(line, f"Función '{name}' no declarada")
    
    p[0] = ('call', name, p[3])

def p_expr_func_call(p):
    '''expr : func_call'''
    p[0] = p[1]

def p_args(p):
    '''args : args COMMA expr
            | expr
            | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []

# --- Lambda con arrow ---
def p_expr_lambda(p):
    '''expr : LBRACE params ARROW expr RBRACE'''
    p[0] = ('lambda', p[2], p[4])

# FIN SECCIÓN INTEGRANTE 2 

#integrante 3
# ===========================================
# SECCIÓN INTEGRANTE 3: POO (Clases y Objetos)
# Responsable: [Johao Dorado/johaodorado]
# ===========================================

# --- Definición de clase ---
def p_class_def(p):
    '''class_def : CLASS IDENT LPAREN class_params RPAREN class_body'''
    name = p[2]
    params = p[4]
    body = p[6]
    line = p.lineno(2)
    
    if name in class_table:
        add_sem_error(line, f"Clase '{name}' ya fue declarada")
    else:
        class_table[name] = {'params': params, 'methods': []}
    
    p[0] = ('class', name, params, body)

def p_class_params(p):
    '''class_params : class_params COMMA class_param
                    | class_param
                    | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_class_param(p):
    '''class_param : VAL IDENT COLON IDENT
                   | VAR IDENT COLON IDENT'''
    p[0] = ('class_param', p[1], p[2], p[4])

def p_class_body(p):
    '''class_body : LBRACE class_members RBRACE
                  | empty'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

def p_class_members(p):
    '''class_members : class_members class_member
                     | class_member
                     | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]] if p[1] else [p[2]]
    elif p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_class_member(p):
    '''class_member : property
                    | method'''
    p[0] = p[1]

# --- Propiedades de clase ---
def p_property(p):
    '''property : VAL IDENT COLON IDENT EQUAL expr SEMICOLON
                | VAR IDENT COLON IDENT EQUAL expr SEMICOLON
                | VAL IDENT EQUAL expr SEMICOLON
                | VAR IDENT EQUAL expr SEMICOLON'''
    if len(p) == 8:
        p[0] = ('property', p[1], p[2], p[4], p[6])
    else:
        p[0] = ('property', p[1], p[2], None, p[4])

# --- Métodos de clase ---
def p_method(p):
    '''method : FUN IDENT LPAREN params RPAREN block
              | FUN IDENT LPAREN params RPAREN COLON IDENT block'''
    name = p[2]
    params = p[4]
    
    if len(p) == 7:
        p[0] = ('method', name, params, 'Unit', p[6])
    else:
        p[0] = ('method', name, params, p[7], p[8])

# --- Object declaration (singleton) ---
def p_class_def_object(p):
    '''class_def : OBJECT IDENT class_body'''
    name = p[2]
    body = p[3]
    line = p.lineno(2)
    
    if name in class_table:
        add_sem_error(line, f"Object '{name}' ya fue declarado")
    else:
        class_table[name] = {'type': 'object', 'members': body}
    
    p[0] = ('object', name, body)

# --- Acceso a miembros con THIS ---
def p_expr_this(p):
    '''expr : THIS DOT IDENT'''
    p[0] = ('member_access', 'this', p[3])

# --- Acceso a miembros de objetos ---
def p_expr_member_access(p):
    '''expr : expr DOT IDENT'''
    p[0] = ('member_access', p[1], p[3])

# --- Instanciación de objetos ---
def p_expr_new_object(p):
    '''expr : IDENT LPAREN args RPAREN'''
    # Puede ser llamada a función o constructor
    p[0] = ('call', p[1], p[3])


#integrante 3
# ===========================================
# SECCIÓN INTEGRANTE 3: POO (Clases y Objetos)
# Responsable: [Johao Dorado/johaodorado]
# ===========================================

# --- Definición de clase ---
def p_class_def(p):
    '''class_def : CLASS IDENT LPAREN class_params RPAREN class_body'''
    name = p[2]
    params = p[4]
    body = p[6]
    line = p.lineno(2)
    
    if name in class_table:
        add_sem_error(line, f"Clase '{name}' ya fue declarada")
    else:
        class_table[name] = {'params': params, 'methods': []}
    
    p[0] = ('class', name, params, body)

def p_class_params(p):
    '''class_params : class_params COMMA class_param
                    | class_param
                    | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_class_param(p):
    '''class_param : VAL IDENT COLON IDENT
                   | VAR IDENT COLON IDENT'''
    p[0] = ('class_param', p[1], p[2], p[4])

def p_class_body(p):
    '''class_body : LBRACE class_members RBRACE
                  | empty'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

def p_class_members(p):
    '''class_members : class_members class_member
                     | class_member
                     | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]] if p[1] else [p[2]]
    elif p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_class_member(p):
    '''class_member : property
                    | method'''
    p[0] = p[1]

# --- Propiedades de clase ---
def p_property(p):
    '''property : VAL IDENT COLON IDENT EQUAL expr SEMICOLON
                | VAR IDENT COLON IDENT EQUAL expr SEMICOLON
                | VAL IDENT EQUAL expr SEMICOLON
                | VAR IDENT EQUAL expr SEMICOLON'''
    if len(p) == 8:
        p[0] = ('property', p[1], p[2], p[4], p[6])
    else:
        p[0] = ('property', p[1], p[2], None, p[4])

# --- Métodos de clase ---
def p_method(p):
    '''method : FUN IDENT LPAREN params RPAREN block
              | FUN IDENT LPAREN params RPAREN COLON IDENT block'''
    name = p[2]
    params = p[4]
    
    if len(p) == 7:
        p[0] = ('method', name, params, 'Unit', p[6])
    else:
        p[0] = ('method', name, params, p[7], p[8])

# --- Object declaration (singleton) ---
def p_class_def_object(p):
    '''class_def : OBJECT IDENT class_body'''
    name = p[2]
    body = p[3]
    line = p.lineno(2)
    
    if name in class_table:
        add_sem_error(line, f"Object '{name}' ya fue declarado")
    else:
        class_table[name] = {'type': 'object', 'members': body}
    
    p[0] = ('object', name, body)

# --- Acceso a miembros con THIS ---
def p_expr_this(p):
    '''expr : THIS DOT IDENT'''
    p[0] = ('member_access', 'this', p[3])

# --- Acceso a miembros de objetos ---
def p_expr_member_access(p):
    '''expr : expr DOT IDENT'''
    p[0] = ('member_access', p[1], p[3])

# --- Instanciación de objetos ---
def p_expr_new_object(p):
    '''expr : IDENT LPAREN args RPAREN'''
    # Puede ser llamada a función o constructor
    p[0] = ('call', p[1], p[3])

# FIN SECCIÓN INTEGRANTE 3
# ===========================================
# =========================
# REGLAS AUXILIARES
# =========================

def p_empty(p):
    '''empty :'''
    pass

# =========================
# MANEJO DE ERRORES
# =========================

def p_error(p):
    if p:
        try:
            col = find_column(p.lexpos)
        except:
            col = '?'
        syntactic_errors.append(
            f"[Error Sintáctico] Línea {p.lineno}, col {col}: "
            f"token inesperado '{p.type}' con valor '{p.value}'"
        )
    else:
        syntactic_errors.append(
            "[Error Sintáctico] Fin de archivo inesperado"
        )

# =========================
# CONSTRUCCIÓN DEL PARSER
# =========================

parser = yacc.yacc()

# =========================
# API DE ANÁLISIS
# =========================

def analyze_syntax(code: str):
    """Analiza sintaxis y semántica de código MiniKotlin"""
    # Limpiar estados
    lexical_errors.clear()
    semantic_errors.clear()
    syntactic_errors.clear()
    symbol_table.clear()
    function_table.clear()
    class_table.clear()
    
    # Configurar fuente
    set_source(code)
    
    # Análisis léxico
    lexer.lineno = 1
    lexer.input(code)
    
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        col = find_column(tok.lexpos)
        tokens_list.append({
            'type': tok.type,
            'value': str(getattr(tok, 'value', '')),
            'line': tok.lineno,
            'col': col
        })
    
    # Análisis sintáctico
    try:
        lexer.lineno = 1
        result = parser.parse(code, lexer=lexer)
    except Exception as e:
        syntactic_errors.append(f"[Error Fatal] {str(e)}")
        result = None
    
    return {
        'tokens': tokens_list,
        'ast': result,
        'lex_errors': list(lexical_errors),
        'syn_errors': list(syntactic_errors),
        'sem_errors': list(semantic_errors),
        'symbol_table': dict(symbol_table),
        'function_table': dict(function_table),
        'class_table': dict(class_table)
    }

__all__ = [
    'parser', 'analyze_syntax',
    'syntactic_errors', 'semantic_errors',
    'symbol_table', 'function_table', 'class_table'
]