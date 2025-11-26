import ply.yacc as yacc
from analizador_lexico import tokens, lexer, lexical_errors, set_source, find_column

# ESTADO / ESTRUCTURAS

# Tabla de símbolos: nombre -> {'type': tipo, 'mutable': bool, 'initialized': bool}
symbol_table = {}

# Tabla de funciones: nombre -> {'ret': tipo_retorno, 'params': [...], 'returns': [tipos]}
function_table = {}

# Tabla de clases: nombre -> {'properties': {...}, 'methods': {...}}
class_table = {}

# Contexto actual (para saber si estamos dentro de una función/clase)
current_function = None
current_class = None

# Errores
semantic_errors = []
syntactic_errors = []

# UTILIDADES

def add_sem_error(line, msg):
    """Agregar error semántico"""
    semantic_errors.append(f"[Error Semántico] Línea {line}: {msg}")

def numeric(t):
    """Verificar si un tipo es numérico"""
    return t in ('Int', 'Double')

def promote_type(t1, t2):
    """Promoción de tipos en operaciones"""
    if t1 == t2:
        return t1
    if {'Int', 'Double'} == {t1, t2}:
        return 'Double'
    return 'Unknown'

# PRECEDENCIA

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQEQ', 'NEQ'),
    ('left', 'LT', 'LTE', 'GT', 'GTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'SLASH', 'PERCENT'),
    ('right', 'BANG', 'UMINUS'),
)

# GRAMÁTICA PRINCIPAL

def p_program(p):
    '''program : stmts'''
    p[0] = ('program', p[1])

def p_stmts(p):
    '''stmts : stmts stmt
             | stmt'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]] if isinstance(p[1], list) else [p[1], p[2]]
    else:
        p[0] = [p[1]]

def p_stmt(p):
    '''stmt : decl
            | assign
            | print
            | input_stmt
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

# SECCIÓN INTEGRANTE 1: Luis Vergara - LuisVergaraA
# Responsable de: Variables, Asignación, Expresiones, If-Else

# --- DECLARACIONES DE VARIABLES ---
def p_decl_init(p):
    '''decl : VAL IDENT EQUAL expr SEMICOLON
            | VAR IDENT EQUAL expr SEMICOLON'''
    mutable = (p[1] == 'var')
    name = p[2]
    line = p.lineno(2)
    expr_type = p[4]
    
    # REGLA SEMÁNTICA 1: No permitir redeclaración
    if name in symbol_table:
        add_sem_error(line, f"Variable '{name}' ya fue declarada")
    else:
        # Inferir tipo de la expresión
        if expr_type == 'Unknown':
            add_sem_error(line, f"No se puede inferir tipo para '{name}'")
        
        symbol_table[name] = {
            'type': expr_type,
            'mutable': mutable,
            'initialized': True,
            'line': line
        }
    
    p[0] = ('decl', p[1], name, expr_type)

def p_decl_no_init(p):
    '''decl : VAL IDENT SEMICOLON
            | VAR IDENT SEMICOLON'''
    mutable = (p[1] == 'var')
    name = p[2]
    line = p.lineno(2)
    
    # REGLA SEMÁNTICA 1: val debe inicializarse
    if not mutable:
        add_sem_error(line, f"'val {name}' debe ser inicializada al declararse")
    
    if name in symbol_table:
        add_sem_error(line, f"Variable '{name}' ya fue declarada")
    else:
        symbol_table[name] = {
            'type': 'Unknown',
            'mutable': mutable,
            'initialized': False,
            'line': line
        }
    
    p[0] = ('decl_no_init', p[1], name)

