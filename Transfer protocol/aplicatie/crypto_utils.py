import hashlib
import hmac
from qiskit_qnrg import generate_random_bits  # Asigură-te că ai funcția din qiskit_qnrg.py
import time
def generate_key(username):
    # Generăm 256 biți aleatori folosind QRNG
    random_bits = generate_random_bits(256)
    # Adăugăm un timestamp pentru entropie suplimentară
    timestamp = str(time.time())  # Current time in seconds
    raw_key = f"{random_bits}:{timestamp}:{username}"
    # Hash-ul cheii brute pentru a obține o cheie sigură și unică
    key = hashlib.sha256(raw_key.encode()).hexdigest()
    return key

def sign_file(file_path, key):
    
    with open(file_path, "rb") as f:
        file_data = f.read()
    # Generăm o semnătură folosind HMAC-SHA256
    signature = hmac.new(key.encode(), file_data, hashlib.sha256).hexdigest()
    return signature

def verify_signature(file_path, signature, key):
 
    if not isinstance(key, str):
        raise ValueError(f"Key should be a string, but got {type(key).__name__}.")

    with open(file_path, "rb") as f:
        file_data = f.read()
    # Generăm semnătura așteptată pentru fișier
    expected_signature = hmac.new(key.encode(), file_data, hashlib.sha256).hexdigest()
    # Comparăm semnătura generată cu cea furnizată
    return hmac.compare_digest(expected_signature, signature)
