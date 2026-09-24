"""
Tudo que conversa com o banco de dados SQLite fica aqui.
"""

import sqlite3


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
        Create table if not exists usuarios (
            email text PRIMARY KEY,
            hash_senha text NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def inserir_usuario(email, hash_senha):
    """
    Guarda o e-mail e o HASH no banco.
    A senha original (texto puro) não é salva em lugar nenhum!

    Retorna True se cadastrou, ou False se o e-mail já existia.
    """
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (email, hash_senha) VALUES (?, ?)",
            (email, hash_senha)
        )
        conexao.commit()
        return True

    except sqlite3.IntegrityError:
        # Esse erro acontece quando o e-mail já existe (chave primária duplicada)
        return False

    finally:
        conexao.close()


def buscar_hash(email):
    """
    Busca o hash salvo no banco a partir do e-mail (chave primária).
    Retorna o hash, ou None se o e-mail não existir.
    """
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    cursor.execute("SELECT hash_senha FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()

    conexao.close()

    if resultado is None:
        return None
    return resultado[0]
