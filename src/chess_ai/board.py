#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: Game of Chess AI
File: board.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-05
Updated: 2025-11-05
License: MIT License (see LICENSE file for details)
=

Description:
Defines core chess data structures: Move and Board. Implements basic chess rules, move generation,
check/checkmate detection, and FEN import/export. Castling and en passant are intentionally omitted
in this first version for simplicity.

Usage:
from chess_ai.board import Board, Move

board = Board.start_position()
legal_moves = board.generate_legal_moves("white")

Notes:
- Board coordinates are 0-based: (row, col) with row=0 at rank 8 and col=0 at file 'a'.
- Moves use long algebraic notation like "e2e4" for CLI input/output.
=================================================================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

Color = str  # "white" or "black"
Piece = str  # "P", "n", etc.
Square = Tuple[int, int]  # (row, col)


@dataclass(frozen=True)
class Move:
    """Represents a single chess move.

    Attributes:
        from_sq: (row, col) of the origin square.
        to_sq: (row, col) of the destination square.
        promotion: Optional promotion piece symbol (e.g. "Q" or "q"), or None.
    """

    from_sq: Square
    to_sq: Square
    promotion: Optional[Piece] = None

    def to_long_algebraic(self) -> str:
        """Return move in long algebraic notation (e.g. "e2e4" or "e7e8Q")."""

        from_str = Board.square_to_str(self.from_sq)
        to_str = Board.square_to_str(self.to_sq)
        promo = self.promotion.upper() if self.promotion else ""
        return f"{from_str}{to_str}{promo}"

    @staticmethod
    def from_long_algebraic(s: str) -> "Move":
        """Parse a move string like "e2e4" or "e7e8Q" into a Move.

        Raises:
            ValueError: If the string is not a valid long algebraic notation.
        """

        s = s.strip()
        if len(s) not in (4, 5):
            raise ValueError(f"Invalid move string: {s!r}")

        from_sq = Board.str_to_square(s[0:2])
        to_sq = Board.str_to_square(s[2:4])
        promotion: Optional[Piece] = None
        if len(s) == 5:
            promo_char = s[4].upper()
            if promo_char not in {"Q", "R", "B", "N"}:
                raise ValueError(f"Invalid promotion piece: {promo_char!r}")
            promotion = promo_char
        return Move(from_sq=from_sq, to_sq=to_sq, promotion=promotion)


