import tkinter as tk
from tkinter import messagebox
from validador import ValidadorLexico

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Fase 1: Validador Léxico de Alfabetos")
        self.root.geometry("450x350")
        self.root.config(bg="#f0f0f0")

        self.root.attributes('-topmost', True)

        self.validador = ValidadorLexico()

        tk.Label(root, text="1. Define el Alfabeto Σ (separado por comas):", 
                 bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.entry_alfabeto = tk.Entry(root, width=45, font=("Arial", 10))
        self.entry_alfabeto.pack(padx=20)
        self.entry_alfabeto.insert(0, "0, 1")

        btn_cargar = tk.Button(root, text="Cargar Alfabeto", bg="#4CAF50", fg="white", 
                               font=("Arial", 9, "bold"), command=self.cargar_alfabeto)
        btn_cargar.pack(pady=5)

        tk.Label(root, text="2. Ingrese Cadena a Evaluar:", 
                 bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(15, 5))

        self.entry_cadena = tk.Entry(root, width=45, font=("Arial", 10))
        self.entry_cadena.pack(padx=20)

        btn_evaluar = tk.Button(root, text="Evaluar Cadena", bg="#2196F3", fg="white", 
                                font=("Arial", 9, "bold"), command=self.evaluar_cadena)
        btn_evaluar.pack(pady=10)

        self.lbl_resultado = tk.Label(root, text="[ Estado: Esperando Entrada ]", 
                                      bg="#e0e0e0", fg="black", font=("Arial", 11, "bold"), 
                                      width=38, height=2, relief="groove")
        self.lbl_resultado.pack(pady=10)

    def cargar_alfabeto(self):
        texto = self.entry_alfabeto.get()
        if not texto.strip():
            messagebox.showwarning("Advertencia", "Por favor ingresa un alfabeto válido.")
            return
        
        self.validador.cargar_alfabeto(texto)
        messagebox.showinfo("Éxito", f"Alfabeto cargado: {self.validador.alfabeto}")

    def evaluar_cadena(self):
        cadena = self.entry_cadena.get()
        es_valida, mensaje = self.validador.validar_cadena(cadena)

        if es_valida:
            self.lbl_resultado.config(text=f"✓ {mensaje}", bg="#C8E6C9", fg="#2E7D32")
        else:
            self.lbl_resultado.config(text=f"✗ {mensaje}", bg="#FFCDD2", fg="#C62828")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = VentanaPrincipal(ventana)
    ventana.lift()
    ventana.mainloop()