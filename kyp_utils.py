import random
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

FILESQUARES = [
    f"{file}{rank}" for rank in range(1, 9) for file in "abcdefgh"
]

def get_32_bits_from_private_key(private_key_path: str) -> str:
    with open(private_key_path, "rb") as key_file:
        key_bytes = key_file.read()
        binary = "".join(f"{byte:08b}" for byte in key_bytes)

    if len(binary) < 32:
        raise ValueError("Private key file too small to extract 32 bits.")

    start = random.randint(0, len(binary) - 32)
    return binary[start:start + 32]

def generate_kyp_mapping(private_key_path: str) -> dict:
    bit_string = get_32_bits_from_private_key(private_key_path)
    selected_squares = random.sample(FILESQUARES, 32)
    return {square: int(bit) for square, bit in zip(selected_squares, bit_string)}

def serialize_kyp(mapping: dict) -> str:
    return "\n".join(f"{square}:{bit}" for square, bit in mapping.items())

def deserialize_kyp(data: str) -> dict:
    result = {}
    for line in data.strip().splitlines():
        parts = line.strip().split(":")
        if len(parts) == 2:
            square, bit = parts
            result[square] = int(bit)
    return result
