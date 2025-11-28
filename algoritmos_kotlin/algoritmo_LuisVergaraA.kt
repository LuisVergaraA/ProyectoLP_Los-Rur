// =============================================================================
// ALGORITMO DE PRUEBA - INTEGRANTE 1: LUIS VERGARA
// =============================================================================
// Responsable: Variables, Expresiones, If-Else, Reglas Semánticas 1 y 2
// =============================================================================

// AVANCE 1: ANÁLISIS LÉXICO

// Prueba 1: Declaración de funciones básicas
fun suma(a: Int, b: Int): Int {
    return a + b;
}

fun resta(x: Int, y: Int): Int {
    return x - y;
}

fun multiplicar(m: Int, n: Int): Int {
    return m * n;
}

fun dividir(numerador: Int, denominador: Int): Int {
    return numerador / denominador;
}

fun modulo(a: Int, b: Int): Int {
    return a % b;
}

// Prueba 2: Variables val e var
val constante = 100;
var variable = 50;

// Prueba 3: Operadores de asignación compuesta
fun incrementos() {
    var contador = 0;
    contador = contador + 1;
    contador = contador + 10;
    contador = contador - 5;
    return;
}

// Prueba 4: Estructuras if-else
fun valorAbsoluto(numero: Int): Int {
    if (numero >= 0) {
        return numero;
    } else {
        return -numero;
    }
}

// Prueba 5: Operaciones aritméticas combinadas
fun operacionesComplejas() {
    val a = 10;
    val b = 5;
    val c = 3;
    
    val resultado1 = a + b * c;
    val resultado2 = (a + b) * c;
    val resultado3 = a / b + c;
    val resultado4 = a % b - c;
    
    return;
}
// Prueba 6: Funciones anidadas con returns
fun funcionExterna(): Int {
    fun funcionInterna(): Int {
        return 42;
    }
    return funcionInterna();
}

// Prueba 7: Uso de val y var en expresiones
fun asignaciones() {
    val x = 10 + 5;
    val y = x * 2;
    var z = y / 3;
    z = z + 1;
    return;
}
// Prueba 8: If-else como expresión
fun maximo(a: Int, b: Int): Int {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

// =============================================================================
// AVANCE 2: ANÁLISIS SINTÁCTICO
// =============================================================================

// Prueba 1: Declaración y asignación
val pi = 3.14159;
val nombre = "Juan";
val activo = true;

var contador = 0;
var temperatura = 25.5;
var mensaje = "Hola";

// Prueba 2: Expresiones aritméticas
fun expresionesAritmeticas() {
    val suma = 10 + 5;
    val resta = 20 - 8;
    val multiplicacion = 4 * 7;
    val division = 50 / 2;
    val modulo = 17 % 5;
    
    val resultado1 = 10 + 5 * 3;
    val resultado2 = (10 + 5) * 3;
    val resultado3 = 100 / (2 + 3);
    
    val negativo = -10;
    
    return;
}

// Prueba 3: Expresiones lógicas
fun expresionesLogicas() {
    val esMayor = 10 > 5;
    val esMenor = 3 < 8;
    val esIgual = 5 == 5;
    val esDiferente = 7 != 3;
    
    val ambosVerdaderos = true && true;
    val alMenosUno = true || false;
    val noVerdadero = !true;
    
    return;
}

// Prueba 4: Impresión
fun pruebaPrintln() {
    println(42);
    println(3.14);
    println("Hola Mundo");
    println(true);
    return;
}

// Prueba 5: Estructuras if-else anidadas
fun ifElseAnidado(x: Int): Int {
    if (x > 0) {
        return 1;
    } else {
        if (x < 0) {
            return -1;
        } else {
            return 0;
        }
    }
}

// Prueba 6: Condiciones complejas
fun condicionesComplejas(x: Int, y: Int) {
    if ((x > 0) && (y > 0)) {
        println("Ambos positivos");
    }
    
    if ((x > 10) || (y > 10)) {
        println("Al menos uno mayor que 10");
    }
    
    return;
}

// =============================================================================
// AVANCE 3: ANÁLISIS SEMÁNTICO - REGLAS 1 Y 2
// =============================================================================

// Prueba Semántica 1: Uso de variable no declarada (ERROR REGLA 1)
fun errorVariableNoDeclarada() {
    println(variableInexistente);
}

// Prueba Semántica 2: Reasignación de val (ERROR REGLA 2)
fun errorReasignacionVal() {
    val constante = 100;
    constante = 200;
}

// Prueba Semántica 3: Variable usada antes de inicializar (ERROR REGLA 1)
fun errorUsoSinInicializar() {
    var x;
    println(x);
    x = 10;
}

// Prueba Semántica 4: Redeclaración de variable (ERROR REGLA 1)
fun errorRedeclaracion() {
    val nombre = "Juan";
    val nombre = "Pedro";
}

// Prueba Semántica 5: Múltiples errores de inmutabilidad (ERROR REGLA 2)
fun errorMultiplesVal() {
    val a = 10;
    val b = 20;
    val c = 30;
    
    a = 11;
    b = 21;
    c = 31;
}

// Prueba Semántica 6: Variables correctas (SIN ERRORES)
fun variablesCorrectas() {
    var x = 10;
    x = 20;
    x = 30;
    
    val y = 100;
    
    println(x);
    println(y);
}

// Prueba Semántica 7: Operaciones aritméticas válidas (SIN ERRORES)
fun operacionesValidas() {
    val a = 10;
    val b = 20;
    
    val suma = a + b;
    val resta = a - b;
    val mult = a * b;
    val div = b / a;
    val mod = b % a;
    
    return;
}

// Prueba Semántica 8: If-else con variables correctas (SIN ERRORES)
fun ifElseCorrecto(numero: Int): Int {
    var resultado = 0;
    
    if (numero > 0) {
        resultado = 1;
    } else {
        resultado = -1;
    }
    
    return resultado;
}

// =============================================================================
// FIN DEL ALGORITMO DE PRUEBA
// =============================================================================