# --- ASIGNACIÓN ---
def p_assign(p):
    '''assign : IDENT EQUAL expr SEMICOLON'''
    name = p[1]
    line = p.lineno(1)
    expr_type = p[3]
    
    # REGLA SEMÁNTICA 1: Variable debe estar declarada
    if name not in symbol_table:
        add_sem_error(line, f"Variable '{name}' no declarada")
        p[0] = ('assign', name, expr_type)
        return
    
    sym = symbol_table[name]
    
    # REGLA SEMÁNTICA 2: Verificar inmutabilidad (VAL)
    if not sym['mutable']:
        add_sem_error(line, f"'{name}' es inmutable (val); reasignación no permitida")
    
    # Verificar compatibilidad de tipos
    if sym['type'] == 'Unknown':
        symbol_table[name]['type'] = expr_type
        symbol_table[name]['initialized'] = True
    elif sym['type'] != expr_type and expr_type != 'Unknown':
        add_sem_error(line, f"Tipo incompatible en asignación a '{name}': esperado {sym['type']}, recibido {expr_type}")
    
    p[0] = ('assign', name, expr_type)

# --- EXPRESIÓN: IDENTIFICADOR ---
def p_expr_ident(p):
    '''expr : IDENT'''
    name = p[1]
    line = p.lineno(1)
    
    # REGLA SEMÁNTICA 1: Verificar que la variable esté declarada
    if name not in symbol_table:
        add_sem_error(line, f"Variable '{name}' no declarada")
        p[0] = 'Unknown'
        return
    
    sym = symbol_table[name]
    
    # REGLA SEMÁNTICA 1: Verificar que esté inicializada
    if not sym['initialized']:
        add_sem_error(line, f"Variable '{name}' usada antes de inicializar")
    
    p[0] = sym['type']

# --- ESTRUCTURAS IF-ELSE ---
def p_if_stmt(p):
    '''if_stmt : IF LPAREN expr RPAREN block
               | IF LPAREN expr RPAREN block ELSE block
               | IF LPAREN expr RPAREN block ELSE if_stmt'''
    cond_type = p[3]
    line = p.lineno(1)
    
    if cond_type != 'Boolean' and cond_type != 'Unknown':
        add_sem_error(line, "Condición de 'if' debe ser Boolean")
    
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if_else', p[3], p[5], p[7])

