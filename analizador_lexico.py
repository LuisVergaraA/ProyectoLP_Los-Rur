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
