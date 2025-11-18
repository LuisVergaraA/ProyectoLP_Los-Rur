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
    """Formato: semantico-usuario-ddmmyyyy-HHhMM.txt"""
    now = datetime.now()
    fecha = now.strftime('%d%m%Y')
    hora = now.strftime('%Hh%M')
    return f"semantico-{usuario}-{fecha}-{hora}.txt"

def guardar_log(usuario, resultado):
    """Guarda log de análisis semántico"""
    nombre_log = generar_nombre_log(usuario)
    ruta_log = os.path.join(LOGS_DIR, nombre_log)
    
    with open(ruta_log, 'w', encoding='utf-8') as f:
        # Encabezado
        f.write("=" * 80 + "\n")
        f.write("ANALIZADOR SEMÁNTICO - MINIKOTLIN MEJORADO\n")
        f.write("Avance 3: Análisis Semántico\n")
        f.write(f"Usuario: {usuario}\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Resumen ejecutivo
        total_errores = (len(resultado['lex_errors']) + 
                        len(resultado['syn_errors']) + 
                        len(resultado['sem_errors']))
        
        f.write("=== RESUMEN EJECUTIVO ===\n\n")
        f.write(f"Tokens analizados:        {len(resultado['tokens'])}\n")
        f.write(f"Errores léxicos:          {len(resultado['lex_errors'])}\n")
        f.write(f"Errores sintácticos:      {len(resultado['syn_errors'])}\n")
        f.write(f"Errores semánticos:       {len(resultado['sem_errors'])}\n")
        f.write(f"Total de errores:         {total_errores}\n")
        f.write(f"\nEstado: {'❌ CON ERRORES' if total_errores > 0 else '✅ SIN ERRORES'}\n\n")
        
        # Errores Léxicos
        if resultado['lex_errors']:
            f.write("=" * 80 + "\n")
            f.write("=== ERRORES LÉXICOS ===\n\n")
            for i, err in enumerate(resultado['lex_errors'], 1):
                f.write(f"{i}. {err}\n")
            f.write(f"\nTotal: {len(resultado['lex_errors'])}\n\n")
        
        # Errores Sintácticos
        if resultado['syn_errors']:
            f.write("=" * 80 + "\n")
            f.write("=== ERRORES SINTÁCTICOS ===\n\n")
            for i, err in enumerate(resultado['syn_errors'], 1):
                f.write(f"{i}. {err}\n")
            f.write(f"\nTotal: {len(resultado['syn_errors'])}\n\n")
        
        # Errores Semánticos (PRINCIPAL)
        f.write("=" * 80 + "\n")
        f.write("=== ERRORES SEMÁNTICOS ===\n\n")
        
        if resultado['sem_errors']:
            # Clasificar errores por tipo
            errores_variables = []
            errores_funciones = []
            errores_tipos = []
            errores_clases = []
            errores_otros = []
            
            for err in resultado['sem_errors']:
                if 'no declarada' in err or 'inmutable' in err or 'inicializar' in err:
                    errores_variables.append(err)
                elif 'Función' in err or 'retorno' in err:
                    errores_funciones.append(err)
                elif 'Operación' in err or 'Operador' in err or 'tipo' in err.lower():
                    errores_tipos.append(err)
                elif 'Clase' in err or 'Miembro' in err or 'Propiedad' in err:
                    errores_clases.append(err)
                else:
                    errores_otros.append(err)
            
            # Mostrar por categoría
            if errores_variables:
                f.write("📌 Errores de Variables (Integrante 1):\n\n")
                for i, err in enumerate(errores_variables, 1):
                    f.write(f"   {i}. {err}\n")
                f.write(f"\n   Subtotal: {len(errores_variables)}\n\n")
            
            if errores_funciones:
                f.write("📌 Errores de Funciones (Integrante 2):\n\n")
                for i, err in enumerate(errores_funciones, 1):
                    f.write(f"   {i}. {err}\n")
                f.write(f"\n   Subtotal: {len(errores_funciones)}\n\n")
            
            if errores_tipos:
                f.write("📌 Errores de Tipos en Operaciones (Integrante 3):\n\n")
                for i, err in enumerate(errores_tipos, 1):
                    f.write(f"   {i}. {err}\n")
                f.write(f"\n   Subtotal: {len(errores_tipos)}\n\n")
            
            if errores_clases:
                f.write("📌 Errores de Clases y Miembros (Integrante 3):\n\n")
                for i, err in enumerate(errores_clases, 1):
                    f.write(f"   {i}. {err}\n")
                f.write(f"\n   Subtotal: {len(errores_clases)}\n\n")
            
            if errores_otros:
                f.write("📌 Otros Errores Semánticos:\n\n")
                for i, err in enumerate(errores_otros, 1):
                    f.write(f"   {i}. {err}\n")
                f.write(f"\n   Subtotal: {len(errores_otros)}\n\n")
            
            f.write(f"Total de errores semánticos: {len(resultado['sem_errors'])}\n\n")
        else:
            f.write("✅ No se encontraron errores semánticos\n\n")
        
        # Tabla de Símbolos
        f.write("=" * 80 + "\n")
        f.write("=== TABLA DE SÍMBOLOS ===\n\n")
        
        if resultado['symbol_table']:
            f.write(f"{'Variable':<25} {'Tipo':<15} {'Mutable':<10} {'Inicializada':<12}\n")
            f.write("-" * 62 + "\n")
            for name, info in sorted(resultado['symbol_table'].items()):
                tipo = info.get('type', 'Unknown')
                mut = 'var' if info.get('mutable') else 'val'
                init = 'Sí' if info.get('initialized') else 'No'
                f.write(f"{name:<25} {tipo:<15} {mut:<10} {init:<12}\n")
            f.write(f"\nTotal de variables: {len(resultado['symbol_table'])}\n")
        else:
            f.write("(vacía)\n")
        
        # Tabla de Funciones
        f.write("\n" + "=" * 80 + "\n")
        f.write("=== TABLA DE FUNCIONES ===\n\n")
        
        if resultado['function_table']:
            f.write(f"{'Función':<25} {'Tipo Retorno':<15} {'Parámetros':<12}\n")
            f.write("-" * 52 + "\n")
            for name, info in sorted(resultado['function_table'].items()):
                ret = info.get('ret', 'Unit')
                params = len(info.get('params', []))
                f.write(f"{name:<25} {ret:<15} {params:<12}\n")
            f.write(f"\nTotal de funciones: {len(resultado['function_table'])}\n")
        else:
            f.write("(vacía)\n")
        
        # Tabla de Clases
        f.write("\n" + "=" * 80 + "\n")
        f.write("=== TABLA DE CLASES ===\n\n")
        
        if resultado['class_table']:
            for name, info in sorted(resultado['class_table'].items()):
                tipo_clase = info.get('type', 'class')
                f.write(f"{'Object' if tipo_clase == 'object' else 'Clase'}: {name}\n")
                
                props = info.get('properties', {})
                if props:
                    f.write(f"  Propiedades ({len(props)}):\n")
                    for prop_name, prop_info in props.items():
                        prop_type = prop_info.get('type', 'Unknown')
                        prop_mut = 'var' if prop_info.get('mutable') else 'val'
                        f.write(f"    - {prop_name}: {prop_type} ({prop_mut})\n")
                
                methods = info.get('methods', {})
                if methods:
                    f.write(f"  Métodos ({len(methods)}):\n")
                    for method_name, method_info in methods.items():
                        method_ret = method_info.get('ret', 'Unit')
                        method_params = len(method_info.get('params', []))
                        f.write(f"    - {method_name}({method_params} params) -> {method_ret}\n")
                
                f.write("\n")
            
            f.write(f"Total de clases/objects: {len(resultado['class_table'])}\n")
        else:
            f.write("(vacía)\n")
        
        # Análisis de reglas semánticas aplicadas
        f.write("\n" + "=" * 80 + "\n")
        f.write("=== REGLAS SEMÁNTICAS APLICADAS ===\n\n")
        
        f.write("Integrante 1 - Variables y Tipos:\n")
        f.write("  ✓ Regla 1: Verificación de declaración de variables\n")
        f.write("  ✓ Regla 2: Inmutabilidad de variables val\n\n")
        
        f.write("Integrante 2 - Funciones:\n")
        f.write("  ✓ Regla 3: Verificación de existencia de funciones\n")
        f.write("  ✓ Regla 4: Consistencia de tipo de retorno\n\n")
        
        f.write("Integrante 3 - Operaciones y Clases:\n")
        f.write("  ✓ Regla 5: Verificación de tipos en operaciones aritméticas\n")
        f.write("  ✓ Regla 6: Verificación de acceso a miembros de clases\n\n")
        
        # Footer
        f.write("=" * 80 + "\n")
        f.write("=== CONCLUSIÓN ===\n\n")
        
        if total_errores == 0:
            f.write("✅ El código es SEMÁNTICAMENTE CORRECTO.\n")
            f.write("   No se encontraron violaciones a las reglas semánticas.\n")
        else:
            f.write(f"❌ Se encontraron {total_errores} error(es) en total.\n")
            if resultado['sem_errors']:
                f.write(f"   {len(resultado['sem_errors'])} error(es) semántico(s) deben ser corregidos.\n")
        
        f.write(f"\nAnalizado por: {usuario}\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 80 + "\n")
    
    return ruta_log

def analizar_archivo(ruta_archivo):
    """Analiza un archivo .kt"""
    usuario = extraer_usuario_de_archivo(ruta_archivo)
    nombre_archivo = os.path.basename(ruta_archivo)
    
    print(f"\n{'='*80}")
    print(f"📄 Analizando: {nombre_archivo}")
    print(f"👤 Usuario: {usuario}")
    print(f"{'='*80}")
    
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
    total_errores = (len(resultado['lex_errors']) + 
                    len(resultado['syn_errors']) + 
                    len(resultado['sem_errors']))
    
    print(f"\n📊 Estadísticas:")
    print(f"   • Tokens reconocidos: {len(resultado['tokens'])}")
    print(f"   • Errores léxicos: {len(resultado['lex_errors'])}")
    print(f"   • Errores sintácticos: {len(resultado['syn_errors'])}")
    print(f"   • Errores semánticos: {len(resultado['sem_errors'])} ⭐")
    print(f"   • Total de errores: {total_errores}")
    
    # Guardar log
    ruta_log = guardar_log(usuario, resultado)
    print(f"\n✅ Log generado: {os.path.basename(ruta_log)}")
    
    # Mostrar errores semánticos en consola
    if resultado['sem_errors']:
        print(f"\n⚠️  Errores Semánticos Detectados:")
        for i, err in enumerate(resultado['sem_errors'][:5], 1):
            print(f"   {i}. {err}")
        if len(resultado['sem_errors']) > 5:
            print(f"   ... y {len(resultado['sem_errors']) - 5} más")
    else:
        print(f"\n✅ ¡Código semánticamente correcto!")
    
    # Mostrar tablas
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
    print("\n" + "="*80)
    print("🚀 ANALIZADOR SEMÁNTICO - MINIKOTLIN MEJORADO")
    print("   Avance 3: Análisis Semántico")
    print("="*80)
    
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
    print("\n" + "="*80)
    print("✅ ANÁLISIS SEMÁNTICO COMPLETADO")
    print(f"📁 Logs guardados en: {LOGS_DIR}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()