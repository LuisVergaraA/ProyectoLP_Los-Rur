import os
from datetime import datetime
from analizador_sintactico import analyze_syntax

# CONFIGURACIÓN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALGO_DIR = os.path.join(BASE_DIR, "algoritmos_kotlin")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOGS_DIR, exist_ok=True)

# FUNCIONES AUXILIARES

def extraer_usuario_de_archivo(filename):
    """Extrae usuario del nombre: algoritmo_usuario.kt"""
    base = os.path.splitext(os.path.basename(filename))[0]
    parts = base.split('_')
    return parts[1] if len(parts) >= 2 else "usuario"

def generar_nombre_log(usuario):
    """Formato: sintactico-usuario-ddmmyyyy-HHhMM.txt"""
    now = datetime.now()
    fecha = now.strftime('%d%m%Y')
    hora = now.strftime('%Hh%M')
    return f"sintactico-{usuario}-{fecha}-{hora}.txt"

def guardar_log(usuario, resultado):
    """Guarda log de análisis sintáctico"""
    nombre_log = generar_nombre_log(usuario)
    ruta_log = os.path.join(LOGS_DIR, nombre_log)
    
    with open(ruta_log, 'w', encoding='utf-8') as f:
        # Encabezado
        f.write("=" * 70 + "\n")
        f.write("ANALIZADOR SINTÁCTICO - MINIKOTLIN MEJORADO\n")
        f.write(f"Usuario: {usuario}\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        
        # Errores Léxicos
        if resultado['lex_errors']:
            f.write("=== ERRORES LÉXICOS ===\n\n")
            for err in resultado['lex_errors']:
                f.write(f"{err}\n")
            f.write(f"\nTotal: {len(resultado['lex_errors'])}\n\n")
        
        # Errores Sintácticos
        f.write("=" * 70 + "\n")
        if resultado['syn_errors']:
            f.write("=== ERRORES SINTÁCTICOS ===\n\n")
            for err in resultado['syn_errors']:
                f.write(f"{err}\n")
            f.write(f"\nTotal: {len(resultado['syn_errors'])}\n\n")
        else:
            f.write("=== ERRORES SINTÁCTICOS ===\n\n")
            f.write("✅ No se encontraron errores sintácticos\n\n")
        
        # Errores Semánticos
        f.write("=" * 70 + "\n")
        if resultado['sem_errors']:
            f.write("=== ERRORES SEMÁNTICOS ===\n\n")
            for err in resultado['sem_errors']:
                f.write(f"{err}\n")
            f.write(f"\nTotal: {len(resultado['sem_errors'])}\n\n")
        else:
            f.write("=== ERRORES SEMÁNTICOS ===\n\n")
            f.write("✅ No se encontraron errores semánticos\n\n")
        
        # Tabla de Símbolos
        f.write("=" * 70 + "\n")
        f.write("=== TABLA DE SÍMBOLOS ===\n\n")
        if resultado['symbol_table']:
            f.write(f"{'Variable':<20} {'Tipo':<15} {'Mutable':<10}\n")
            f.write("-" * 45 + "\n")
            for name, info in resultado['symbol_table'].items():
                tipo = info.get('type', 'Unknown')
                mut = 'var' if info.get('mutable') else 'val'
                f.write(f"{name:<20} {tipo:<15} {mut:<10}\n")
        else:
            f.write("(vacía)\n")
        
        # Tabla de Funciones
        f.write("\n" + "=" * 70 + "\n")
        f.write("=== TABLA DE FUNCIONES ===\n\n")
        if resultado['function_table']:
            f.write(f"{'Función':<20} {'Retorno':<15} {'Parámetros':<10}\n")
            f.write("-" * 45 + "\n")
            for name, info in resultado['function_table'].items():
                ret = info.get('ret', 'Unit')
                params = len(info.get('params', []))
                f.write(f"{name:<20} {ret:<15} {params:<10}\n")
        else:
            f.write("(vacía)\n")
        
        # Tabla de Clases
        f.write("\n" + "=" * 70 + "\n")
        f.write("=== TABLA DE CLASES ===\n\n")
        if resultado['class_table']:
            for name, info in resultado['class_table'].items():
                f.write(f"Clase: {name}\n")
                if 'params' in info:
                    f.write(f"  Parámetros: {len(info['params'])}\n")
                if 'methods' in info:
                    f.write(f"  Métodos: {len(info['methods'])}\n")
                f.write("\n")
        else:
            f.write("(vacía)\n")
        
        # Resumen
        f.write("\n" + "=" * 70 + "\n")
        f.write("=== RESUMEN ===\n\n")
        f.write(f"Tokens: {len(resultado['tokens'])}\n")
        f.write(f"Errores léxicos: {len(resultado['lex_errors'])}\n")
        f.write(f"Errores sintácticos: {len(resultado['syn_errors'])}\n")
        f.write(f"Errores semánticos: {len(resultado['sem_errors'])}\n")
        
        total_errores = (len(resultado['lex_errors']) + 
                        len(resultado['syn_errors']) + 
                        len(resultado['sem_errors']))
        
        if total_errores == 0:
            f.write("\n✅ ANÁLISIS COMPLETADO EXITOSAMENTE\n")
        else:
            f.write(f"\n❌ ANÁLISIS COMPLETADO CON {total_errores} ERRORES\n")
    
    return ruta_log

def analizar_archivo(ruta_archivo):
    """Analiza un archivo .kt"""
    usuario = extraer_usuario_de_archivo(ruta_archivo)
    nombre_archivo = os.path.basename(ruta_archivo)
    
    print(f"\n{'='*70}")
    print(f"📄 Analizando: {nombre_archivo}")
    print(f"👤 Usuario: {usuario}")
    print(f"{'='*70}")
    
    # Leer código
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return
    
    # Analizar
    resultado = analyze_syntax(codigo)
    
    # Mostrar estadísticas en consola
    print(f"\n📊 Estadísticas:")
    print(f"   • Tokens reconocidos: {len(resultado['tokens'])}")
    print(f"   • Errores léxicos: {len(resultado['lex_errors'])}")
    print(f"   • Errores sintácticos: {len(resultado['syn_errors'])}")
    print(f"   • Errores semánticos: {len(resultado['sem_errors'])}")
    
    # Guardar log
    ruta_log = guardar_log(usuario, resultado)
    print(f"\n✅ Log generado: {os.path.basename(ruta_log)}")
    
    # Mostrar errores en consola
    if resultado['syn_errors']:
        print(f"\n⚠️  Errores Sintácticos:")
        for err in resultado['syn_errors'][:3]:
            print(f"   • {err}")
        if len(resultado['syn_errors']) > 3:
            print(f"   ... y {len(resultado['syn_errors']) - 3} más")
    
    if resultado['sem_errors']:
        print(f"\n⚠️  Errores Semánticos:")
        for err in resultado['sem_errors'][:3]:
            print(f"   • {err}")
        if len(resultado['sem_errors']) > 3:
            print(f"   ... y {len(resultado['sem_errors']) - 3} más")
    
    # Mostrar tabla de símbolos
    if resultado['symbol_table']:
        print(f"\n📋 Variables declaradas: {len(resultado['symbol_table'])}")
    
    if resultado['function_table']:
        print(f"📋 Funciones declaradas: {len(resultado['function_table'])}")
    
    if resultado['class_table']:
        print(f"📋 Clases declaradas: {len(resultado['class_table'])}")

def listar_archivos_kotlin():
    """Lista todos los archivos .kt"""
    if not os.path.isdir(ALGO_DIR):
        return []
    
    archivos = [
        os.path.join(ALGO_DIR, f) 
        for f in os.listdir(ALGO_DIR) 
        if f.endswith('.kt')
    ]
    return sorted(archivos)

# FUNCIÓN PRINCIPAL

def main():
    """Analiza todos los archivos .kt"""
    print("\n" + "="*70)
    print("🚀 ANALIZADOR SINTÁCTICO - MINIKOTLIN MEJORADO")
    print("="*70)
    
    # Buscar archivos
    archivos = listar_archivos_kotlin()
    
    if not archivos:
        print("\n❌ No se encontraron archivos .kt en 'algoritmos_kotlin/'")
        print(f"   Ruta: {ALGO_DIR}")
        return
    
    print(f"\n🔍 Encontrados {len(archivos)} archivo(s):")
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