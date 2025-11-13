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
