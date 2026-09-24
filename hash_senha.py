"""
Geração do hash da senha (SHA-256 padrão do trabalho).
"""

import hashlib


# ------------------------------------------------------
# FUNÇÃO DE HASH (SHA-256 padrão do trabalho)
# ------------------------------------------------------

def gerar_hash(senha, algoritmo="sha256"):
    """
    Função pra receber a senha pura e guardar o hash do algoritmo selecionado.

    Algoritmo padrão: SHA-256 (padrão).
    Mas a função também aceitará: "md5", "sha1" e "sha512",
    para testes.

    CURIOSIDADES:
    - MD5 e SHA-1 são considerados INSEGUROS hoje em dia (fáceis de quebrar
      com ataques de colisão / força bruta). Já o
    - SHA-256 e SHA-512 são da família SHA-2, muito mais seguros.
    - Por isso o padrão SHA-256 como algoritmo principal. (acho)
    """

    # As funções de hash trabalham com bytes, não com texto direto.
    # Por isso, variável para "codificar" a senha antes de gerar o hash, passei paramento utf-8 pela senha ser em portugues
    senha_em_bytes = senha.encode("utf-8")

    if algoritmo == "md5":
        hash_gerado = hashlib.md5(senha_em_bytes)
    elif algoritmo == "sha1":
        hash_gerado = hashlib.sha1(senha_em_bytes)
    elif algoritmo == "sha512":
        hash_gerado = hashlib.sha512(senha_em_bytes)
    else:
        # Padrão do trabalho: SHA-256
        hash_gerado = hashlib.sha256(senha_em_bytes)

    # .hexdigest() transforma o hash (que é binário) em uma string hexadecimal
    #hex = hexademcimal digest = resumo
    # letras e números, que é o formato que a gente guarda no banco.
    return hash_gerado.hexdigest()
