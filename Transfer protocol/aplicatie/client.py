from crypto_utils import sign_file
from server import receive_file

def send_file(username, key, file_path):
    # Semnează fișierul cu cheia generată
    signature = sign_file(file_path, key)
    print(f"Original Signature: {signature}")

    # Alterare manuală sau automată a semnăturii
    alter_choice = input("Do you want to alter the signature? (yes/no): ").strip().lower()
    if alter_choice == "yes":
        alter_type = input("Choose alteration type (truncate, noise, flip): ").strip().lower()

        if alter_type == "truncate":
            altered_signature = signature[:len(signature)//2]  # Trunchierea semnăturii
            print(f"Truncated Signature: {altered_signature}")
        elif alter_type == "noise":
            # Adăugare zgomot
            import random
            altered_signature = ''.join(
                char if random.random() > 0.1 else ('0' if char != '0' else '1') for char in signature
            )
            print(f"Signature with Noise: {altered_signature}")
        elif alter_type == "flip":
            # Flip ultimul caracter al semnăturii
            altered_signature = signature[:-1] + ('0' if signature[-1] != '0' else '1')
            print(f"Flipped Signature: {altered_signature}")
        else:
            print("Invalid alteration type! Sending the original signature.")
            altered_signature = signature
    else:
        altered_signature = signature

    # Trimiterea semnăturii și a fișierului către server
    print("Sending file to the server...")
    success, saved_path = receive_file(file_path, altered_signature, username)

    if success:
        print(f"File successfully verified and saved at: {saved_path}")
    else:
        print("File verification failed on the server.")
