from lang import KEYWORDS_LIST, SYMBOLS_LIST, State


def determinar_estado(input_str: str) -> State:
    # Testar palavras e símbolos reservados
    if input_str in SYMBOLS_LIST:
        return State.SYMBOL
    if input_str in KEYWORDS_LIST:
        return State.KEYWORD

    # Testar letras e números
    if input_str.isalpha():
        return State.ALPHANUMERIC
    if input_str.isdigit():
        return State.NUMERIC

    # Pular espaços em branco
    elif input_str.isspace():
        return State.IDENTIFIER

    return State.INEXISTENT


# definir o tipo que será retornado da função abaixo
def ler_arquivo(arquivo: str) -> str:
    conteudo = ""
    with open("example_input.c", "r") as arquivo:
        conteudo = arquivo.read()
    return conteudo


def recortar_valor_numerico(palavra: str) -> (str, str):
    valor = ""
    for caractere in palavra:
        if caractere.isdigit():
            valor += caractere
        else:
            break
    resto = palavra[len(valor) :]
    return (valor, resto)


def recortar_valor_str(palavra: str) -> (str, str):
    valor = ""
    simbolo = None
    nalpha = None

    if comeca_com_simbolo(palavra):
        (simbolo, palavra) = recortar_simbolo(palavra)

    if not comeca_com_alpha(palavra):
        (nalpha, palavra) = recortar_nao_alpha(palavra)

    for caractere in palavra:
        if caractere.isalpha():
            valor += caractere
        else:
            break
    resto = palavra[len(valor) :]
    return (valor, resto, simbolo, nalpha)


def recortar_nao_alpha(palavra: str) -> (str, str):
    valor = ""
    for caractere in palavra:
        if not caractere.isalpha():
            valor += caractere
        else:
            break
    resto = palavra[len(valor) :]
    return (valor, resto)


def recortar_simbolo(palavra: str) -> (str, str):
    valor = ""
    for caractere in palavra:
        if caractere in SYMBOLS_LIST:
            valor += caractere
        else:
            break
    resto = palavra[len(valor) :]
    return (valor, resto)


def comeca_com_simbolo(palavra: str) -> bool:
    for simbolo in SYMBOLS_LIST:
        if palavra.startswith(simbolo):
            return True
    return False


def comeca_com_alpha(palavra: str) -> bool:
    for caractere in palavra:
        if caractere.isalpha():
            continue
        else:
            return False
    return True
