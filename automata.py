class EvaluadorAFDSQL:
    def __init__(self):
        pass

    def evaluar(self, tokens):
        if not tokens:
            return "Sintaxis rechazada", "La consulta está vacía."
        
        if tokens[-1] != ";":
            return "Sintaxis rechazada", "Error sintáctico: La consulta debe finalizar con ';'."

        tokens_cuerpo = tokens[:-1]
        n = len(tokens_cuerpo)
        i = 0

        if i >= n or tokens_cuerpo[i] != "SELECT":
            return "Sintaxis rechazada", "Toda consulta debe iniciar con la palabra clave 'SELECT'."
        i += 1

        if i < n and tokens_cuerpo[i] == "*":
            i += 1
        else:
            mantiene_columnas = True
            while mantiene_columnas and i < n:
                if tokens_cuerpo[i] == "COUNT":
                    if i + 3 < n and tokens_cuerpo[i+1] == "(" and tokens_cuerpo[i+2] in ["ID", "*", "NUM"] and tokens_cuerpo[i+3] == ")":
                        i += 4
                    else:
                        return "Sintaxis rechazada", "Sintaxis incorrecta en la función COUNT(). Revisa los paréntesis o el argumento."
                elif tokens_cuerpo[i] == "ID":
                    i += 1
                else:
                    return "Sintaxis rechazada", f"Elemento no reconocido en SELECT: '{tokens_cuerpo[i]}'."
                
                if i < n and tokens_cuerpo[i] == ",":
                    i += 1
                    if i < n and tokens_cuerpo[i] == "FROM":
                        return "Sintaxis rechazada", "Error sintáctico: Coma sobrante antes de la cláusula FROM."
                else:
                    mantiene_columnas = False

        if i >= n or tokens_cuerpo[i] != "FROM":
            return "Sintaxis rechazada", "Se esperaba la cláusula 'FROM' (revisa si te faltó una coma ',' en el SELECT o si está mal escrita)."
        i += 1

        if i >= n or tokens_cuerpo[i] != "ID":
            return "Sintaxis rechazada", "Se esperaba el nombre de una tabla válido después de 'FROM'."
        i += 1

        if i < n and tokens_cuerpo[i] == "ID":
            i += 1

        if i < n and tokens_cuerpo[i] in ["INNER", "LEFT"]:
            tipo_join = tokens_cuerpo[i]
            i += 1
            if i >= n or tokens_cuerpo[i] != "JOIN":
                return "Sintaxis rechazada", f"Se esperaba la palabra 'JOIN' después de '{tipo_join}' (revisa si está bien escrito)."
            i += 1
            
            if i >= n or tokens_cuerpo[i] != "ID":
                return "Sintaxis rechazada", "Se esperaba el nombre de la tabla a unificar en JOIN."
            i += 1

            if i < n and tokens_cuerpo[i] == "ID":
                i += 1

            if i >= n or tokens_cuerpo[i] != "ON":
                return "Sintaxis rechazada", "Se esperaba la cláusula 'ON' para especificar la condición de unificación del JOIN."
            i += 1

            if i + 2 < n and tokens_cuerpo[i] == "ID" and tokens_cuerpo[i+1] == "=" and tokens_cuerpo[i+2] == "ID":
                i += 3
            else:
                return "Sintaxis rechazada", "Error en la cláusula JOIN: la condición relacional ON está mal escrita o incompleta."

        if i < n and tokens_cuerpo[i] == "WHERE":
            i += 1
            if i + 2 < n and tokens_cuerpo[i] == "ID" and tokens_cuerpo[i+1] in [">", "<", "=", ">=", "<=", "!="] and tokens_cuerpo[i+2] in ["ID", "NUM"]:
                i += 3
            else:
                return "Sintaxis rechazada", "Condición de filtrado WHERE inválida o mal escrita."

        if i < n and tokens_cuerpo[i] == "GROUP":
            i += 1
            if i >= n or tokens_cuerpo[i] != "BY":
                return "Sintaxis rechazada", "Se esperaba 'BY' después de 'GROUP' (comprueba si falta un espacio o si está mal escrito)."
            i += 1
            if i >= n or tokens_cuerpo[i] != "ID":
                return "Sintaxis rechazada", "Se esperaba el nombre de una columna para la agrupación en 'GROUP BY'."
            i += 1

        if i < n and tokens_cuerpo[i] == "HAVING":
            i += 1
            if i + 5 < n and tokens_cuerpo[i] == "COUNT" and tokens_cuerpo[i+1] == "(" and tokens_cuerpo[i+2] in ["ID", "*", "NUM"] and tokens_cuerpo[i+3] == ")" and tokens_cuerpo[i+4] in [">", "<", "=", ">=", "<=", "!="] and tokens_cuerpo[i+5] in ["NUM", "ID"]:
                i += 6
            elif i + 2 < n and tokens_cuerpo[i] == "ID" and tokens_cuerpo[i+1] in [">", "<", "=", ">=", "<=", "!="] and tokens_cuerpo[i+2] in ["NUM", "ID"]:
                i += 3
            else:
                return "Sintaxis rechazada", "Estructura o condición inválida dentro de la cláusula 'HAVING'."

        if i < n and tokens_cuerpo[i] == "ORDER":
            i += 1
            if i >= n or tokens_cuerpo[i] != "BY":
                return "Sintaxis rechazada", "Se esperaba 'BY' después de 'ORDER' (comprueba si falta un espacio o si está mal escrito)."
            i += 1
            if i >= n or tokens_cuerpo[i] != "ID":
                return "Sintaxis rechazada", "Se esperaba una columna para ordenar en 'ORDER BY'."
            i += 1
            
            if i < n and tokens_cuerpo[i] in ["ASC", "DESC"]:
                i += 1

        if i == n:
            return "Sintaxis válida", "La consulta cumple con la sintaxis SQL requerida."
        else:
            return "Sintaxis rechazada", f"Estructura sintáctica no reconocida a partir del token o palabra '{tokens_cuerpo[i]}'."