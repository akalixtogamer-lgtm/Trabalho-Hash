"""
Regras de formato da senha.
"""

import re


# ------------------------------------------------------
# VALIDAÇÃO DO FORMATO DA SENHA
# ------------------------------------------------------

def senha_e_valida(senha):
    """
    Confere se a senha segue a regra pedida:
    - De 8 a 16 caracteres
    - Pelo menos 1 letra MAIÚSCULA
    - Pelo menos 1 letra minúscula
    - Pelo menos 1 caractere especial (ex: @, #, !, $)
    """

    if len(senha) < 8 or len(senha) > 16:

        print("-> A senha precisa ter de 8 a 16 caracteres.")
        return False

    tem_maiuscula = re.search(r"[A-Z]", senha)
    tem_minuscula = re.search(r"[a-z]", senha)
    tem_especial = re.search(r"[^A-Za-z0-9]", senha)

    if not tem_maiuscula:
        print("-> A senha precisa ter pelo menos 1 letra MAIÚSCULA.")
        return False

    if not tem_minuscula:
        print("-> A senha precisa ter pelo menos 1 letra minúscula.")
        return False

    if not tem_especial:
        print("-> A senha precisa ter pelo menos 1 caractere especial (ex: @, #, !, $).")
        return False

    return True
