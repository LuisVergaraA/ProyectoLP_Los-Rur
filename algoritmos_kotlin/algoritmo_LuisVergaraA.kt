// Prueba 1: Declaración de funciones básicas
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


