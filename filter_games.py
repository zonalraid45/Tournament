#!/usr/bin/env python3
import chess.pgn, pathlib

IN  = pathlib.Path("black.pgn")     # PGN where Nikitosikbot_v2 plays Black
OUT = pathlib.Path("blacker.pgn")   # Output PGN without losses
BOT = "Nikitosikbot_v2"

with IN.open() as fin, OUT.open("w") as fout:
    while (g := chess.pgn.read_game(fin)) is not None:
        # Keep the game if our bot was Black AND did **not** lose
        if g.headers.get("Black") == BOT and g.headers.get("Result") in {"0-1", "1/2-1/2"}:
            print(g, file=fout, end="\n\n")
