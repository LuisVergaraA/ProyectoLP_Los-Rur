import os
from datetime import datetime
from analizador_lexico import lexer, lexical_errors, set_source, find_column

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALGO_DIR = os.path.join(BASE_DIR, "algoritmos_kotlin")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Crear carpeta de logs si no existe
os.makedirs(LOGS_DIR, exist_ok=True)

def extraer_usuario_de_archivo(filename):
    """
    Extrae el nombre de usuario del archivo.
    Formato esperado: algoritmo_usuario.kt
    Ejemplo: algoritmo_juan.kt -> juan
    """
    base = os.path.splitext(os.path.basename(filename))[0]
    parts = base.split('_')
    return parts[1] if len(parts) >= 2 else "usuario"

def generar_nombre_log(usuario):
    """
    Genera nombre de log con formato: lexico-usuario-ddmmyyyy-HHhMM.txt
    Ejemplo: lexico-juan-12112025-14h30.txt
    """
    now = datetime.now()
    fecha = now.strftime('%d%m%Y')
    hora = now.strftime('%Hh%M')
    return f"lexico-{usuario}-{fecha}-{hora}.txt"

def guardar_log(usuario, tokens_list, errores):
    """
    Guarda el log de análisis con tokens y errores.
    Retorna la ruta del archivo creado.
    """
    nombre_log = generar_nombre_log(usuario)
    ruta_log = os.path.join(LOGS_DIR, nombre_log)
    
    with open(ruta_log, 'w', encoding='utf-8') as f:
        # Encabezado
        f.write("=" * 70 + "\n")
        f.write(f"ANALIZADOR LÉXICO - MINIKOTLIN MEJORADO\n")
        f.write(f"Usuario: {usuario}\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        
        # Tokens reconocidos
        if tokens_list:
            f.write("=== TOKENS RECONOCIDOS ===\n\n")
            for tok in tokens_list:
                f.write(
                    f"{tok['type']:15} ({tok['value']}) "
                    f"-> línea {tok['line']}, col {tok['col']}\n"
                )
            f.write(f"\nTotal de tokens: {len(tokens_list)}\n")
        else:
            f.write("=== TOKENS RECONOCIDOS ===\n\n")
            f.write("(No se encontraron tokens)\n")
        
        # Errores léxicos
        f.write("\n" + "=" * 70 + "\n")
        if errores:
            f.write("=== ERRORES LÉXICOS ===\n\n")
            for err in errores:
                f.write(f"{err}\n")
            f.write(f"\nTotal de errores: {len(errores)}\n")
        else:
            f.write("=== ERRORES LÉXICOS ===\n\n")
            f.write("✅ No se encontraron errores léxicos\n")
        
        # Resumen final
        f.write("\n" + "=" * 70 + "\n")
        f.write("=== RESUMEN ===\n\n")
        f.write(f"Tokens reconocidos: {len(tokens_list)}\n")
        f.write(f"Errores encontrados: {len(errores)}\n")
        
        if errores:
            f.write(f"\n❌ Análisis completado CON ERRORES\n")
        else:
            f.write(f"\n✅ Análisis completado EXITOSAMENTE\n")
    
    return ruta_log

def analizar_archivo(ruta_archivo):
    """
    Analiza un archivo .kt y genera su log correspondiente.
    """
    # Extraer información del archivo
    usuario = extraer_usuario_de_archivo(ruta_archivo)
    nombre_archivo = os.path.basename(ruta_archivo)
    
    print(f"\n{'='*70}")
    print(f"📄 Analizando: {nombre_archivo}")
    print(f"👤 Usuario: {usuario}")
    print(f"{'='*70}")
    
    # Leer el código fuente
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return
    
    # Limpiar errores previos
    lexical_errors.clear()
    set_source(codigo)
    
    # Reiniciar el lexer
    lexer.lineno = 1
    lexer.input(codigo)
    
    # Tokenizar
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
    
    # Mostrar estadísticas en consola
    print(f"\n📊 Estadísticas:")
    print(f"   • Tokens reconocidos: {len(tokens_list)}")
    print(f"   • Errores encontrados: {len(lexical_errors)}")
    
    # Guardar log
    ruta_log = guardar_log(usuario, tokens_list, list(lexical_errors))
    print(f"\n✅ Log generado: {os.path.basename(ruta_log)}")
    
    # Mostrar primeros tokens
    if tokens_list:
        print(f"\n🔍 Primeros 5 tokens:")
        for tok in tokens_list[:5]:
            print(f"   {tok['type']:15} -> {tok['value']}")
        if len(tokens_list) > 5:
            print(f"   ... y {len(tokens_list) - 5} más")
    
    # Mostrar errores
    if lexical_errors:
        print(f"\n⚠️  Errores encontrados:")
        for err in lexical_errors[:3]:
            print(f"   • {err}")
        if len(lexical_errors) > 3:
            print(f"   ... y {len(lexical_errors) - 3} más")

def listar_archivos_kotlin():
    """
    Lista todos los archivos .kt en la carpeta algoritmos_kotlin/
    """
    if not os.path.isdir(ALGO_DIR):
        return []
    
    archivos = [
        os.path.join(ALGO_DIR, f) 
        for f in os.listdir(ALGO_DIR) 
        if f.endswith('.kt')
    ]
    return sorted(archivos)

# ====================================
# FUNCIÓN PRINCIPAL
# ====================================

def main():
    """
    Busca y analiza todos los archivos .kt en algoritmos_kotlin/
    """
    print("\n" + "="*70)
    print("🚀 ANALIZADOR LÉXICO - MINIKOTLIN MEJORADO")
    print("="*70)
    
    # Buscar archivos
    archivos = listar_archivos_kotlin()
    
    if not archivos:
        print("\n❌ No se encontraron archivos .kt en la carpeta 'algoritmos_kotlin/'")
        print(f"   Ruta buscada: {ALGO_DIR}")
        return
    
    print(f"\n🔍 Encontrados {len(archivos)} archivo(s) para analizar:")
    for i, archivo in enumerate(archivos, 1):
        print(f"   {i}. {os.path.basename(archivo)}")
    
    # Analizar cada archivo
    for archivo in archivos:
        analizar_archivo(archivo)
    
    # Resumen final
    print("\n" + "="*70)
    print("✅ ANÁLISIS COMPLETADO")
    print(f"📁 Logs guardados en: {LOGS_DIR}")
    print("="*70 + "\n")
    

if __name__ == "__main__":
    main()