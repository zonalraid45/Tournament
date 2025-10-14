#!/usr/bin/env python3
import chess.pgn
import argparse

def filter_black_wins(input_pgn, output_pgn):
    with open(input_pgn, "r", encoding="utf-8") as infile, \
         open(output_pgn, "w", encoding="utf-8") as outfile:

        count = 0
        while True:
            game = chess.pgn.read_game(infile)
            if game is None:
                break

            result = game.headers.get("Result", "").strip()
            if result == "0-1":  # Only Black wins
                outfile.write(str(game) + "\n\n")
                count += 1

    print(f"✅ Saved {count} Black-win games to {output_pgn}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter PGN and keep only Black wins.")
    parser.add_argument("--input", required=True, help="Input PGN file path")
    parser.add_argument("--output", required=True, help="Output PGN file path")
    args = parser.parse_args()

    filter_black_wins(args.input, args.output)
