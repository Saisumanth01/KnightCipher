from time import time
from math import log2
from chess import pgn, Board
from util import to_binary_string
from kyp_utils import generate_kyp_mapping, serialize_kyp
from crypto_utils import rsa_encrypt

def encode(file_path: str, sender_private_key: str, receiver_public_key: str):
    start_time = time()

    with open(file_path, "rb") as f:
        file_bytes = list(f.read())

    file_bits_count = len(file_bytes) * 8
    output_pgns = []
    file_bit_index = 0
    chess_board = Board()

    kyp_map = generate_kyp_mapping(sender_private_key)
    kyp_serialized = serialize_kyp(kyp_map)
    encrypted_kyp = rsa_encrypt(receiver_public_key, kyp_serialized.encode())

    while True:
        legal_moves = list(chess_board.generate_legal_moves())
        move_bits = {}

        max_binary_length = min(
            int(log2(len(legal_moves))),
            file_bits_count - file_bit_index
        )

        for index, legal_move in enumerate(legal_moves):
            move_binary = to_binary_string(index, max_binary_length)
            if len(move_binary) > max_binary_length:
                break
            move_bits[legal_move.uci()] = move_binary

        closest_byte_index = file_bit_index // 8
        file_chunk_pool = "".join([
            to_binary_string(byte, 8)
            for byte in file_bytes[closest_byte_index: closest_byte_index + 2]
        ])

        next_file_chunk = file_chunk_pool[
            file_bit_index % 8:
            file_bit_index % 8 + max_binary_length
        ]

        for move_uci, move_binary in move_bits.items():
            if move_binary == next_file_chunk:
                chess_board.push_uci(move_uci)
                break

        file_bit_index += max_binary_length

        eof_reached = file_bit_index >= file_bits_count

        if (
            chess_board.legal_moves.count() <= 1
            or chess_board.is_insufficient_material()
            or chess_board.can_claim_draw()
            or eof_reached
        ):
            pgn_board = pgn.Game()
            pgn_board.add_line(chess_board.move_stack)
            output_pgns.append(str(pgn_board))
            chess_board.reset()

        if eof_reached:
            break

    final_output = b"===KYP===\n" + encrypted_kyp + b"\n===PGN===\n" + "\n\n".join(output_pgns).encode()

    with open(file_path + ".knightcipher", "wb") as f:
        f.write(final_output)

    print(
        f"\nSuccessfully encoded '{file_path}' into {len(output_pgns)} game(s) in PGN format"
        + f" and attached encrypted KYP (Elapsed: {round(time() - start_time, 3)}s)."
    )
