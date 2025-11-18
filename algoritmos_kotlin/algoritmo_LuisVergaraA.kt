// AVANCE 1

Prueba 1: Declaración de funciones básicas
fun suma(a: Int, b: Int): Int {
    return a + b
}

fun resta(x: Int, y: Int): Int {
    return x - y
}

fun multiplicar(m: Int, n: Int): Int {
    return m * n
}

fun dividir(numerador: Int, denominador: Int): Int {
    return numerador / denominador
}

fun modulo(a: Int, b: Int): Int {
    return a % b
}


// Prueba 2: Variables val e var
val constante = 100
var variable = 50


// Prueba 3: Operadores de asignación compuesta
fun incrementos() {
    var contador = 0
    contador++       // Operador ++
    contador--       // Operador --
    contador += 10   // Operador +=
    contador -= 5    // Operador -=
    
    return
}


// Prueba 4: Estructuras if-else
fun valorAbsoluto(numero: Int): Int {
    if (numero >= 0) {
        return numero
    } else {
        return -numero
    }
}


// Prueba 5: Lambdas con arrow operator
val cuadrado = { x: Int -> x * x }
val cubo = { n: Int -> n * n * n }


// Prueba 6: Rangos con operador ..
fun usarRangos() {
    val rango1 = 1..10
    val rango2 = 0..100
    return
}


// Prueba 7: Operaciones aritméticas combinadas
fun operacionesComplejas() {
    val a = 10
    val b = 5
    val c = 3
    
    val resultado1 = a + b * c
    val resultado2 = (a + b) * c
    val resultado3 = a / b + c
    val resultado4 = a % b - c
    
    return
}


// Prueba 8: Funciones anidadas con returns
fun funcionExterna(): Int {
    fun funcionInterna(): Int {
        return 42
    }
    
    return funcionInterna()
}


// Prueba 9: Uso de val y var en expresiones
fun asignaciones() {
    val x = 10 + 5
    val y = x * 2
    var z = y / 3
    z += 1
    
    return
}


// Prueba 10: If-else como expresión
fun maximo(a: Int, b: Int): Int {
    val max = if (a > b) a else b
    return max
}


// AVANCE 2: SINTAXIS COMPLEJA 

// PRUEBA 1: DECLARACIÓN Y ASIGNACIÓN
// Declaración con val (inmutable)
val constante = 100;
val pi = 3.14159;
val nombre = "Juan";
val activo = true;

// Declaración con var (mutable)
var contador = 0;
var temperatura = 25.5;
var mensaje = "Hola";
var esValido = false;

// Asignaciones múltiples
var x = 10;
x = 20;
x = 30;

var y = 5;
y = y + 10;
y = y * 2;


// PRUEBA 2: EXPRESIONES ARITMÉTICAS
// Operadores básicos
val suma = 10 + 5;
val resta = 20 - 8;
val multiplicacion = 4 * 7;
val division = 50 / 2;
val modulo = 17 % 5;

// Expresiones compuestas
val resultado1 = 10 + 5 * 3;
val resultado2 = (10 + 5) * 3;
val resultado3 = 100 / (2 + 3);
val resultado4 = 10 + 20 - 5 * 2;

// Con paréntesis anidados
val complejo1 = ((10 + 5) * (3 - 1)) / 2;
val complejo2 = (50 - (10 + 5)) * 2;

// Operadores unarios
val negativo = -10;
val dobleNegativo = -(-5);


// PRUEBA 3: EXPRESIONES LÓGICAS
// Operadores relacionales
val esMayor = 10 > 5;
val esMenor = 3 < 8;
val esIgual = 5 == 5;
val esDiferente = 7 != 3;
val mayorIgual = 10 >= 10;
val menorIgual = 5 <= 8;

// Operadores lógicos AND
val ambosVerdaderos = true && true;
val unoFalso = true && false;
val condicion1 = (10 > 5) && (20 < 30);
val condicion2 = (x > 0) && (y > 0);

// Operadores lógicos OR
val alMenosUno = true || false;
val ambos = false || false;
val condicion3 = (x < 0) || (y < 0);
val condicion4 = (temperatura > 30) || (temperatura < 0);

// Operador de negación
val noVerdadero = !true;
val noFalso = !false;
val negacion1 = !(10 > 5);
val negacion2 = !(x == 0);

// Combinaciones complejas
val compleja1 = (10 > 5) && (20 < 30) || (x == 0);
val compleja2 = !(x > 10) && (y < 20);
val compleja3 = (a >= 0 && a <= 100) || (b >= 0 && b <= 100);


// PRUEBA 4: IMPRESIÓN (println)
println(42);
println(3.14);
println("Hola Mundo");
println(true);
println(x);
println(x + y);
println((10 + 5) * 2);
println(x > 10);
println("El resultado es:");


// PRUEBA 5: ESTRUCTURAS DE CONTROL (if-else)
// If simple
if (x > 0) {
    println("x es positivo");
}

// If-else
if (temperatura > 30) {
    println("Hace calor");
} else {
    println("Temperatura normal");
}

// If-else anidado
if (x > 0) {
    println("Positivo");
} else {
    if (x < 0) {
        println("Negativo");
    } else {
        println("Cero");
    }
}

// If-else como expresión
val mensaje1 = if (x > 10) "Grande" else "Pequeño";
val estado = if (activo) "Activo" else "Inactivo";

// Condiciones complejas
if ((x > 0) && (y > 0)) {
    println("Ambos positivos");
}

if ((temperatura > 35) || (temperatura < 0)) {
    println("Temperatura extrema");
} else {
    println("Temperatura normal");
}

if (!(x == 0) && (y != 0)) {
    val division = x / y;
    println(division);
}

// AVANCE 3: PRUEBAS SEMÁNTICAS 

// Prueba 1: Uso de variable no declarada
fun errorVariableNoDeclarada() {
    println(variableInexistente);  // ERROR: variable no declarada
}

// Prueba 2: Reasignación de val
fun errorReasignacionVal() {
    val constante = 100;
    constante = 200;  // ERROR: val es inmutable
}

// Prueba 3: Variable usada antes de inicializar
fun errorUsoSinInicializar() {
    var x;
    println(x);  // ERROR: usada antes de inicializar
    x = 10;
}

// Prueba 4: Redeclaración de variable
fun errorRedeclaracion() {
    val nombre = "Juan";
    val nombre = "Pedro";  // ERROR: redeclaración
}

// Prueba 5: Múltiples errores de inmutabilidad
fun errorMultiplesVal() {
    val a = 10;
    val b = 20;
    val c = 30;
    
    a = 11;  // ERROR: a es inmutable
    b = 21;  // ERROR: b es inmutable
    c = 31;  // ERROR: c es inmutable
}

// Prueba 6: Variables correctas (sin errores)
fun variablesCorrectas() {
    var x = 10;
    x = 20;  // OK: x es var
    x = 30;  // OK
    
    val y = 100;
    // No se reasigna y
    
    println(x);  // OK: x está declarada e inicializada
    println(y);  // OK: y está declarada e inicializada
}

// Prueba 7: val sin inicialización
fun errorValSinInicializar() {
    val sinValor;  // ERROR: val debe inicializarse
}
