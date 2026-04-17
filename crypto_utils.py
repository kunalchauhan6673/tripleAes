import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

KEY_LENGTH = 32
ITERATIONS = 100000
SALT = b"secure_salt_123"

def pad(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    return data[:-data[-1]]

def derive_keys(password):
    full_key = PBKDF2(password, SALT, dkLen=96, count=ITERATIONS)
    return full_key[:32], full_key[32:64], full_key[64:96]

def encrypt_file(path, password):
    with open(path, 'rb') as f:
        data = pad(f.read())

    k1, k2, k3 = derive_keys(password)

    iv1 = get_random_bytes(16)
    iv2 = get_random_bytes(16)
    iv3 = get_random_bytes(16)

    cipher1 = AES.new(k1, AES.MODE_CBC, iv1)
    cipher2 = AES.new(k2, AES.MODE_CBC, iv2)
    cipher3 = AES.new(k3, AES.MODE_CBC, iv3)

    c1 = cipher1.encrypt(data)
    c2 = cipher2.decrypt(c1)
    c3 = cipher3.encrypt(c2)

    hash_val = SHA256.new(data=data).digest()

    save_path = os.path.join(os.path.dirname(path), "encrypted_" + os.path.basename(path))

    with open(save_path, 'wb') as f:
        f.write(iv1 + iv2 + iv3 + c3 + hash_val)

    return save_path

def decrypt_file(path, password):
    with open(path, 'rb') as f:
        data = f.read()

    iv1, iv2, iv3 = data[:16], data[16:32], data[32:48]
    encrypted_data = data[48:-32]
    original_hash = data[-32:]

    k1, k2, k3 = derive_keys(password)

    cipher1 = AES.new(k1, AES.MODE_CBC, iv1)
    cipher2 = AES.new(k2, AES.MODE_CBC, iv2)
    cipher3 = AES.new(k3, AES.MODE_CBC, iv3)

    p1 = cipher3.decrypt(encrypted_data)
    p2 = cipher2.encrypt(p1)
    p3 = cipher1.decrypt(p2)

    p3 = unpad(p3)

    if SHA256.new(data=pad(p3)).digest() != original_hash:
        raise ValueError("Wrong password or corrupted file")

    save_path = os.path.join(os.path.dirname(path), "decrypted_" + os.path.basename(path))

    with open(save_path, 'wb') as f:
        f.write(p3)

    return save_pathx