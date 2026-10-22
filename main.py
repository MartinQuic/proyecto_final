"""Punto de entrada."""
import tkinter as tk
from interfaz.interfaz import Aplicacion

if __name__ == '__main__':
    ventana=tk.Tk()
    Aplicacion(ventana)
    ventana.mainloop()



