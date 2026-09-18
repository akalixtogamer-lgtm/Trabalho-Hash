"""
Trabalho de Segurança - Hash e senhas em banco de dados
========================================================================
Este programa faz o cadastro de usuários (e-mail + senha) em um banco de
dados SQLite, mas NUNCA guarda a senha em texto puro. Em vez disso, é
guardado apenas o HASH da senha.

O trabalho pede o algoritmo SHA-256 como padrão, então uso ele como padrão. Mas desenvolvi os outros 
"""

import sqlite3
import hashlib
import re


# ------------------------------------------------------
# CONFIGURAÇÃO DO BANCO DE DADOS
# ------------------------------------------------------

#Variável para salvar os contatos
NOME_BANCO = "usuarios.db"


def criar_banco():
    """
    Função para criar a tabela 'usuarios' no banco de dados, caso ela ainda não exista.
    - email        -> CHAVE PRIMÁRIA (não pode se repetir)
    - hash_senha   -> guarda só o hash, nunca a senha original
    """
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    cursor.execute("""
        Criando tabela se ela não existir usuarios (
            email texto PRIMARY KEY,
            hash_senha texto NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


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

    if len(senha) <= 8:
    
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
    #função para guardar senha e o algoritmo escolhido

    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    try:
        # Guarda o e-mail e o HASH no banco.
        # A senha original (texto puro) não é salva em lugar nenhum!
        cursor.execute(
            "INSERT INTO usuarios (email, hash_senha) VALUES (?, ?)",
            (email, hash_da_senha)
        )
        conexao.commit()
        print("\nUsuário cadastrado com sucesso!")
        print(f"Hash salvo no banco: {hash_da_senha}")

    except sqlite3.IntegrityError:
        # Esse erro acontece quando o e-mail já existe (chave primária duplicada)
        print("\n-> Esse e-mail já está cadastrado!")

    conexao.close()


# ------------------------------------------------------
# OPÇÃO 2 - VALIDAÇÃO DE SENHA
# ------------------------------------------------------

def validar_senha():
    print("\n--- VALIDAÇÃO DE SENHA ---")

    email = input("Digite o e-mail: ").strip()
    senha = input("Digite a senha: ")

    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    # Busca o hash salvo no banco a partir do e-mail (chave primária)
    cursor.execute("SELECT hash_senha FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()

    conexao.close()

    if resultado is None:
        print("\n-> E-mail inexistente.")
        return

    hash_salvo_no_banco = resultado[0]

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

    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    cursor.execute("SELECT hash_senha FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()

    conexao.close()

    if resultado is None:
        print("\n-> E-mail inexistente.")
    else:
        print(f"\nHash da senha cadastrada: {resultado[0]}")


# ------------------------------------------------------
# MENU PRINCIPAL
# ------------------------------------------------------

def menu():
    criar_banco()  # garante que a tabela já existe antes de tudo

    while True:
        print("\n===== MENU =====")
        print("1) Cadastro de senha")
        print("2) Validação de senha")
        print("3) Pesquisa do hash da senha no banco")
        print("4) Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_senha()
        elif opcao == "2":
            validar_senha()
        elif opcao == "3":
            pesquisar_hash()
        elif opcao == "4":
            print("\nSaindo do programa...")
            break
        else:
            print("\n-> Opção inválida, tente novamente.")


# Ponto de entrada do programa
if __name__ == "__main__":
    menu()
