def to_binary_string(value: int, length: int) -> str:
    return format(value, f"0{length}b")

def from_binary_string(bits: str) -> int:
    return int(bits, 2)

def chunk_binary_string(bits: str, chunk_size: int) -> list[str]:
    return [bits[i:i + chunk_size] for i in range(0, len(bits), chunk_size)]
