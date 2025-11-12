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


# SECCIÓN INTEGRANTE 2


# SECCIÓN INTEGRANTE 3

# CONSOLIDACIÓN (temporal)
reserved = {}
tokens = []

# Reglas comunes
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    col = find_column(t.lexpos)
    lexical_errors.append(
        f"[Error Léxico] Línea {t.lineno}, col {col}: '{t.value[0]}'"
    )
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

__all__ = ['tokens', 'lexer', 'lexical_errors', 'set_source']
