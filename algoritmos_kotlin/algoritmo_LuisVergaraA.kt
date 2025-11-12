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


