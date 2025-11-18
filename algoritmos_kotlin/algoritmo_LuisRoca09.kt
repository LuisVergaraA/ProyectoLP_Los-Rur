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


// AVANCE 3: PRUEBAS SEMÁNTICAS 


// Prueba 1: Llamada a función no declarada
fun errorFuncionNoDeclarada() {
    funcionInexistente();  // ERROR: función no declarada
}

// Prueba 2: Llamada antes de declaración
fun errorLlamadaAntes() {
    funcionTarde();  // ERROR: función no declarada aún
}

fun funcionTarde() {
    println("Tardía");
}

// Prueba 3: Inconsistencia en tipo de retorno
fun errorRetornoInconsistente(): Int {
    if (true) {
        return 42;        // OK: Int
    } else {
        return "texto";   // ERROR: String no es Int
    }
}

// Prueba 4: Return sin valor cuando se espera tipo
fun errorRetornoVacio(): Int {
    return;  // ERROR: debe retornar Int
}

// Prueba 5: Return con valor cuando es Unit
fun errorRetornoSobrante() {
    return 42;  // ERROR: función es Unit, no debe retornar valor
}

// Prueba 6: Número incorrecto de argumentos
fun sumar(a: Int, b: Int): Int {
    return a + b;
}

fun errorArgumentos() {
    val resultado1 = sumar(10);        // ERROR: faltan argumentos
    val resultado2 = sumar(10, 20, 30); // ERROR: demasiados argumentos
}

// Prueba 7: Funciones correctas (sin errores)
fun funcionCorrecta1(): Int {
    return 42;  // OK
}

fun funcionCorrecta2(x: Int, y: Int): Int {
    if (x > y) {
        return x;  // OK: Int
    } else {
        return y;  // OK: Int
    }
}

fun funcionCorrecta3() {
    println("Sin retorno");  // OK: Unit implícito
}

// Prueba 8: Return fuera de función
val x = 10;
return x;  // ERROR: return fuera de función

// Prueba 9: Múltiples returns inconsistentes
fun errorMultiplesReturns(): Int {
    val condicion = true;
    
    if (condicion) {
        return 10;        // OK: Int
    }
    
    if (!condicion) {
        return 20;        // OK: Int
    }
    
    return "texto";       // ERROR: String no es Int
}

// Prueba Semántica 10: Redeclaración de función
fun miFuncion(): Int {
    return 1;
}

fun miFuncion(): Int {  // ERROR: función ya declarada
    return 2;
}

// Prueba Semántica 11: Función llamando a otra correctamente
fun multiplicar(a: Int, b: Int): Int {
    return a * b;
}

fun calcularArea(base: Int, altura: Int): Int {
    return multiplicar(base, altura);  // OK: multiplicar está declarada
}

// Prueba Semántica 12: Casos mixtos con funciones
fun casosMixtosFunciones() {
    val resultado1 = sumar(5, 10);           // OK
    val resultado2 = funcionInexistente2();  // ERROR: no declarada
    
    println(resultado1);  // OK
}