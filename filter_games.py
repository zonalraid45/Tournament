#!/usr/bin/env python3
import argparse
import chess.pgn

def filter_games(input_pgn, output_pgn, result_type, username):
    """
    Filter PGN games for a specific username based on result (win/loss).
    Saves the filtered games to output_pgn.
    """
    result_type = result_type.lower()
    username = username.strip().lower()
    if result_type not in ("win", "loss"):
        raise ValueError("Result type must be 'win' or 'loss'")

    total = kept = 0

    with open(input_pgn, "r", encoding="utf-8") as infile, \
         open(output_pgn, "w", encoding="utf-8") as outfile:

        while True:
            game = chess.pgn.read_game(infile)
            if game is None:
                break
            total += 1

            white = game.headers.get("White", "").strip().lower()
            black = game.headers.get("Black", "").strip().lower()
            result = game.headers.get("Result", "").strip()

            you_are_white = (white == username)
            you_are_black = (black == username)

            # Skip games where username is not involved
            if not (you_are_white or you_are_black):
                continue

            # Determine if this game is a win or loss for username
            if result_type == "win":
                if (you_are_white and result == "1-0") or (you_are_black and result == "0-1"):
                    outfile.write(str(game) + "\n\n")
                    kept += 1
            elif result_type == "loss":
                if (you_are_white and result == "0-1") or (you_are_black and result == "1-0"):
                    outfile.write(str(game) + "\n\n")
                    kept += 1

    print(f"✅ Found {kept}/{total} games matching '{result_type}' for username '{username}'.")
    print(f"📁 Saved filtered games to {output_pgn}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter PGN games by win/loss for a specific username.")
    parser.add_argument("--input", required=True, help="Input PGN file path")
    parser.add_argument("--output", required=True, help="Output PGN file path")
    parser.add_argument("--result", required=True, choices=["win", "loss"], help="Result type (win or loss)")
    parser.add_argument("--username", required=True, help="Username to filter (case-insensitive)")
    args = parser.parse_args()

    filter_games(args.input, args.output, args.result, args.username)
