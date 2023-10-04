from typing import List
from lang import State, Token, TokenType
from util import (
    determinar_estado,
    ler_arquivo,
    recortar_valor_numerico,
    recortar_valor_str,
)


def analisar_cada_caractere(palavra: str) -> List[Token]:
    PALAVRAS_TOKEN_LIST = []

    for caractere in palavra:
        estado_caractere = determinar_estado(caractere)

        if estado_caractere is State.INEXISTENT:
            PALAVRAS_TOKEN_LIST.append(Token(caractere, TokenType.NONE))
            continue
        if estado_caractere is State.SYMBOL:
            PALAVRAS_TOKEN_LIST.append(Token(caractere, TokenType.SYMBOL))
            continue

        if estado_caractere is State.NUMERIC:
            (numero, resto) = recortar_valor_numerico(palavra)
            PALAVRAS_TOKEN_LIST.append(Token(numero, TokenType.NUM))
            PALAVRAS_TOKEN_LIST.extend(analisar_cada_caractere(resto))
            break
        if estado_caractere is State.ALPHANUMERIC:
            (str_alpha, resto, simbolo, nalpha) = recortar_valor_str(palavra)
            PALAVRAS_TOKEN_LIST.append(Token(str_alpha, TokenType.ALPHA))
            if simbolo is not None and simbolo != "":
                PALAVRAS_TOKEN_LIST.append(Token(simbolo, TokenType.SYMBOL))
            if nalpha is not None and nalpha != "":
                PALAVRAS_TOKEN_LIST.append(Token(nalpha, TokenType.ALPHA))
            PALAVRAS_TOKEN_LIST.extend(analisar_cada_caractere(resto))
            break

        if estado_caractere is State.IDENTIFIER:
            continue

    return PALAVRAS_TOKEN_LIST


def analisar_codigo_fonte(conteudo: str):
    palavras = conteudo.split()
    TOKENS_LIST = []

    for palavra in palavras:
        estado_palavra = determinar_estado(palavra)

        if estado_palavra is State.IDENTIFIER:
            continue
        elif estado_palavra is State.ALPHANUMERIC:
            TOKENS_LIST.append(Token(palavra, TokenType.ALPHA))
            continue
        elif estado_palavra is State.NUMERIC:
            TOKENS_LIST.append(Token(palavra, TokenType.NUM))
            continue
        elif estado_palavra is State.SYMBOL:
            TOKENS_LIST.append(Token(palavra, TokenType.SYMBOL))
            continue
        elif estado_palavra is State.KEYWORD:
            TOKENS_LIST.append(Token(palavra, TokenType.KEYWORD))
            continue
        else:
            TOKENS_LIST.extend(analisar_cada_caractere(palavra))

    return TOKENS_LIST


conteudo = ler_arquivo("example_input.c")
tokens: List[Token] = analisar_codigo_fonte(conteudo)

tokens_invalidos = [token for token in tokens if token.classe is TokenType.NONE]
tokens_validos = [token for token in tokens if token.classe is not TokenType.NONE]

tokens_validos_sort = sorted(tokens_validos, key=lambda token: token.classe.value)

print("Tokens inválidos:")
for token in tokens_invalidos:
    print(token)

print()

print("Tokens válidos:")
for token in tokens_validos_sort:
    print(token)
