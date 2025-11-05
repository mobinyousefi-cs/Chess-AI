#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: Game of Chess AI
File: ai.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-05
Updated: 2025-11-05
License: MIT License (see LICENSE file for details)
=

Description:
Implements a simple chess AI based on minimax search with alpha–beta pruning and a hand-crafted
static evaluation function.

Usage:
from chess_ai.ai import find_best_move
from chess_ai.board import Board

board = Board.start_position()
move = find_best_move(board, max_depth=3)

Notes:
- The evaluation function is intentionally simple but structured for easy experimentation.
- No transposition tables or advanced heuristics are used in this baseline implementation.
=================================================================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from .board import Board, Color, Move


@dataclass
class SearchResult:
    """Container for search results (best move and its score)."""

    move: Optional[Move]
    score: float


# Material values (in pawns)
PIECE_VALUES = {
    "P": 1.0,
    "N": 3.0,
    "B": 3.25,
    "R": 5.0,
    "Q": 9.0,
    "K": 0.0,  # King's value is implicit; losing it is game over
}


def evaluate_board(board: Board) -> float:
    """Evaluate a position from White's perspective.

    Positive values are good for White, negative values are good for Black.
    The current implementation uses a simple material count. You can extend this to include:

    - Piece-square tables
    - Mobility (number of legal moves)
    - King safety, pawn structure, etc.
    """

    material = 0.0
    for row in range(8):
        for col in range(8):
            piece = board.piece_at((row, col))
            if piece is None:
                continue
            base = PIECE_VALUES.get(piece.upper(), 0.0)
            if piece.isupper():
                material += base
            else:
                material -= base
    return material


def minimax(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    maximizing_color: Color,
) -> float:
    """Minimax search with alpha–beta pruning.

    Args:
        board: Current position.
        depth: Remaining search depth.
        alpha: Alpha bound.
        beta: Beta bound.
        maximizing_color: The color whose perspective we are optimizing (usually "white").
    """

    if depth == 0:
        score = evaluate_board(board)
        return score if maximizing_color == "white" else -score

    side_to_move = board.turn
    legal_moves = board.generate_legal_moves(side_to_move)

    if not legal_moves:
        # Checkmate or stalemate
        if board.is_in_check(side_to_move):
            # If the side to move is the maximizing side, this is very bad; otherwise it's very good.
            mate_score = -10_000.0 if side_to_move == maximizing_color else 10_000.0
            return mate_score
        # Stalemate -> draw
        return 0.0

    is_maximizing_player = side_to_move == maximizing_color

    if is_maximizing_player:
        value = float("-inf")
        for move in legal_moves:
            child = board.apply_move(move)
            value = max(value, minimax(child, depth - 1, alpha, beta, maximizing_color))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cut-off
        return value

    # Minimizing player
    value = float("inf")
    for move in legal_moves:
        child = board.apply_move(move)
        value = min(value, minimax(child, depth - 1, alpha, beta, maximizing_color))
        beta = min(beta, value)
        if beta <= alpha:
            break  # alpha cut-off
    return value


def find_best_move(board: Board, max_depth: int = 3) -> SearchResult:
    """Compute the best move for the side to move using minimax with alpha–beta pruning.

    Args:
        board: Position for which to find the best move.
        max_depth: Search depth (plies).

    Returns:
        SearchResult containing the chosen move and its evaluation score.
    """

    side_to_move = board.turn
    legal_moves = board.generate_legal_moves(side_to_move)
    if not legal_moves:
        # No moves available
        if board.is_in_check(side_to_move):
            score = -10_000.0 if side_to_move == "white" else 10_000.0
        else:
            score = 0.0
        return SearchResult(move=None, score=score)

    best_move: Optional[Move] = None
    if side_to_move == "white":
        best_score = float("-inf")
    else:
        best_score = float("inf")

    for move in legal_moves:
        child = board.apply_move(move)
        score = minimax(child, max_depth - 1, alpha=float("-inf"), beta=float("inf"), maximizing_color=side_to_move)

        if side_to_move == "white":
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move

    return SearchResult(move=best_move, score=best_score)