# --- EXPRESIONES ARITMÉTICAS ---
def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr STAR expr
            | expr SLASH expr
            | expr PERCENT expr'''
    left = p[1]
    right = p[3]
    line = p.lineno(2)
    
    if not numeric(left) and left != 'Unknown':
        add_sem_error(line, f"Operando izquierdo debe ser numérico, recibió {left}")
    if not numeric(right) and right != 'Unknown':
        add_sem_error(line, f"Operando derecho debe ser numérico, recibió {right}")
    
    p[0] = promote_type(left, right)

# --- ASIGNACIÓN COMPUESTA (+=, -=) ---
def p_assign_compound(p):
    '''assign : IDENT PLUSEQUAL expr SEMICOLON
              | IDENT MINUSEQUAL expr SEMICOLON'''
    name = p[1]
    line = p.lineno(1)
    expr_type = p[3]
    
    if name not in symbol_table:
        add_sem_error(line, f"Variable '{name}' no declarada")
    else:
        sym = symbol_table[name]
        if not sym['mutable']:
            add_sem_error(line, f"'{name}' es inmutable (val)")
        if not numeric(sym['type']) and sym['type'] != 'Unknown':
            add_sem_error(line, f"Operador compuesto requiere tipo numérico")
    
    p[0] = ('assign_compound', name, p[2], expr_type)

# --- INCREMENTO/DECREMENTO (++, --) ---
def p_expr_postfix(p):
    '''expr : IDENT PLUSPLUS
            | IDENT MINUSMINUS'''
    name = p[1]
    line = p.lineno(1)
    
    if name not in symbol_table:
        add_sem_error(line, f"Variable '{name}' no declarada")
    else:
        sym = symbol_table[name]
        if not sym['mutable']:
            add_sem_error(line, f"'{name}' es inmutable (val)")
        if not numeric(sym['type']) and sym['type'] != 'Unknown':
            add_sem_error(line, f"Operador {p[2]} requiere tipo numérico")
        p[0] = sym['type']
        return
    
    p[0] = 'Unknown'

# FIN SECCIÓN INTEGRANTE 1
# =====================================================


# SECCION INTEGRANTE 2: Luis Roca - LuisRoca09
# Responsable de: Funciones, While, For, When, Operadores

# --- DEFINICIÓN DE FUNCIÓN SIMPLE ---
def p_function_def_simple(p):
    '''function_def : FUN IDENT LPAREN RPAREN block'''
    global current_function
    name = p[2]
    line = p.lineno(2)
    
    # REGLA SEMÁNTICA 3: No permitir funciones duplicadas
    if name in function_table:
        add_sem_error(line, f"Función '{name}' ya fue declarada")
    else:
        function_table[name] = {
            'ret': 'Unit',
            'params': [],
            'returns': [],
            'line': line
        }
    
    current_function = None
    p[0] = ('fun_def', name, [], 'Unit', p[5])

# --- DEFINICIÓN DE FUNCIÓN CON PARÁMETROS ---
def p_function_def_params(p):
    '''function_def : FUN IDENT LPAREN params RPAREN COLON IDENT block'''
    global current_function
    name = p[2]
    params = p[4]
    ret_type = p[7]
    line = p.lineno(2)
    
    # REGLA SEMÁNTICA 3: No permitir funciones duplicadas
    if name in function_table:
        add_sem_error(line, f"Función '{name}' ya fue declarada")
    else:
        function_table[name] = {
            'ret': ret_type,
            'params': params,
            'returns': [],
            'line': line
        }
    
    current_function = None
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
    param_name = p[1]
    param_type = p[3]
    p[0] = {'name': param_name, 'type': param_type}

# --- RETURN STATEMENT ---
def p_return_stmt(p):
    '''return_stmt : RETURN expr SEMICOLON
                   | RETURN SEMICOLON'''
    global current_function
    line = p.lineno(1)
    
    if len(p) == 4:
        return_type = p[2]
    else:
        return_type = 'Unit'
    
    # REGLA SEMÁNTICA 4: Verificar que estamos dentro de una función
    if current_function is None:
        add_sem_error(line, "Return usado fuera de una función")
    else:
        if current_function in function_table:
            expected_type = function_table[current_function]['ret']
            
            if return_type != expected_type and return_type != 'Unknown':
                if expected_type == 'Unit' and return_type != 'Unit':
                    add_sem_error(line, f"Función '{current_function}' no debe retornar valor (tipo Unit)")
                elif expected_type != 'Unit' and return_type == 'Unit':
                    add_sem_error(line, f"Función '{current_function}' debe retornar {expected_type}")
                else:
                    add_sem_error(line, f"Tipo de retorno inconsistente: esperado {expected_type}, recibido {return_type}")
    
    p[0] = ('return', return_type if len(p) == 4 else None)

# --- LLAMADA A FUNCIÓN ---
def p_func_call_stmt(p):
    '''func_call_stmt : func_call SEMICOLON'''
    p[0] = p[1]

def p_func_call(p):
    '''func_call : IDENT LPAREN args RPAREN'''
    name = p[1]
    args = p[3]
    line = p.lineno(1)
    
    # REGLA SEMÁNTICA 3: Verificar que la función esté declarada
    if name not in function_table and name != 'println' and name != 'readln':
        add_sem_error(line, f"Función '{name}' no está declarada")
    
    # Verificar número de argumentos
    if name in function_table:
        expected_params = len(function_table[name]['params'])
        actual_args = len(args) if args else 0
        if expected_params != actual_args:
            add_sem_error(line, f"Función '{name}' espera {expected_params} argumentos, recibió {actual_args}")
    
    p[0] = ('call', name, args)

def p_expr_func_call(p):
    '''expr : func_call'''
    func_name = p[1][1]
    if func_name in function_table:
        p[0] = function_table[func_name]['ret']
    elif func_name == 'readln':
        p[0] = 'String'
    else:
        p[0] = 'Unknown'

def p_args(p):
    '''args : args COMMA expr
            | expr
            | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]] if p[1] else [p[3]]
    elif p[1]:
        p[0] = [p[1]]
    else:
        p[0] = []

