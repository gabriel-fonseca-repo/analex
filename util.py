from typing import List
from lang import KEYWORDS_LIST, SYMBOLS_LIST, State, Symbols
import re


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


def eh_inicio_comentario(palavra: str, indice: int) -> bool:
    if palavra == Symbols.MULTI_LINE_COMMENT_START:
        return True
    caractere = palavra[indice]
    if caractere == Symbols.DIVISION.value:
        if indice + 1 < len(palavra):
            return palavra[indice + 1] == Symbols.MULTIPLICATION.value
    return False


def ler_arquivo(arquivo: str) -> str:
    conteudo = ""
    with open(arquivo, "r") as arquivo:
        conteudo = arquivo.read()
    return conteudo


def recortar_valor_numerico(palavra: str) -> (str, str):
    valor = ""
    simbolo = None

    if comeca_com_simbolo(palavra):
        (simbolo, palavra) = recortar_simbolo(palavra)

    for caractere in palavra:
        if caractere.isdigit():
            valor += caractere
        else:
            break
    resto = palavra[len(valor) :]
    return (valor, resto, simbolo)


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


def simbolo_multicaractere(simbolo: str) -> bool:
    return simbolo in SYMBOLS_LIST and len(simbolo) > 1


def str_valida(str_value: str) -> bool:
    return str_value is not None and str_value != ""


def str_contem_palavra_chave(str_value: str) -> bool:
    for palavra_chave in KEYWORDS_LIST:
        if palavra_chave in str_value:
            return True
    return False


def extrair_palavras_chave(str_value: str):
    regex = "|".join(re.escape(palavra) for palavra in KEYWORDS_LIST)
    palavras_chave_encontradas = re.findall(regex, str_value)
    partes_string = re.split(regex, str_value)
    partes_string = [parte for parte in partes_string if parte]
    return (palavras_chave_encontradas, partes_string)
