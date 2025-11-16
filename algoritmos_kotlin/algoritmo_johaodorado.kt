// Prueba 1: Clases básicas
class Persona(val nombre: String, val edad: Int) {
    fun saludar() {
        println("Hola, soy " + nombre)
        return
    }
    
    fun obtenerEdad(): Int {
        return this.edad
    }
}

class Estudiante(val matricula: String, val carrera: String) {
    fun estudiar() {
        println("Estudiando...")
        return
    }
}

// Prueba 2: Object declarations
object Configuracion {
    val version = "1.0.0"
    val puerto = 8080
    
    fun inicializar() {
        println("Configuración inicializada")
        return
    }
}

object Constantes {
    val PI = 3.14159
    val E = 2.71828
}

// Prueba 3: Uso de this
class Rectangulo(val ancho: Int, val alto: Int) {
    fun area(): Int {
        return this.ancho * this.alto
    }
    
    fun perimetro(): Int {
        return 2 * (this.ancho + this.alto)
    }
}

// Prueba 4: Literales numéricos (enteros y decimales)
fun literalesNumericos() {
    val entero1 = 42
    val entero2 = 0
    val entero3 = 999999
    
    val decimal1 = 3.14
    val decimal2 = 2.718
    val decimal3 = 0.5
    val decimal4 = 123.456
    
    return
}

// Prueba 5: Literales de caracteres y strings
fun literalesTexto() {
    val caracter1 = 'A'
    val caracter2 = 'z'
    val caracter3 = '0'
    
    val texto1 = "Hola mundo"
    val texto2 = "Kotlin es genial"
    val texto3 = ""
    val texto4 = "Texto con espacios"
    
    return
}

// Prueba 6: Arrays y listas con delimitadores
fun estructurasDatos() {
    val numeros = [1, 2, 3, 4, 5]
    val nombres = ["Ana", "Bob", "Carlos"]
    val vacio = []
    val mixto = [1, 2, 3]
    
    return
}



// Reglas sintácticas implementadas:
// - Definición de clases
// ============================================
// PRUEBA 1: CLASES BÁSICAS
// ============================================

// Clase simple sin propiedades
class VaciaClass() {
}

// Clase con propiedades en constructor
class Persona(val nombre: String, val edad: Int) {
}

class Estudiante(val matricula: String, var carrera: String) {
}

class Producto(val codigo: Int, val nombre: String, var precio: Double) {
}

// Clase con múltiples propiedades
class Empleado(
    val id: Int,
    val nombre: String,
    val apellido: String,
    var salario: Double,
    var activo: Boolean
) {
}

// ============================================
// PRUEBA 2: PROPIEDADES DE CLASE
// ============================================

class Configuracion() {
    // Propiedades inmutables
    val version = "1.0.0";
    val nombre = "MiApp";
    val puerto = 8080;
    
    // Propiedades mutables
    var timeout = 30;
    var maxConexiones = 100;
    var debug = true;
}

class Contador() {
    var valor = 0;
    var incremento = 1;
    val maximo = 100;
}

// Propiedades con tipos explícitos
class DatosTipados() {
    val entero: Int = 42;
    val decimal: Double = 3.14;
    val texto: String = "Hola";
    val booleano: Boolean = true;
}

// ============================================
// PRUEBA 3: MÉTODOS DE CLASE
// ============================================

class Calculadora() {
    // Método simple
    fun saludar() {
        println("Hola desde Calculadora");
    }
    
    // Método con parámetros
    fun sumar(a: Int, b: Int): Int {
        return a + b;
    }
    
    fun restar(x: Int, y: Int): Int {
        return x - y;
    }
    
    // Método con lógica
    fun dividir(numerador: Int, denominador: Int): Int {
        if (denominador != 0) {
            return numerador / denominador;
        } else {
            return 0;
        }
    }
}

class Rectangulo(val ancho: Int, val alto: Int) {
    fun area(): Int {
        return ancho * alto;
    }
    
    fun perimetro(): Int {
        return 2 * (ancho + alto);
    }
    
    fun esCuadrado(): Boolean {
        return ancho == alto;
    }
}

// ============================================
// PRUEBA 4: USO DE THIS
// ============================================

class Punto(val x: Int, val y: Int) {
    fun distanciaAlOrigen(): Double {
        val cuadradoX = this.x * this.x;
        val cuadradoY = this.y * this.y;
        val suma = cuadradoX + cuadradoY;
        return suma;
    }
    
    fun mover(deltaX: Int, deltaY: Int): Punto {
        val nuevoX = this.x + deltaX;
        val nuevoY = this.y + deltaY;
        return Punto(nuevoX, nuevoY);
    }
}

class CuentaBancaria(val numero: String, var saldo: Double) {
    fun depositar(monto: Double) {
        this.saldo = this.saldo + monto;
        println("Nuevo saldo:");
        println(this.saldo);
    }
    
    fun retirar(monto: Double): Boolean {
        if (this.saldo >= monto) {
            this.saldo = this.saldo - monto;
            return true;
        } else {
            return false;
        }
    }
    
    fun obtenerSaldo(): Double {
        return this.saldo;
    }
}

// ============================================
// PRUEBA 5: OBJECT DECLARATIONS (Singleton)
// ============================================

// Object simple
object ConfiguracionGlobal {
    val appName = "MiAplicacion";
    val version = "2.0.0";
    val puerto = 3000;
}

// Object con propiedades mutables
object Contador {
    var total = 0;
    var incremento = 1;
    
    fun incrementar() {
        total = total + incremento;
    }
    
    fun obtenerTotal(): Int {
        return total;
    }
}

// Object con constantes
object Constantes {
    val PI = 3.14159;
    val E = 2.71828;
    val MAX_INT = 2147483647;
    val MIN_INT = -2147483648;
}

// Object con funciones utilitarias
object Matematicas {
    fun cuadrado(n: Int): Int {
        return n * n;
    }
    
    fun cubo(n: Int): Int {
        return n * n * n;
    }
    
    fun absoluto(n: Int): Int {
        if (n < 0) {
            return -n;
        } else {
            return n;
        }
    }
}

// ============================================
// PRUEBA 6: ACCESO A MIEMBROS CON PUNTO
// ============================================

fun usarClases() {
    // Crear instancias
    val persona = Persona("Ana", 25);
    val rect = Rectangulo(10, 5);
    val punto = Punto(3, 4);
    val cuenta = CuentaBancaria("12345", 1000.0);
    
    // Acceder a propiedades
    println(persona.nombre);
    println(persona.edad);
    println(rect.ancho);
    println(rect.alto);
    
    // Llamar métodos
    val area = rect.area();
    val perimetro = rect.perimetro();
    val esCuadrado = rect.esCuadrado();
    
    cuenta.depositar(500.0);
    val retiro = cuenta.retirar(200.0);
    val saldo = cuenta.obtenerSaldo();
    
    // Acceder a objects
    println(ConfiguracionGlobal.appName);
    println(Constantes.PI);
    
    Contador.incrementar();
    val total = Contador.obtenerTotal();
    
    val cuad = Matematicas.cuadrado(5);
    val cubito = Matematicas.cubo(3);
    
    return;
}

// ============================================
// PRUEBA 7: CLASES CON MÉTODOS COMPLEJOS
// ============================================

class ListaNumeros(val capacidad: Int) {
    var elementos = [];
    var tamano = 0;

}

