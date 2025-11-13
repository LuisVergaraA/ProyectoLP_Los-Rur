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