# --- OPERADORES RELACIONALES ---
def p_expr_relational(p):
    '''expr : expr LT expr
            | expr GT expr
            | expr LTE expr
            | expr GTE expr
            | expr EQEQ expr
            | expr NEQ expr'''
    left = p[1]
    right = p[3]
    line = p.lineno(2)
    
    if left != right and left != 'Unknown' and right != 'Unknown':
        add_sem_error(line, f"Comparación entre tipos incompatibles: {left} y {right}")
    
    p[0] = 'Boolean'

# --- OPERADORES LÓGICOS ---
def p_expr_logical(p):
    '''expr : expr AND expr
            | expr OR expr'''
    left = p[1]
    right = p[3]
    line = p.lineno(2)
    
    if left != 'Boolean' and left != 'Unknown':
        add_sem_error(line, f"Operador lógico requiere Boolean, recibió {left}")
    if right != 'Boolean' and right != 'Unknown':
        add_sem_error(line, f"Operador lógico requiere Boolean, recibió {right}")
    
    p[0] = 'Boolean'

# --- WHILE ---
def p_while_stmt(p):
    '''while_stmt : WHILE LPAREN expr RPAREN block'''
    cond_type = p[3]
    line = p.lineno(1)
    
    if cond_type != 'Boolean' and cond_type != 'Unknown':
        add_sem_error(line, "Condición de 'while' debe ser Boolean")
    
    p[0] = ('while', p[3], p[5])

# --- FOR ---
def p_for_stmt(p):
    '''for_stmt : FOR LPAREN IDENT IN expr RPAREN block'''
    var_name = p[3]
    symbol_table[var_name] = {
        'type': 'Int',
        'mutable': False,
        'initialized': True,
        'line': p.lineno(3)
    }
    p[0] = ('for', var_name, p[5], p[7])

# --- WHEN ---
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

# --- OPERADORES ESPECIALES ---
def p_expr_range(p):
    '''expr : expr RANGE expr'''
    p[0] = 'Range'

def p_expr_in(p):
    '''expr : expr IN expr'''
    p[0] = 'Boolean'

def p_expr_is(p):
    '''expr : expr IS IDENT'''
    p[0] = 'Boolean'

def p_expr_elvis(p):
    '''expr : expr ELVIS expr'''
    left_type = p[1]
    right_type = p[3]
    p[0] = right_type if left_type == 'Unknown' else left_type

# --- LAMBDA ---
def p_expr_lambda(p):
    '''expr : LBRACE params ARROW expr RBRACE'''
    p[0] = 'Function'

# FIN SECCIÓN INTEGRANTE 2
# =====================================================


# SECCIÓN INTEGRANTE 3: Johao Dorado - johaodorado
# Responsable de: Clases, Objetos, Listas, Propiedades

# --- DEFINICIÓN DE CLASE ---
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

# --- PROPIEDADES DE CLASE ---
def p_property(p):
    '''property : VAL IDENT COLON IDENT EQUAL expr SEMICOLON
                | VAR IDENT COLON IDENT EQUAL expr SEMICOLON
                | VAL IDENT EQUAL expr SEMICOLON
                | VAR IDENT EQUAL expr SEMICOLON'''
    if len(p) == 8:
        p[0] = ('property', p[1], p[2], p[4], p[6])
    else:
        p[0] = ('property', p[1], p[2], None, p[4])

# --- MÉTODOS DE CLASE ---
def p_method(p):
    '''method : FUN IDENT LPAREN params RPAREN block
              | FUN IDENT LPAREN params RPAREN COLON IDENT block'''
    name = p[2]
    params = p[4]
    
    if len(p) == 7:
        p[0] = ('method', name, params, 'Unit', p[6])
    else:
        p[0] = ('method', name, params, p[7], p[8])

# --- OBJECT DECLARATION (SINGLETON) ---
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

# --- ACCESO A MIEMBROS CON THIS ---
def p_expr_this(p):
    '''expr : THIS DOT IDENT'''
    p[0] = ('member_access', 'this', p[3])

