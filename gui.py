import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import pprint

# Importamos la función principal de tu backend
# Asegúrate de que analizador_sintactico.py esté en la misma carpeta
try:
    from analizador_sintactico import analyze_syntax
except ImportError as e:
    messagebox.showerror("Error Crítico", f"No se pudo importar el analizador:\n{e}\nAsegúrate de tener analizador_sintactico.py en la misma carpeta.")
    exit()

class CompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador Kotlin (Educativo) - Proyecto Final")
        self.root.geometry("1200x800")
        
        # Estilos
        style = ttk.Style()
        style.theme_use('clam')
        
        # --- BARRA SUPERIOR (Botones) ---
        toolbar = ttk.Frame(root, padding=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        btn_open = ttk.Button(toolbar, text="📂 Abrir Archivo", command=self.open_file)
        btn_open.pack(side=tk.LEFT, padx=5)
        
        btn_clear = ttk.Button(toolbar, text="🧹 Limpiar", command=self.clear_editor)
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Botón grande de compilación
        btn_run = ttk.Button(toolbar, text="▶ EJECUTAR ANÁLISIS", command=self.run_compiler)
        btn_run.pack(side=tk.LEFT, padx=20)
        
        lbl_status = ttk.Label(toolbar, text="Listo para compilar.")
        self.lbl_status = lbl_status
        lbl_status.pack(side=tk.RIGHT, padx=10)

        # --- CONTENIDO PRINCIPAL (Panel Dividido) ---
        paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=5, bg="#dcdcdc")
        paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 1. LADO IZQUIERDO: Editor de Código
        frame_editor = ttk.LabelFrame(paned_window, text=" Editor de Código (Kotlin) ", padding=5)
        paned_window.add(frame_editor)
        
        self.txt_code = scrolledtext.ScrolledText(frame_editor, width=50, height=30, font=("Consolas", 11))
        self.txt_code.pack(fill=tk.BOTH, expand=True)
        
        # 2. LADO DERECHO: Resultados (Pestañas)
        frame_results = ttk.LabelFrame(paned_window, text=" Resultados del Análisis ", padding=5)
        paned_window.add(frame_results)
        
        self.notebook = ttk.Notebook(frame_results)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # --- Pestaña 1: Errores (Prioridad) ---
        self.tab_errors = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_errors, text="❌ Errores")
        self.txt_errors = scrolledtext.ScrolledText(self.tab_errors, font=("Consolas", 10), fg="red")
        self.txt_errors.pack(fill=tk.BOTH, expand=True)
        
        # --- Pestaña 2: Tokens (Léxico) ---
        self.tab_tokens = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tokens, text="🎫 Tokens")
        
        # Treeview para tokens
        cols = ("Tipo", "Valor", "Línea", "Col")
        self.tree_tokens = ttk.Treeview(self.tab_tokens, columns=cols, show='headings')
        for col in cols:
            self.tree_tokens.heading(col, text=col)
            self.tree_tokens.column(col, width=80 if col != "Valor" else 150)
            
        scrollbar_tokens = ttk.Scrollbar(self.tab_tokens, orient="vertical", command=self.tree_tokens.yview)
        self.tree_tokens.configure(yscroll=scrollbar_tokens.set)
        
        self.tree_tokens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tokens.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Pestaña 3: Árbol AST (Sintáctico) ---
        self.tab_ast = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ast, text="🌳 AST")
        self.txt_ast = scrolledtext.ScrolledText(self.tab_ast, font=("Consolas", 10))
        self.txt_ast.pack(fill=tk.BOTH, expand=True)

        # --- Pestaña 4: Tablas de Símbolos (Semántico) ---
        self.tab_symbols = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_symbols, text="📚 Tablas de Símbolos")
        self.txt_symbols = scrolledtext.ScrolledText(self.tab_symbols, font=("Consolas", 10))
        self.txt_symbols.pack(fill=tk.BOTH, expand=True)

    def open_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Kotlin Files", "*.kt"), ("All Files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.txt_code.delete("1.0", tk.END)
                self.txt_code.insert("1.0", content)
                self.lbl_status.config(text=f"Archivo cargado: {filepath.split('/')[-1]}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    def clear_editor(self):
        self.txt_code.delete("1.0", tk.END)
        
    def clear_results(self):
        self.txt_errors.delete("1.0", tk.END)
        self.txt_ast.delete("1.0", tk.END)
        self.txt_symbols.delete("1.0", tk.END)
        for item in self.tree_tokens.get_children():
            self.tree_tokens.delete(item)

    def run_compiler(self):
        # 1. Obtener código
        code = self.txt_code.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Advertencia", "El editor está vacío.")
            return
            
        self.clear_results()
        
        # 2. Ejecutar análisis (Llamada al Backend)
        try:
            results = analyze_syntax(code)
        except Exception as e:
            self.txt_errors.insert(tk.END, f"[ERROR INTERNO CRÍTICO]: {str(e)}\n")
            return

        # 3. Mostrar Tokens
        tokens = results.get('tokens', [])
        for t in tokens:
            self.tree_tokens.insert("", tk.END, values=(t['type'], t['value'], t['line'], t['col']))
            
        # 4. Mostrar Errores (Consolidado)
        lex_err = results.get('lex_errors', [])
        syn_err = results.get('syn_errors', [])
        sem_err = results.get('sem_errors', [])
        
        has_errors = False
        
        if lex_err:
            self.txt_errors.insert(tk.END, "--- ERRORES LÉXICOS ---\n")
            for e in lex_err: self.txt_errors.insert(tk.END, f"{e}\n")
            has_errors = True
            
        if syn_err:
            self.txt_errors.insert(tk.END, "\n--- ERRORES SINTÁCTICOS ---\n")
            for e in syn_err: self.txt_errors.insert(tk.END, f"{e}\n")
            has_errors = True

        if sem_err:
            self.txt_errors.insert(tk.END, "\n--- ERRORES SEMÁNTICOS ---\n")
            for e in sem_err: self.txt_errors.insert(tk.END, f"{e}\n")
            has_errors = True
            
        if not has_errors:
            self.txt_errors.config(fg="green")
            self.txt_errors.insert(tk.END, "✅ ANÁLISIS EXITOSO: No se encontraron errores.")
        else:
            self.txt_errors.config(fg="red")
            # Auto-seleccionar pestaña de errores si hay fallos
            self.notebook.select(self.tab_errors)

        # 5. Mostrar AST (Formateado bonito)
        ast = results.get('ast', None)
        if ast:
            formatted_ast = pprint.pformat(ast, indent=2, width=120)
            self.txt_ast.insert(tk.END, formatted_ast)
        else:
            self.txt_ast.insert(tk.END, "No se generó AST (probablemente hubo errores de sintaxis).")

        # 6. Mostrar Tablas
        sym_table = results.get('symbol_table', {})
        func_table = results.get('function_table', {})
        class_table = results.get('class_table', {})
        
        self.txt_symbols.insert(tk.END, "=== TABLA DE VARIABLES ===\n")
        self.txt_symbols.insert(tk.END, pprint.pformat(sym_table, indent=2) + "\n\n")
        
        self.txt_symbols.insert(tk.END, "=== TABLA DE FUNCIONES ===\n")
        self.txt_symbols.insert(tk.END, pprint.pformat(func_table, indent=2) + "\n\n")
        
        self.txt_symbols.insert(tk.END, "=== TABLA DE CLASES ===\n")
        self.txt_symbols.insert(tk.END, pprint.pformat(class_table, indent=2))

        self.lbl_status.config(text="Análisis completado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerApp(root)
    root.mainloop()