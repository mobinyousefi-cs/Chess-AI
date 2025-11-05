#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: Game of Chess AI
File: main.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-05
Updated: 2025-11-05
License: MIT License (see LICENSE file for details)
=

Description:
Command-line interface for the Game of Chess AI project. Allows a human player to play against the
engine from the terminal using long algebraic notation (e.g. "e2e4").

Usage:
python -m chess_ai.main --depth 3 --human-color white

Notes:
- Type "help" during the game to see available commands.
- Type "quit" to exit the game at any time.
=================================================================================================================
"""

from __future__ import annotations

import argparse
from typing import Literal

from .game import Game


HumanColor = Literal["white", "black"]


def run_cli() -> None:
    parser = argparse.ArgumentParser(description="Play chess against a simple minimax-based engine.")
    parser.add_argument("--depth", type=int, default=3, help="Search depth in plies (default: 3)")
    parser.add_argument(
        "--human-color",
        type=str,
        default="white",
        choices=["white", "black"],
        help="Which side the human will play (default: white)",
    )
    args = parser.parse_args()

    human_color: HumanColor = args.human_color  # type: ignore[assignment]
    depth: int = args.depth

    game = Game()
    print("Game of Chess AI — Mobin Yousefi")
    print("Type moves like 'e2e4'. Type 'help' for commands, 'quit' to exit.\n")

    while True:
        result = game.is_finished()
        if result is not None:
            print(game.board.to_ascii())
            if result.winner is None:
                print(f"Game over: draw by {result.reason}.")
            else:
                print(f"Game over: {result.winner.capitalize()} wins by {result.reason}.")
            break

        side_to_move = game.turn
        print(game.board.to_ascii())
        print(f"Side to move: {side_to_move}\n")

        if side_to_move == human_color:
            user_input = input("Your move> ").strip()
            if user_input.lower() in {"quit", "exit"}:
                print("Goodbye!")
                break
            if user_input.lower() in {"help", "?"}:
                print("""
Commands:
  - Enter a move in long algebraic notation, e.g. 'e2e4', 'g1f3'.
  - 'help' or '?'  : Show this help message.
  - 'quit' or 'exit': Quit the game.
                """)
                continue

            move = game.parse_and_validate_move(user_input)
            if move is None:
                print("Invalid or illegal move. Please try again.\n")
                continue

            game.apply_move(move)
        else:
            print(f"Engine ({side_to_move}) is thinking (depth={depth})...")
            search_result = game.ai_move(depth=depth)
            if search_result.move is None:
                print("Engine has no moves — game should be finished.")
                break
            engine_move = search_result.move
            print(
                f"Engine plays: {engine_move.to_long_algebraic()} "
                f"(score={search_result.score:.2f} from {side_to_move}'s perspective)\n"
            )
            game.apply_move(engine_move)


if __name__ == "__main__":  # pragma: no cover
    run_cli()