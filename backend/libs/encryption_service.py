"""
Генерация ключей:

Используется алгоритм RSA для генерации пары ключей.

Ключи сериализуются в формате бинарных данных для удобного хранения.

Шифрование:

Данные преобразуются в строку с помощью json.dumps().

Используется схема шифрования OAEP с хэшированием SHA-256.

Расшифрование:

Зашифрованные данные преобразуются обратно в байты.

Используется приватный ключ для расшифрования.

Поддержка разных типов данных:

Методы поддерживают строки, числа, списки и словари.
"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import json

def generate_keys():
    """
    Генерирует пару ключей (публичный и приватный) для асимметричного шифрования.

    :return: Публичный и приватный ключи в бинарном формате (тип bytes).
    """
    # Генерация приватного ключа
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Генерация публичного ключа
    public_key = private_key.public_key()

    # Сериализация ключей в бинарный формат (DER)
    private_der = private_key.private_bytes(
        encoding=serialization.Encoding.DER,  # Используем DER для бинарного формата
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,  # Используем DER для бинарного формата
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return public_der, private_der


def encrypt_data(data: str, public_key_der: bytes) -> bytes:
    """
    Шифрует данные с использованием публичного ключа.

    :param data: Данные для шифрования (текстовая строка).
    :param public_key_der: Публичный ключ в бинарном формате (DER).
    :return: Зашифрованные данные в бинарном формате.
    """
    # Десериализация публичного ключа
    public_key = serialization.load_der_public_key(public_key_der)

    # Шифрование данных
    encrypted = public_key.encrypt(
        data.encode('utf-8'),  # Преобразуем строку в байты
        padding.PKCS1v15(),    # Используем PKCS1v15 без хеширования
    )

    return encrypted  # Возвращаем бинарные данные

    
    
def decrypt_data(encrypted_data: bytes, private_key_der: bytes) -> str:
    """
    Расшифровывает данные с использованием приватного ключа.

    :param encrypted_data: Зашифрованные данные в бинарном формате.
    :param private_key_der: Приватный ключ в бинарном формате (DER).
    :return: Расшифрованные данные в виде текстовой строки.
    """
    # Десериализация приватного ключа
    private_key = serialization.load_der_private_key(
        private_key_der,
        password=None,
    )

    # Расшифрование данных
    decrypted = private_key.decrypt(
        encrypted_data,
        padding.PKCS1v15(),  # Используем PKCS1v15 без хеширования
    )

    # Преобразуем байты обратно в строку
    return decrypted.decode('utf-8')