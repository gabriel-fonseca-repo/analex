class Token:
    classe = ""
    valor = ""

    def __init__(self, valor, classe):
        self.valor = valor
        self.classe = classe


estado = 1
cadeia = "A2333-jk(68768687687687687687686876876"

global pos
global lista

pos = 0
lista = []
valor = ""
i = 0  # ponteiro inicial

while i < len(cadeia):
    if estado == 1:  # identificador
        if (
            cadeia[i : i + 1] == "("
            or cadeia[i : i + 1] == ")"
            or cadeia[i : i + 1] == "+"
            or cadeia[i : i + 1] == "*"
            or cadeia[i : i + 1] == "/"
            or cadeia[i : i + 1] == "-"
        ):
            estado = 2
            continue
        elif cadeia[i : i + 1].isdigit():
            estado = 3
            continue
        elif cadeia[i : i + 1].isalpha() or cadeia[i : i + 1].isdigit():
            while cadeia[i : i + 1].isalpha() or cadeia[i : i + 1].isdigit():
                valor = valor + cadeia[i : i + 1]
                Token.classe = "ide"
                Token.valor = valor
                i = i + 1
        else:
            estado = 99
            continue
    elif estado == 2:  # simbolo
        Token.valor = cadeia[i : i + 1]
        Token.classe = "sim"
    elif estado == 3:  # numero
        while cadeia[i : i + 1].isdigit():
            valor = valor + cadeia[i : i + 1]
            Token.classe = "num"
            Token.valor = valor
            i = i + 1
    elif estado == 99:  # fora da gramática
        Token.valor = cadeia[i : i + 1]
        Token.classe = "out"
        print(Token.valor)
        print("Símbolo fora da gramática! Análise léxica não OK!")
        raise SystemExit
    print(Token.classe + " " + Token.valor)
    tok = Token(Token.valor, Token.classe)
    lista.append(tok)
    valor = ""
    estado = 1

    if Token.classe == "sim" or Token.classe == "out":
        i = i + 1

print("análise léxica OK!")
