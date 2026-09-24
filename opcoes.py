"""
As 3 opções do menu: cadastro, validação e pesquisa do hash.
Aqui fica só a conversa com o usuário (input/print); o trabalho
"pesado" é feito pelos módulos banco, hash_senha e validacao.
"""

from banco import inserir_usuario, buscar_hash
from hash_senha import gerar_hash
from validacao import senha_e_valida


# ------------------------------------------------------
# OPÇÃO 1 - CADASTRO DE SENHA
# ------------------------------------------------------

def cadastrar_senha():
    print("\n--- CADASTRO DE SENHA ---")

    email = input("Digite o e-mail: ").strip()

    # Fica pedindo a senha até o usuário digitar uma que seja válida
    while True:
        senha = input(
            "Digite uma senha (de 8 a 16 caracteres, com maiúscula, minúscula "
            "e caractere especial): "
        )
        if senha_e_valida(senha):
            break

    # Gera o hash da senha usando SHA-256 (padrão)
    hash_da_senha = gerar_hash(senha, algoritmo="sha256")

    if inserir_usuario(email, hash_da_senha):
        print("\nUsuário cadastrado com sucesso!")
        print(f"Hash salvo no banco: {hash_da_senha}")
    else:
        print("\n-> Esse e-mail já está cadastrado!")


# ------------------------------------------------------
# OPÇÃO 2 - VALIDAÇÃO DE SENHA
# ------------------------------------------------------

def validar_senha():
    print("\n--- VALIDAÇÃO DE SENHA ---")

    email = input("Digite o e-mail: ").strip()
    senha = input("Digite a senha: ")

    hash_salvo_no_banco = buscar_hash(email)

    if hash_salvo_no_banco is None:
        print("\n-> E-mail inexistente.")
        return

    # Gera o hash da senha que o usuário acabou de digitar,
    # usando o MESMO algoritmo do cadastro (SHA-256)
    hash_digitado_agora = gerar_hash(senha, algoritmo="sha256")

    # Compara os dois hashes (nunca comparamos a senha em texto puro!)
    if hash_digitado_agora == hash_salvo_no_banco:
        print("\n-> Senha correta!")
    else:
        print("\n-> Senha incorreta!")


# ------------------------------------------------------
# OPÇÃO 3 - PESQUISA DO HASH DA SENHA NO BANCO
# ------------------------------------------------------

def pesquisar_hash():
    print("\n--- PESQUISA DO HASH DA SENHA ---")

    email = input("Digite o e-mail: ").strip()

    hash_salvo = buscar_hash(email)

    if hash_salvo is None:
        print("\n-> E-mail inexistente.")
    else:
        print(f"\nHash da senha cadastrada: {hash_salvo}")
