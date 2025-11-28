# ProyectoLP_Los-Rur
# Analizador Léxico, Sintáctico y Semántico para MiniKotlin

## Equipo
- Luis Vergara - LuisVergaraA - Responsable: Variables, Expresiones (Reglas 1, 2)
- Luis Roca - LuisRoca09 - Responsable: Funciones, Estructuras de Control (Reglas 3, 4)
- Johao Dorado - johaodorado - Responsable: Clases, POO (Reglas 5, 6)

## Avances

### ✅ Avance 1: Analizador Léxico
- Tokens: 40+ tokens implementados
- Palabras reservadas: 15
- Literales: INT, DOUBLE, STRING, CHAR
- Operadores: Aritméticos, Lógicos, Relacionales
- Estado: Completo y funcional

### ✅ Avance 2: Analizador Sintáctico
- Reglas sintácticas: 25+ reglas
- Estructuras: if-else, while, for, when
- Funciones: Definición, parámetros, return
- Clases: class, object, propiedades, métodos
- Estado: Completo y funcional

### ✅ Avance 3: Analizador Semántico
- Reglas semánticas: 6 reglas implementadas
- Validaciones: Variables, funciones, tipos, clases
- Tablas: Símbolos, funciones, clases
- Estado: Completo y funcional

## Estructura del Proyecto
ProyectoLP_Los-Rur/
├── analizador_lexico.py       
├── analizador_sintactico.py   
├── test_lexico.py             
├── test_sintactico.py      
├── test_semantico.py 
├── requirements.txt      
├── README.md             
├── .gitignore               
├── Documentacion_LOSRUR.pdf 
├── algoritmos_kotlin/        
│   ├── algoritmo_LuisVergaraA.kt
│   ├── algoritmo_LuisRoca09.kt
│   └── algoritmo_johaodorado.kt
└── logs/                     
├── lexico-.txt
├── sintactico-.txt
└── semantico-*.txt

## Instalación
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/ProyectoLP_Los-Rur.git
cd ProyectoLP_Los-Rur

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Análisis Léxico
```bash
python test_lexico.py
```

### Análisis Sintáctico
```bash
python test_sintactico.py
```

### Análisis Semántico
```bash
python test_semantico.py
```

### Ver Logs
```bash
# Ver logs léxicos
cat logs/lexico-LuisVergaraA-*.txt

# Ver logs sintácticos
cat logs/sintactico-LuisRoca09-*.txt

# Ver logs semánticos
cat logs/semantico-johaodorado-*.txt
```

## Reglas Semánticas Implementadas

Ver [Documentacion_LOSRUR.pdf](https://github.com/LuisVergaraA/ProyectoLP_Los-Rur/blob/main/Documentacion_LOSRUR.pdf) para detalles completos.

### Integrante 1: Luis Vergara
- **Regla 1:** Verificación de declaración de variables
- **Regla 2:** Inmutabilidad de variables `val`

### Integrante 2: Luis Roca
- **Regla 3:** Verificación de existencia de funciones
- **Regla 4:** Consistencia de tipo de retorno

### Integrante 3: Johao Dorado
- **Regla 5:** Verificación de tipos en operaciones
- **Regla 6:** Verificación de acceso a miembros de clases

## Estado del Proyecto

🟢 **Avance 1:** Completado  
🟢 **Avance 2:** Completado  
🟢 **Avance 3:** Completado

## Licencia

Este proyecto es para fines académicos.
