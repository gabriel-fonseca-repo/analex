from typing import List

from lang import State, Symbols, Token, TokenType
from util import (
    determinar_estado,
    eh_inicio_comentario,
    eh_palavra_chave,
    ler_arquivo,
    recortar_valor_numerico,
    recortar_valor_str,
    simbolo_multicaractere,
    str_valida,
)


def analisar_cada_caractere(
    palavra: str,
    eh_comentario: bool,
    comentario: str,
) -> List[Token]:
    PALAVRAS_TOKEN_LIST = []

    for indice, caractere in enumerate(palavra):
        if not eh_comentario:
            eh_comentario = eh_inicio_comentario(palavra, indice)

        if eh_comentario:
            comentario += caractere
            if comentario.endswith("*/"):
                PALAVRAS_TOKEN_LIST.append(Token(comentario, TokenType.COMMENT))
                comentario = ""
                eh_comentario = False
            continue

        estado_caractere = determinar_estado(caractere)

        if estado_caractere is State.NUMERIC:
            (numero, resto, simbolo) = recortar_valor_numerico(palavra)
            PALAVRAS_TOKEN_LIST.append(Token(numero, TokenType.NUM))
            if str_valida(simbolo):
                if simbolo_multicaractere(simbolo):
                    PALAVRAS_TOKEN_LIST.append(Token(simbolo, TokenType.SYMBOL))
                elif not palavra.startswith(simbolo):
                    PALAVRAS_TOKEN_LIST.extend(
                        [Token(tk_simbolo, TokenType.SYMBOL) for tk_simbolo in simbolo]
                    )
            (
                tokens,
                eh_comentario,
                comentario,
            ) = analisar_cada_caractere(resto, eh_comentario, comentario)
            PALAVRAS_TOKEN_LIST.extend(tokens)
            break

        if estado_caractere is State.ALPHABETIC:
            (str_alpha, resto, simbolo, nalpha) = recortar_valor_str(palavra)
            if str_valida(simbolo) and not palavra.startswith(simbolo):
                if simbolo_multicaractere(simbolo):
                    PALAVRAS_TOKEN_LIST.append(Token(simbolo, TokenType.SYMBOL))
                else:
                    PALAVRAS_TOKEN_LIST.extend(
                        [Token(tk_simbolo, TokenType.SYMBOL) for tk_simbolo in simbolo]
                    )
            if str_valida(nalpha):
                PALAVRAS_TOKEN_LIST.append(Token(nalpha, TokenType.ALPHA))
            if str_valida(str_alpha):
                if eh_palavra_chave(str_alpha):
                    PALAVRAS_TOKEN_LIST.append(Token(str_alpha, TokenType.KEYWORD))
                elif str_alpha.isalpha():
                    PALAVRAS_TOKEN_LIST.append(Token(str_alpha, TokenType.ALPHA))
                elif str_alpha.isdigit():
                    PALAVRAS_TOKEN_LIST.append(Token(str_alpha, TokenType.NUM))
                elif str_alpha.isalnum():
                    PALAVRAS_TOKEN_LIST.append(Token(str_alpha, TokenType.NONE))
            (
                tokens,
                eh_comentario,
                comentario,
            ) = analisar_cada_caractere(resto, eh_comentario, comentario)
            PALAVRAS_TOKEN_LIST.extend(tokens)
            break

        if estado_caractere is State.INEXISTENT:
            PALAVRAS_TOKEN_LIST.append(Token(caractere, TokenType.NONE))
            continue
        if estado_caractere is State.SYMBOL:
            PALAVRAS_TOKEN_LIST.append(Token(caractere, TokenType.SYMBOL))
            continue

        if estado_caractere is State.IDENTIFIER:
            continue

    return (PALAVRAS_TOKEN_LIST, eh_comentario, comentario)


def analisar_codigo_fonte(conteudo: str):
    global eh_comentario
    global comentario

    eh_comentario = False
    comentario = ""

    palavras = conteudo.split()
    TOKENS_LIST = []

    for palavra in palavras:
        if not eh_comentario:
            eh_comentario = palavra.startswith(Symbols.MULTI_LINE_COMMENT_START.value)

        if eh_comentario:
            comentario += palavra + " " if palavra != "*/" else palavra
            if comentario.endswith("*/"):
                TOKENS_LIST.append(Token(comentario, TokenType.COMMENT))
                comentario = ""
                eh_comentario = False
            continue

        estado_palavra = determinar_estado(palavra)

        if estado_palavra is State.IDENTIFIER:
            continue
        elif estado_palavra is State.ALPHABETIC:
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
        elif estado_palavra is State.ALPHANUMERIC:
            TOKENS_LIST.append(Token(palavra, TokenType.NONE))
            continue
        else:
            (
                tokens,
                eh_comentario,
                comentario,
            ) = analisar_cada_caractere(palavra, eh_comentario, comentario)
            TOKENS_LIST.extend(tokens)

    return TOKENS_LIST


conteudo = ler_arquivo("example_input.c")
# conteudo = "(A12345+(a1+22)*42)"
# conteudo = "int x = 42; /* Isso é um comentário */ y = x + 10; identificador123 a 1 B aleatoria else if while for return void 12345 /* Outro comentário */"
tokens: List[Token] = analisar_codigo_fonte(conteudo)

tokens_invalidos = [token for token in tokens if token.classe is TokenType.NONE]
tokens_validos = [token for token in tokens if token.classe is not TokenType.NONE]

tokens_validos_sort = sorted(tokens_validos, key=lambda token: token.classe.value)

print()
print("Tokens inválidos:")
for token in tokens_invalidos:
    print(f"{(token.classe.name + ':'):10s} {token.valor}")

print()

print("Tokens válidos:")
for token in tokens_validos_sort:
    print(f"{(token.classe.name + ':'):10s} {token.valor}")
