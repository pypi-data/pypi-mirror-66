from . import *


def main() -> None:
    import sys
    if len(sys.argv[1:]) != 3:
        exit(1)
    command = sys.argv[1]
    key = sys.argv[2]
    content = sys.argv[3]
    cipher = AESCipher(key)
    if command == "e":
        print(cipher.encrypt(content), flush=True)
    elif command == "d":
        print(cipher.decrypt(content), flush=True)
    else:
        exit(1)
    exit(0)


if __name__ == "__main__":
    main()

