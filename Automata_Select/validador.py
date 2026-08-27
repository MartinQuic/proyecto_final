class ValidadorLexico:
    def __init__(self):
        self.alfabeto = set()

    def cargar_alfabeto(self, entrada_alfabeto):
        entrada_limpia = entrada_alfabeto.replace(',', ' ')
        simbolos = entrada_limpia.split()
        self.alfabeto = set(simbolos)

    def validar_cadena(self, cadena):
        if not self.alfabeto:
            return False, "El alfabeto esta vacio. Ingresa un alfabeto primero."

        for simbolo in cadena:
            if simbolo == ' ' and ' ' not in self.alfabeto:
                continue

            if simbolo not in self.alfabeto:
                return False, f"Error: El simbolo '{simbolo}' no pertenece al alfabeto"

        return True, "Estado: Valido"


# if __name__ == "__main__":
  #  validador = ValidadorLexico()
  #  validador.cargar_alfabeto("0, 1")
  #  es_valido, msg = validador.validar_cadena("01001")

  #  es_valido, msg = validador.validar_cadena("01A01")
  #  print("Input Cadena 2: '01A01' ->", msg)