from encode import encode
from decode import decode
import os

def main():
    print("\nKnightCipher - Secure Chess-Based File Exchange")
    print("1) Encode a file")
    print("2) Decode a file")
    choice = input("\nSelect an option (1/2): ").strip()

    if choice == "1":
        file_path = input("Enter the path to the file to encode: ").strip()
        sender_private_key = input("Enter path to sender's private key: ").strip()
        receiver_public_key = input("Enter path to receiver's public key: ").strip()
        if all(map(os.path.exists, [file_path, sender_private_key, receiver_public_key])):
            try:
                encode(file_path, sender_private_key, receiver_public_key)
            except Exception as e:
                print(f"\nEncoding failed: {e}")
        else:
            print("\nError: One or more file paths are invalid.")

    elif choice == "2":
        package_file_path = input("Enter path to .knightcipher package: ").strip()
        receiver_private_key = input("Enter path to receiver's private key: ").strip()
        output_file_path = input("Enter path to save the recovered file: ").strip()
        if all(map(os.path.exists, [package_file_path, receiver_private_key])):
            try:
                decode(package_file_path, receiver_private_key, output_file_path)
            except Exception as e:
                print(f"\nDecoding failed: {e}")
        else:
            print("\nError: One or more file paths are invalid.")

    else:
        print("\nInvalid choice. Please run the program again and select 1 or 2.")

if __name__ == "__main__":
    main()
