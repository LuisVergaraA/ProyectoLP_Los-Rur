from flask import Flask, render_template, request, jsonify
from analizador_sintactico import analyze_syntax
import os

app = Flask(__name__)

# Cargar algoritmos de ejemplo
def cargar_ejemplos():
    ejemplos = {}
    carpeta = 'algoritmos_kotlin'
    
    if os.path.exists(carpeta):
        for archivo in os.listdir(carpeta):
            if archivo.endswith('.kt'):
                ruta = os.path.join(carpeta, archivo)
                with open(ruta, 'r', encoding='utf-8') as f:
                    ejemplos[archivo] = f.read()
    
    return ejemplos

@app.route('/')
def index():
    ejemplos = cargar_ejemplos()
    return render_template('index.html', ejemplos=ejemplos)

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.get_json()
    codigo = data.get('codigo', '')
    
    if not codigo.strip():
        return jsonify({'error': 'El código está vacío'}), 400
    
    # Ejecutar análisis
    resultado = analyze_syntax(codigo)
    
    # Preparar respuesta
    response = {
        'tokens': resultado['tokens'],
        'errores': {
            'lexicos': resultado['lex_errors'],
            'sintacticos': resultado['syn_errors'],
            'semanticos': resultado['sem_errors']
        },
        'tablas': {
            'variables': resultado['symbol_table'],
            'funciones': resultado['function_table'],
            'clases': resultado['class_table']
        },
        'ast': str(resultado['ast']) if resultado['ast'] else None
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)