class Board:
    """Immutable representation of a chessboard position.

    The board is stored as an 8x8 list of lists containing piece symbols or None.

    Uppercase pieces belong to white, lowercase pieces belong to black.
    """

    def __init__(self, grid: Optional[List[List[Optional[Piece]]]] = None, turn: Color = "white") -> None:
        if grid is None:
            grid = [[None for _ in range(8)] for _ in range(8)]
        # Deep copy to enforce immutability semantics
        self._grid: List[List[Optional[Piece]]] = [[cell for cell in row] for row in grid]
        self.turn: Color = turn

    # -----------------------------------------------------------------------------------------------------------------
    # Construction helpers
    # -----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def start_position() -> "Board":
        """Return a Board initialized to the standard chess starting position."""

        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
        return Board.from_fen(fen)

    @staticmethod
    def from_fen(fen: str) -> "Board":
        """Create a board from a very small subset of FEN (board + side to move)."""

        parts = fen.strip().split()
        if len(parts) < 2:
            raise ValueError(f"Invalid FEN: {fen!r}")
        board_part, turn_part = parts[0], parts[1]
        rows = board_part.split("/")
        if len(rows) != 8:
            raise ValueError(f"Invalid FEN (rows): {fen!r}")
        grid: List[List[Optional[Piece]]] = []
        for row_str in rows:
            row: List[Optional[Piece]] = []
            for ch in row_str:
                if ch.isdigit():
                    for _ in range(int(ch)):
                        row.append(None)
                else:
                    row.append(ch)
            if len(row) != 8:
                raise ValueError(f"Invalid FEN row: {row_str!r}")
            grid.append(row)

        turn = "white" if turn_part == "w" else "black"
        return Board(grid=grid, turn=turn)

    def to_fen(self) -> str:
        """Export the board position to a minimal FEN string (board + side to move)."""

        rows: List[str] = []
        for r in range(8):
            empty = 0
            row_str = ""
            for c in range(8):
                piece = self._grid[r][c]
                if piece is None:
                    empty += 1
                else:
                    if empty:
                        row_str += str(empty)
                        empty = 0
                    row_str += piece
            if empty:
                row_str += str(empty)
            rows.append(row_str)
        board_part = "/".join(rows)
        turn_part = "w" if self.turn == "white" else "b"
        return f"{board_part} {turn_part}"

    # -----------------------------------------------------------------------------------------------------------------
    # Coordinate helpers
    # -----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def square_to_str(square: Square) -> str:
        row, col = square
        file_char = chr(ord("a") + col)
        rank_char = str(8 - row)
        return f"{file_char}{rank_char}"

    @staticmethod
    def str_to_square(s: str) -> Square:
        if len(s) != 2:
            raise ValueError(f"Invalid square string: {s!r}")
        file_char, rank_char = s[0], s[1]
        if file_char not in "abcdefgh" or rank_char not in "12345678":
            raise ValueError(f"Invalid square: {s!r}")
        col = ord(file_char) - ord("a")
        row = 8 - int(rank_char)
        return row, col

    @staticmethod
    def opposite(color: Color) -> Color:
        return "black" if color == "white" else "white"

    # -----------------------------------------------------------------------------------------------------------------
    # Board access
    # -----------------------------------------------------------------------------------------------------------------

    def piece_at(self, square: Square) -> Optional[Piece]:
        row, col = square
        return self._grid[row][col]

    def is_on_board(self, square: Square) -> bool:
        row, col = square
        return 0 <= row < 8 and 0 <= col < 8

    # -----------------------------------------------------------------------------------------------------------------
    # Move generation
    # -----------------------------------------------------------------------------------------------------------------

    def generate_legal_moves(self, color: Optional[Color] = None) -> List[Move]:
        """Generate all legal moves for the given color (or the side to move if None)."""

        if color is None:
            color = self.turn

        legal_moves: List[Move] = []
        for move in self._generate_pseudo_moves(color):
            new_board = self.apply_move(move, switch_turn=False)
            if not new_board.is_in_check(color):
                legal_moves.append(move)
        return legal_moves

    def _generate_pseudo_moves(self, color: Color) -> Iterable[Move]:
        for row in range(8):
            for col in range(8):
                piece = self._grid[row][col]
                if piece is None:
                    continue
                if color == "white" and not piece.isupper():
                    continue
                if color == "black" and not piece.islower():
                    continue
                yield from self._moves_for_piece((row, col), piece)

    def _moves_for_piece(self, square: Square, piece: Piece) -> Iterable[Move]:
        row, col = square
        color = "white" if piece.isupper() else "black"
        p = piece.upper()

        if p == "P":
            yield from self._pawn_moves(square, color)
        elif p == "N":
            yield from self._knight_moves(square, color)
        elif p == "B":
            yield from self._sliding_moves(square, color, directions=[(-1, -1), (-1, 1), (1, -1), (1, 1)])
        elif p == "R":
            yield from self._sliding_moves(square, color, directions=[(-1, 0), (1, 0), (0, -1), (0, 1)])
        elif p == "Q":
            yield from self._sliding_moves(
                square,
                color,
                directions=[(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)],
            )
        elif p == "K":
            yield from self._king_moves(square, color)
        else:
            return

    def _pawn_moves(self, square: Square, color: Color) -> Iterable[Move]:
        row, col = square
        direction = -1 if color == "white" else 1
        start_row = 6 if color == "white" else 1
        promotion_row = 0 if color == "white" else 7

        # Single step forward
        forward = (row + direction, col)
        if self.is_on_board(forward) and self.piece_at(forward) is None:
            if forward[0] == promotion_row:
                for promo in ("Q", "R", "B", "N"):
                    piece = promo if color == "white" else promo.lower()
                    yield Move(square, forward, promotion=piece)
            else:
                yield Move(square, forward)

            # Double step from starting rank
            double = (row + 2 * direction, col)
            if row == start_row and self.piece_at(double) is None and self.piece_at(forward) is None:
                yield Move(square, double)

        # Captures
        for dc in (-1, 1):
            target = (row + direction, col + dc)
            if not self.is_on_board(target):
                continue
            target_piece = self.piece_at(target)
            if target_piece is None:
                continue
            if color == "white" and target_piece.islower() or color == "black" and target_piece.isupper():
                if target[0] == promotion_row:
                    for promo in ("Q", "R", "B", "N"):
                        piece = promo if color == "white" else promo.lower()
                        yield Move(square, target, promotion=piece)
                else:
                    yield Move(square, target)

    def _knight_moves(self, square: Square, color: Color) -> Iterable[Move]:
        row, col = square
        deltas = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]
        for dr, dc in deltas:
            target = (row + dr, col + dc)
            if not self.is_on_board(target):
                continue
            piece = self.piece_at(target)
            if piece is None or (color == "white" and piece.islower()) or (color == "black" and piece.isupper()):
                yield Move(square, target)

    def _sliding_moves(self, square: Square, color: Color, directions: Iterable[Tuple[int, int]]) -> Iterable[Move]:
        row, col = square
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = self._grid[r][c]
                target = (r, c)
                if piece is None:
                    yield Move(square, target)
                else:
                    if (color == "white" and piece.islower()) or (color == "black" and piece.isupper()):
                        yield Move(square, target)
                    break
                r += dr
                c += dc

    def _king_moves(self, square: Square, color: Color) -> Iterable[Move]:
        row, col = square
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                target = (row + dr, col + dc)
                if not self.is_on_board(target):
                    continue
                piece = self.piece_at(target)
                if piece is None or (color == "white" and piece.islower()) or (color == "black" and piece.isupper()):
                    yield Move(square, target)

    # -----------------------------------------------------------------------------------------------------------------
    # Game status and move application
    # -----------------------------------------------------------------------------------------------------------------

    def apply_move(self, move: Move, switch_turn: bool = True) -> "Board":
        """Return a new Board with the given move applied.

        Args:
            move: Move to apply.
            switch_turn: Whether to toggle the side to move. When simulating a move for evaluating
                legality, this may be disabled.
        """

        new_grid = [[cell for cell in row] for row in self._grid]
        from_row, from_col = move.from_sq
        to_row, to_col = move.to_sq
        piece = new_grid[from_row][from_col]
        new_grid[from_row][from_col] = None

        if move.promotion is not None:
            piece = move.promotion

        new_grid[to_row][to_col] = piece
        next_turn = self.opposite(self.turn) if switch_turn else self.turn
        return Board(grid=new_grid, turn=next_turn)

    def _find_king(self, color: Color) -> Optional[Square]:
        king_symbol = "K" if color == "white" else "k"
        for row in range(8):
            for col in range(8):
                if self._grid[row][col] == king_symbol:
                    return row, col
        return None

    def is_in_check(self, color: Color) -> bool:
        """Return True if the king of the given color is in check."""

        king_sq = self._find_king(color)
        if king_sq is None:
            # No king found; treat as check for safety
            return True
        opponent = self.opposite(color)
        for move in self._generate_pseudo_moves(opponent):
            if move.to_sq == king_sq:
                return True
        return False

    def is_checkmate(self, color: Color) -> bool:
        return self.is_in_check(color) and len(self.generate_legal_moves(color)) == 0

    def is_stalemate(self, color: Color) -> bool:
        return not self.is_in_check(color) and len(self.generate_legal_moves(color)) == 0

    # -----------------------------------------------------------------------------------------------------------------
    # Display helpers
    # -----------------------------------------------------------------------------------------------------------------

    def to_ascii(self) -> str:
        """Return a simple ASCII representation of the board."""

        lines: List[str] = []
        for row in range(8):
            rank = 8 - row
            row_pieces: List[str] = []
            for col in range(8):
                piece = self._grid[row][col]
                row_pieces.append(piece if piece is not None else ".")
            lines.append(f"{rank}  {' '.join(row_pieces)}")
        lines.append("   a b c d e f g h")
        return "\n".join(lines)

    def __str__(self) -> str:  # pragma: no cover - for convenience
        return self.to_ascii()