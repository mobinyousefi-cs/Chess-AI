#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: Game of Chess AI
File: game.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-05
Updated: 2025-11-05
License: MIT License (see LICENSE file for details)
=

Description:
High-level game orchestration utilities for playing chess games, including human vs AI and
AI vs AI modes. Responsible for tracking the board state, checking for game termination, and
validating user moves.

Usage:
from chess_ai.game import Game

game = Game()
print(game.board.to_ascii())

Notes:
- The CLI wrapper is implemented in `chess_ai.main`.
=================================================================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .ai import SearchResult, find_best_move
from .board import Board, Color, Move


@dataclass
class GameResult:
    winner: Optional[Color]  # "white", "black", or None for draw
    reason: str


class Game:
    """Represents a single chess game."""

    def __init__(self) -> None:
        self.board: Board = Board.start_position()

    @property
    def turn(self) -> Color:
        return self.board.turn

    def apply_move(self, move: Move) -> None:
        self.board = self.board.apply_move(move)

    def is_finished(self) -> Optional[GameResult]:
        color = self.board.turn
        if self.board.is_checkmate(color):
            return GameResult(winner=Board.opposite(color), reason="checkmate")
        if self.board.is_stalemate(color):
            return GameResult(winner=None, reason="stalemate")
        return None

    # -----------------------------------------------------------------------------------------------------------------
    # Human interaction helpers
    # -----------------------------------------------------------------------------------------------------------------

    def parse_and_validate_move(self, move_str: str) -> Optional[Move]:
        """Parse a move string and ensure it is legal from the current position.

        Returns the Move if valid, otherwise None.
        """

        move_str = move_str.strip()
        try:
            move = Move.from_long_algebraic(move_str)
        except ValueError:
            return None

        legal_moves = self.board.generate_legal_moves(self.turn)
        for m in legal_moves:
            if m.from_sq == move.from_sq and m.to_sq == move.to_sq:
                # Allow engine to decide promotion piece if user omitted it, defaulting to queen
                if m.promotion is not None and move.promotion is None:
                    move = Move(m.from_sq, m.to_sq, promotion=m.promotion)
                return move
        return None

    def ai_move(self, depth: int = 3) -> SearchResult:
        """Ask the engine to play a move for the current side to move."""

        return find_best_move(self.board, max_depth=depth)