# --- ACCESO A MIEMBROS DE OBJETOS ---
def p_expr_member_access(p):
    '''expr : expr DOT IDENT'''
    p[0] = ('member_access', p[1], p[3])

# --- INSTANCIACIÓN DE OBJETOS ---
def p_expr_new_object(p):
    '''expr : IDENT LPAREN args RPAREN'''
    p[0] = ('call', p[1], p[3])

# --- LISTAS (ESTRUCTURA DE DATOS) ---
def p_expr_list_lit(p):
    '''expr : LBRACKET list_elems_opt RBRACKET'''
    p[0] = 'List'

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

# FIN SECCIÓN INTEGRANTE 3
# =====================================================


# REGLAS COMUNES

# --- BLOQUES ---
def p_block(p):
    '''block : LBRACE stmts RBRACE'''
    p[0] = ('block', p[2])

# --- IMPRESIÓN (println) ---
def p_print(p):
    '''print : PRINTLN LPAREN expr RPAREN SEMICOLON'''
    p[0] = ('println', p[3])

# --- INGRESO DE DATOS (readln) - NUEVO ---
def p_input_stmt(p):
    '''input_stmt : IDENT EQUAL func_call SEMICOLON'''
    # Para manejar: val x = readln()
    if p[3][1] == 'readln':  # ('call', 'readln', args)
        name = p[1]
        line = p.lineno(1)
        
        if name in symbol_table:
            sym = symbol_table[name]
            if not sym['mutable']:
                add_sem_error(line, f"'{name}' es inmutable (val)")
            symbol_table[name]['type'] = 'String'
            symbol_table[name]['initialized'] = True
        else:
            add_sem_error(line, f"Variable '{name}' no declarada")
        
        p[0] = ('input', name, 'readln')
    else:
        # Es una llamada de función normal
        p[0] = ('assign_call', p[1], p[3])

# --- EXPRESIONES UNARIAS ---
def p_expr_unary_not(p):
    '''expr : BANG expr'''
    expr_type = p[2]
    line = p.lineno(1)
    
    if expr_type != 'Boolean' and expr_type != 'Unknown':
        add_sem_error(line, f"Operador '!' requiere Boolean; recibió {expr_type}")
    
    p[0] = 'Boolean'

def p_expr_unary_minus(p):
    '''expr : MINUS expr %prec UMINUS'''
    expr_type = p[2]
    line = p.lineno(1)
    
    if not numeric(expr_type) and expr_type != 'Unknown':
        add_sem_error(line, f"Operador unario '-' requiere tipo numérico; recibió {expr_type}")
    
    p[0] = expr_type

# --- PARÉNTESIS ---
def p_expr_group(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

# --- LITERALES ---
def p_expr_int(p):
    '''expr : INT'''
    p[0] = 'Int'

def p_expr_double(p):
    '''expr : DOUBLE'''
    p[0] = 'Double'

def p_expr_bool(p):
    '''expr : TRUE
            | FALSE'''
    p[0] = 'Boolean'

def p_expr_string(p):
    '''expr : STRING'''
    p[0] = 'String'

def p_expr_char(p):
    '''expr : CHAR'''
    p[0] = 'Char'

def p_expr_null(p):
    '''expr : NULL'''
    p[0] = 'Null'

# --- VACÍO ---
def p_empty(p):
    '''empty :'''
    pass

# MANEJO DE ERRORES

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

# CONSTRUCCIÓN DEL PARSER

parser = yacc.yacc()

# API DE ANÁLISIS

def analyze_syntax(code: str):
    """Analiza sintaxis y semántica de código MiniKotlin"""
    # Limpiar estados
    global current_function, current_class
    
    lexical_errors.clear()
    semantic_errors.clear()
    syntactic_errors.clear()
    symbol_table.clear()
    function_table.clear()
    class_table.clear()
    
    current_function = None
    current_class = None
    
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
    
    # Análisis sintáctico y semántico
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

__all__ = ['parser', 'analyze_syntax','syntactic_errors', 'semantic_errors','symbol_table', 'function_table', 'class_table']