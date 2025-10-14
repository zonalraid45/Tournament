#!/usr/bin/env python3
import argparse
import chess.pgn

def filter_games(input_pgn, output_pgn, result_type):
    """
    Filter PGN games by result (win or loss) for any player.
    Saves filtered games to output_pgn.
    """
    result_type = result_type.lower()
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

            result = game.headers.get("Result", "").strip()

            if result_type == "win":
                if result in ("1-0", "0-1"):  # any decisive win
                    outfile.write(str(game) + "\n\n")
                    kept += 1
            elif result_type == "loss":
                if result in ("1-0", "0-1"):  # any decisive loss
                    outfile.write(str(game) + "\n\n")
                    kept += 1

    print(f"✅ Found {kept}/{total} games matching '{result_type}'.")
    print(f"📁 Saved filtered games to {output_pgn}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter PGN games by win/loss for any player.")
    parser.add_argument("--input", required=True, help="Input PGN file path")
    parser.add_argument("--output", required=True, help="Output PGN file path")
    parser.add_argument("--result", required=True, choices=["win", "loss"], help="Result type (win or loss)")
    args = parser.parse_args()

    filter_games(args.input, args.output, args.result)
