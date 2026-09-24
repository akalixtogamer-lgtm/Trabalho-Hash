"""
Trabalho de Segurança - Hash e senhas em banco de dados
========================================================================
Este programa faz o cadastro de usuários (e-mail + senha) em um banco de
dados SQLite, mas NUNCA guarda a senha em texto puro. Em vez disso, é
guardado apenas o HASH da senha.

O trabalho pede o algoritmo SHA-256 como padrão, então uso ele como padrão. Mas desenvolvi os outros

Organização dos arquivos:
- trabalho_hash_senhas.py -> arquivo atual: menu principal (ponto de entrada)
- opcoes.py               -> as 3 opções do menu (cadastro, validação, pesquisa)
- banco.py                -> tudo que mexe com o banco SQLite
- hash_senha.py           -> geração do hash (SHA-256 e outros)
- validacao.py            -> regras de formato da senha
"""

from banco import criar_banco
from opcoes import cadastrar_senha, validar_senha, pesquisar_hash


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
