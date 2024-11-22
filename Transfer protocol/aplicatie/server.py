import os
from crypto_utils import verify_signature
from user_manager import get_active_key

RECEIVED_FILES_DIR = "received_files"

def ensure_directory_exists(directory):
    """Ensure that the directory exists, create it if not."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def receive_file(file_path, signature, username):

    # Extrage cheia activă a utilizatorului
    key = get_active_key(username)
    if not key:
        print(f"No active key found for user {username}. Verification failed.")
        return False, None

    # Salvăm fișierul primit într-un director local
    RECEIVED_FILES_DIR = "received_files"
    os.makedirs(RECEIVED_FILES_DIR, exist_ok=True)
    received_file_path = os.path.join(RECEIVED_FILES_DIR, os.path.basename(file_path))

    with open(file_path, "rb") as source:
        with open(received_file_path, "wb") as destination:
            destination.write(source.read())

    # Verificăm semnătura
    is_verified = verify_signature(received_file_path, signature, key)
    if is_verified:
        print(f"File '{file_path}' received from {username} verified successfully.")
    else:
        print(f"File '{file_path}' received from {username} failed verification.")
        print("Potential causes of failure: altered signature or tampered file.")

    return is_verified, received_file_path if is_verified else None
