#!/usr/bin/env python3
import chess.pgn, sys, pathlib

IN  = pathlib.Path("black.pgn")
OUT = pathlib.Path("blacker.pgn")
BOT = "Nikitosikbot_v2"

with IN.open() as fin, OUT.open("w") as fout:
    while (g := chess.pgn.read_game(fin)) is not None:
        if g.headers.get("White") == BOT and g.headers.get("Result") in {"1-0", "1/2-1/2"}:
            print(g, file=fout, end="\n\n")
