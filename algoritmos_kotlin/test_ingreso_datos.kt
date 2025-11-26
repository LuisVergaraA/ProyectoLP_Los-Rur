// Prueba de ingreso de datos por teclado
// Para verificar el cumplimiento del requisito

// Prueba 1: Ingreso simple
fun pedirNombre() {
    println("Ingresa tu nombre:");
    val nombre = readln();
    println("Hola ");
    println(nombre);
    return;
}

// Prueba 2: Ingreso de número
fun pedirEdad() {
    println("Ingresa tu edad:");
    val edad = readln();
    println("Tienes ");
    println(edad);
    println(" años");
    return;
}

// Prueba 3: Múltiples ingresos
fun formulario() {
    println("=== FORMULARIO ===");
    
    println("Nombre:");
    val nombre = readln();
    
    println("Apellido:");
    val apellido = readln();
    
    println("Ciudad:");
    val ciudad = readln();
    
    println("=== RESUMEN ===");
    println(nombre);
    println(apellido);
    println(ciudad);
    
    return;
}

// Prueba 4: Ingreso con validación
fun ingresoConValidacion() {
    println("Ingresa un número:");
    val numero = readln();
    
    if (numero != null) {
        println("Número ingresado: ");
        println(numero);
    } else {
        println("No ingresaste nada");
    }
    
    return;
}

// Prueba 5: Uso en cálculos (asumiendo conversión manual)
fun calculadora() {
    println("Primer número:");
    val num1 = readln();
    
    println("Segundo número:");
    val num2 = readln();
    
    println("Resultado:");
    println(num1);
    println(" + ");
    println(num2);
    
    return;
}