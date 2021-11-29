import secrets
import string
import uuid


def gerar_senha_letras(comprimento):
    """Gerar uma senha com letras, com o comprimento informado
    :param comprimento: Comprimento da senha
    :return: Senha gerada
    """
    password_characters = string.ascii_letters
    password = ''.join(secrets.choice(password_characters) for i in range(comprimento))
    return password


def gerar_senha_letras_numeros(comprimento):
    """Gerar uma senha com letras e números, com o comprimento informado
    :param comprimento: Comprimento da senha
    :return: Senha gerada
    """
    password_characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(password_characters) for i in range(comprimento))
    return password


def gerar_senha_letras_numeros_simbolos(comprimento):
    """Gerar uma senha com letras, números e símbolos, com o comprimento informado
    :param comprimento: Comprimento da senha
    :return: Senha gerada
    """
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(password_characters) for i in range(comprimento))
    return password


def gerar_senha_hexadecimal(metade_comprimento):
    """Gerar uma senha hexadecimal, sendo o comprimento igual o dobro
    :param metade_comprimento: Comprimento da senha
    :return: Senha gerada
    """
    password = secrets.token_hex(metade_comprimento)
    return password


def gerar_senha_uuid():
    """Gerar uma senha com UUID com 36 caracteres
    :return:
    """
    password = uuid.uuid4()
    return password
