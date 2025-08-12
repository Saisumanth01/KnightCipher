from time import time
from math import log2
from chess import pgn, Board
from kyp_utils import deserialize_kyp
from crypto_utils import rsa_decrypt
from util import from_binary_string, chunk_binary_string, to_binary_string

def decode(package_file_path: str, receiver_private_key_path: str, output_file_path: str):
    start_time = time()

    with open(package_file_path, "rb") as f:
        raw_data = f.read()

    parts = raw_data.split(b"===PGN===\n")
    if len(parts) != 2:
        raise ValueError("Invalid package format: PGN section missing.")

    kyp_section = parts[0].split(b"===KYP===\n")
    if len(kyp_section) != 2:
        raise ValueError("Invalid package format: KYP section missing.")

    kyp_encrypted = kyp_section[1].strip()
    pgn_data = parts[1].decode()

    decrypted_kyp = rsa_decrypt(receiver_private_key_path, kyp_encrypted)
    kyp_map = deserialize_kyp(decrypted_kyp.decode())

    games = []
    game_buffer = []
    for line in pgn_data.splitlines():
        if line.strip() == "" and game_buffer:
            games.append(pgn.read_game(iter(game_buffer)))
            game_buffer = []
        else:
            game_buffer.append(line)
    if game_buffer:
        games.append(pgn.read_game(iter(game_buffer)))

    binary_data = ""

    for game in games:
        board = Board()
        for move in game.mainline_moves():
            legal_moves = list(board.generate_legal_moves())
            move_index = legal_moves.index(move)
            max_length = int(log2(len(legal_moves)))
            move_bin_str = to_binary_string(move_index, max_length)
            binary_data += move_bin_str
            board.push(move)

    byte_data = bytes([from_binary_string(chunk) for chunk in chunk_binary_string(binary_data, 8)])

    with open(output_file_path, "wb") as f:
        f.write(byte_data)

    print(f"\nSuccessfully decoded '{package_file_path}' and recovered original file to '{output_file_path}' (Elapsed: {round(time() - start_time, 3)}s).")
