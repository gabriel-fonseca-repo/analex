import re


def extrair_palavras_chave(input_string, lista_palavras_chave):
    # Crie uma expressão regular com todas as palavras-chave separadas por "|"
    regex = "|".join(re.escape(palavra) for palavra in lista_palavras_chave)

    # Use a expressão regular para encontrar todas as palavras-chave na string de entrada
    palavras_chave_encontradas = re.findall(regex, input_string)

    # Use a expressão regular para dividir a string de entrada nas palavras-chave
    partes_string = re.split(regex, input_string)

    # Remova strings vazias da lista de partes
    partes_string = [parte for parte in partes_string if parte]

    return palavras_chave_encontradas, partes_string


# Exemplo de uso:
input_string = "returnwhi213elsewdkleifvoid"
lista_palavras_chave = [
    "if",
    "else",
    "while",
    "int",
    "return",
    "void",
]

palavras_chave_encontradas, partes_string = extrair_palavras_chave(
    input_string, lista_palavras_chave
)

print("Palavras-chave encontradas:", palavras_chave_encontradas)
print("String original sem as palavras-chave:", partes_string)
