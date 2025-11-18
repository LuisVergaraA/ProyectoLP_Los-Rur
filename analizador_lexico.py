import ply.lex as lex

_code_text = ""
lexical_errors = []

def set_source(text: str):
    """Guarda el código fuente para calcular columnas."""
    global _code_text
    _code_text = text

def find_column(lexpos: int) -> int:
    """Calcula la columna a partir de la posición léxica."""
    if not _code_text:
        return 1
    last_nl = _code_text.rfind('\n', 0, lexpos)
    return (lexpos - last_nl) if last_nl >= 0 else (lexpos + 1)

# SECCIÓN INTEGRANTE 1: Luis Vergara - LuisVergaraA
# Palabras reservadas
reserved_integrante1 = {
    'val'    : 'VAL',
    'var'    : 'VAR',
    'fun'    : 'FUN',
    'return' : 'RETURN',
    'if'     : 'IF',
    'else'   : 'ELSE',
}

# Tokens operadores
tokens_integrante1 = [
    # Aritméticos básicos
    'PLUS',          # +
    'MINUS',         # -
    'STAR',          # *
    'SLASH',         # /
    'PERCENT',       # %
    
    # Asignación
    'EQUAL',         # =
    'PLUSEQUAL',     # +=
    'MINUSEQUAL',    # -=
    
    # Incremento/Decremento
    'PLUSPLUS',      # ++
    'MINUSMINUS',    # --
    
    # Operadores especiales de Kotlin
    'ARROW',         # ->
    'RANGE',         # ..
]

# Reglas de tokens
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='
t_ARROW = r'->'
t_RANGE = r'\.\.'

t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_PERCENT = r'%'
t_EQUAL = r'='

# FIN SECCIÓN INTEGRANTE 1


# SECCIÓN INTEGRANTE 2: Luis Roca - LuisRoca09

reserved_integrante2 = {
    'while'  : 'WHILE',
    'for'    : 'FOR',
    'when'   : 'WHEN',
    'in'     : 'IN',
    'is'     : 'IS',
    'true'   : 'TRUE',
    'false'  : 'FALSE',
    'null'   : 'NULL',
    'println': 'PRINTLN',
}

# Tokens operadores relacionales y lógicos 
tokens_integrante2 = [
    # Relacionales
    'LT',            # 
    'GT',            # >
    'LTE',           # <=
    'GTE',           # >=
    'EQEQ',          # ==
    'NEQ',           # !=
    
    # Lógicos
    'AND',           # &&
    'OR',            # ||
    'BANG',          # !
    
    # Elvis operator
    'ELVIS',         # ?:
]

# Reglas de tokens 
t_LTE = r'<='
t_GTE = r'>='
t_EQEQ = r'=='
t_NEQ = r'!='
t_AND = r'&&'
t_OR = r'\|\|'
t_ELVIS = r'\?:'

t_LT = r'<'
t_GT = r'>'
t_BANG = r'!'




# FIN SECCIÓN INTEGRANTE 2


# SECCIÓN INTEGRANTE 3

# ===========================================
# SECCIÓN INTEGRANTE 3: Structure & Literals
# Responsable: [Johao Dorado/johaodorado]
# ===========================================

# Palabras reservadas de estructura (3)
reserved_integrante3 = {
    'class'  : 'CLASS',
    'object' : 'OBJECT',
    'this'   : 'THIS',
}

# Tokens delimitadores y literales (15)
tokens_integrante3 = [
    # Literales
    'IDENT',
    'INT',
    'DOUBLE',
    'STRING',
    'CHAR',
    
    # Delimitadores
    'LPAREN',        # (
    'RPAREN',        # )
    'LBRACE',        # {
    'RBRACE',        # }
    'LBRACKET',      # [
    'RBRACKET',      # ]
    'SEMICOLON',     # ;
    'COMMA',         # ,
    'DOT',           # .
    'COLON',         # :
]

# Delimitadores
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_COLON = r':'

# Literales (funciones para orden de prioridad)
def t_DOUBLE(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        t.value = 0.0
    return t

def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        t.value = 0
    return t

def t_CHAR(t):
    r"'([^'\\\\]|\\\\.)'"
    t.value = t.value[1:-1]  # Quitar comillas
    return t

def t_STRING(t):
    r'"([^"\\\\]|\\\\.)*"'
    t.value = t.value[1:-1]  # Quitar comillas
    return t

def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verificar si es palabra reservada
    t.type = reserved.get(t.value, 'IDENT')
    return t

# Errores léxicos específicos
def t_BAD_INT(t):
    r'\\d+[a-zA-Z_][a-zA-Z0-9_]*'
    col = find_column(t.lexpos)
    lexical_errors.append(
        f"Entero inválido '{t.value}' en línea {t.lineno}, columna {col}"
    )
    t.lexer.skip(len(t.value))

def t_UNCLOSED_STRING(t):
    r'"([^"\\n]|\\\\.)*$'
    col = find_column(t.lexpos)
    lexical_errors.append(
        f"Cadena no cerrada desde línea {t.lineno}, columna {col}"
    )
    t.lexer.skip(len(t.value))

def t_UNCLOSED_CHAR(t):
    r"'([^'\\n]|\\\\.)*$"
    col = find_column(t.lexpos)
    lexical_errors.append(
        f"Carácter no cerrado en línea {t.lineno}, columna {col}"
    )
    t.lexer.skip(len(t.value))

# FIN SECCIÓN INTEGRANTE 3
# ===========================================

# ====================================
# CONSOLIDACIÓN FINAL
# ====================================

# Juntar todas las palabras reservadas
reserved = {}
reserved.update(reserved_integrante1)
reserved.update(reserved_integrante2)
reserved.update(reserved_integrante3)

# Juntar todos los tokens
tokens = (
    tokens_integrante1 +
    tokens_integrante2 +
    tokens_integrante3 +
    list(reserved.values())
)

# ====================================
# REGLAS COMUNES
# ====================================

# Ignorar espacios y tabulaciones
t_ignore = ' \t\r'

# Comentarios de línea
def t_COMMENT_SINGLE(t):
    r'//.*'
    pass  # Ignorar comentario

# Comentarios multilínea
def t_COMMENT_MULTI(t):
    r'/\\*[\\s\\S]*?\\*/'
    # Contar saltos de línea dentro del comentario
    t.lexer.lineno += t.value.count('\\n')

# Saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores genéricos
def t_error(t):
    col = find_column(t.lexpos)
    lexical_errors.append(
        f"[Error Léxico] Línea {t.lineno}, col {col}: Carácter ilegal '{t.value[0]}'"
    )
    t.lexer.skip(1)

# ====================================
# CONSTRUCCIÓN DEL LEXER
# ====================================

lexer = lex.lex(debug=True)

# ====================================
# EXPORTACIONES
# ====================================

__all__ = ['tokens', 'lexer', 'lexical_errors', 'set_source', 'find_column', 'reserved']