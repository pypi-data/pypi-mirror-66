import pickle
from getpass import getpass
from cryptography.fernet import Fernet


def my_encrypt(object_input, key_save=False, file_name=None):
    if key_save and file_name is None:
        raise Exception("file name needed")
    while True:
        dialog = input("file is small (y or n)")
        if dialog == "n":
            return
        elif dialog == "y":
            break
        else:
            print("wrong answer")
    string_object = pickle.dumps(object_input)
    key = Fernet.generate_key()
    if key_save:
        with open(file_name, 'wb') as f:
            f.write(key)
    else:
        print("'''", end="")
        print(key)
        print("'''", end="")
    f = Fernet(key)
    return f.encrypt(string_object)


def my_decrypt(string_encrypted):
    key = getpass("key : ")
    f = Fernet(key)
    string_decrypted = f.decrypt(string_encrypted)
    return pickle.loads(string_decrypted)


def my_encrypt_save(object_input, key_save, file_name):
    encrypted = my_encrypt(object_input, key_save, file_name)
    with open(file_name, 'wb') as f:
        f.write(encrypted)


def my_decrypt_load(file_name):
    with open(file_name, 'rb') as f:
        string_encrypted = f.read()
    key = getpass("key : ")
    f = Fernet(key)
    return f.decrypt(string_encrypted)

