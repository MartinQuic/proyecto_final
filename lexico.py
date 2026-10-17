import string
import re

class ValidadorLexico:
    def __init__(self):
        letras_y_digitos = string.ascii_letters + string.digits
        simbolos_especiales = " ,;()*=<>_.-"
        self.alfabeto = set(letras_y_digitos + simbolos_especiales)

    def validar_cadena(self, cadena):
        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                return False, f"El símbolo '{simbolo}' no pertenece al alfabeto."
        return True, "Símbolos válidos."

class Tokenizador:
    def __init__(self):
        self.palabras_reservadas = {
            "SELECT", "FROM", "WHERE", "GROUP", "BY", "HAVING", 
            "ORDER", "ASC", "DESC", "JOIN", "INNER", "LEFT", "ON", "COUNT"
        }

    def tokenizar(self, consulta_sql):
        patron = r"\w+\.\w+|>=|<=|!=|[=><,;*()]|\w+|\'[^\']*\'"
        lexemas = re.findall(patron, consulta_sql)
        
        tokens = []
        for lexema in lexemas:
            lexema_upper = lexema.upper()
            
            if lexema_upper in self.palabras_reservadas:
                tokens.append(lexema_upper)
            elif lexema in [",", ";", "*", "=", ">", "<", "(", ")"]:
                tokens.append(lexema)
            elif lexema.isdigit():
                tokens.append("NUM")
            elif re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)?$", lexema):
                tokens.append("ID")
            else:
                tokens.append("DESCONOCIDO")

        return tokens