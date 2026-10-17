import tkinter as tk
from tkinter import messagebox
from lexico import ValidadorLexico, Tokenizador
from automata import EvaluadorAFDSQL

class AplicacionSQL:
    def __init__(self, root):
        self.root = root
        self.root.title("Validador Sintáctico de Consultas SQL")
        self.root.geometry("920x580")
        self.root.config(bg="#f4f6f9")

        self.validador = ValidadorLexico()
        self.tokenizador = Tokenizador()
        self.evaluador = EvaluadorAFDSQL()

        tk.Label(root, text="Autómatas y Lenguajes Formales - Analizador SQL", 
                 bg="#f4f6f9", fg="#2c3e50", font=("Arial", 13, "bold")).pack(pady=15)

        tk.Label(root, text="Ingrese la consulta Select a evaluar:", 
                 bg="#f4f6f9", font=("Arial", 10)).pack(anchor="w", padx=35)
        
        self.entry_sql = tk.Entry(root, width=65, font=("Consolas", 10))
        self.entry_sql.pack(padx=35, pady=5)
        self.entry_sql.insert(0, "SELECT * FROM tabla;")

        btn_evaluar = tk.Button(root, text="Evaluar Sintaxis", bg="#27ae60", fg="white", 
                                font=("Arial", 10, "bold"), padx=10, pady=5, command=self.evaluar)
        btn_evaluar.pack(pady=15)

        self.lbl_resultado = tk.Label(root, text=" Listo para evaluar ", 
                                      bg="#e2e8f0", fg="#334155", font=("Arial", 10, "bold"), 
                                      width=100, height=6, relief="groove", justify="center")
        self.lbl_resultado.pack(pady=10)

    def evaluar(self):
        sql = self.entry_sql.get().strip()
        if not sql:
            messagebox.showwarning("Advertencia", "Por favor ingrese una consulta SQL.")
            return

        es_valido, msg_lexico = self.validador.validar_cadena(sql)
        if not es_valido:
            self.lbl_resultado.config(text=f"✗ Sintaxis rechazada\nError Léxico: {msg_lexico}", bg="#f8d7da", fg="#842029")
            return

        tokens = self.tokenizador.tokenizar(sql)

        resultado, mensaje = self.evaluador.evaluar(tokens)

        if resultado == "Sintaxis válida":
            self.lbl_resultado.config(text=f"✓ {resultado}\n{mensaje}", bg="#d1e7dd", fg="#0f5132")
        else:
            self.lbl_resultado.config(text=f"✗ {resultado}\n{mensaje}", bg="#f8d7da", fg="#842029")

if __name__ == "__main__":
    ventana = tk.Tk()
    app = AplicacionSQL(ventana)
    ventana.mainloop()