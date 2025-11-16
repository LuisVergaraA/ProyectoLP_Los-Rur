// AVANCE 1

// Prueba 1: Ciclo while con operadores relacionales
fun contarHastaDiez() {
    var i = 0
    while (i < 10) {
        println(i)
        i++
    }
    return
}


// Prueba 2: Ciclo for con rangos
fun imprimirNumeros() {
    for (numero in 1..20) {
        println(numero)
    }
    return
}


// Prueba 3: Operadores relacionales
fun compararNumeros(a: Int, b: Int) {
    val menor = a < b
    val mayor = a > b
    val menorIgual = a <= b
    val mayorIgual = a >= b
    val igual = a == b
    val diferente = a != b
    
    return
}


// Prueba 4: Operadores lógicos AND y OR
fun validarRango(numero: Int): Boolean {
    return numero >= 1 && numero <= 100
}

fun estaFueraDeRango(n: Int): Boolean {
    return n < 0 || n > 100
}


// Prueba 5: Operador de negación !
fun invertir(valor: Boolean): Boolean {
    return !valor
}


// Prueba 6: Valores booleanos true, false, null
val verdadero = true
val falso = false
val nulo = null


// AVANCE 2

// Prueba 1: While anidado
fun tablaMultiplicar() {
    var i = 1
    while (i <= 5) {
        var j = 1
        while (j <= 5) {
            val producto = i * j
            println(producto)
            j = j + 1
        }
        i = i + 1
    }
    return
}


// Prueba 2: For con rangos de variables
fun sumarRango() {
    val inicio = 1
    val fin = 100
    var suma = 0
    
    for (num in inicio..fin) {
        suma = suma + num
    }
    
    return suma
}

// Prueba 3: For anidado
fun matrizNumeros() {
    for (fila in 1..3) {
        for (columna in 1..3) {
            val valor = fila * columna
            println(valor)
        }
    }
    return
}

// Prueba 4: Declaración de rangos como variables
val rango1 = 1..10
val rango2 = 0..100
val rango3 = -5..5

fun usarRangos() {
    val rangoEdades = 18..65
    val rangoTemperaturas = -10..40
    
    for (edad in 18..25) {
        println(edad)
    }
    return
}

// Prueba 5: Operador in con listas
fun verificarPertenencia() {
    val numero = 5
    val enRango = numero in 1..10
    
    if (numero in 1..100) {
        println("Número válido")
    }
    
    val lista = [1, 2, 3, 4, 5]
    val encontrado = 3 in lista
    
    return enRango
}

// Prueba 6: Lambdas con arrow operator
val duplicar = { x: Int -> x * 2 }
val triplicar = { n: Int -> n * 3 }

val sumarLambda = { a: Int, b: Int -> a + b }
val multiplicarLambda = { x: Int, y: Int -> x * y }

val esParLambda = { num: Int -> num % 2 == 0 }
val esMayorLambda = { a: Int, b: Int -> a > b }