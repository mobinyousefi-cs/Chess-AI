#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: Game of Chess AI
File: test_board.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-05
Updated: 2025-11-05
License: MIT License (see LICENSE file for details)
=

Description:
Pytest-based unit tests for the Board class, focusing on FEN round-tripping and basic move
generation properties.

Usage:
pytest tests/test_board.py
=================================================================================================================
"""

from __future__ import annotations

from chess_ai.board import Board


def test_start_position_fen_roundtrip() -> None:
    board = Board.start_position()
    fen = board.to_fen()
    board2 = Board.from_fen(fen)
    assert board2.to_fen() == fen


def test_start_position_side_to_move() -> None:
    board = Board.start_position()
    assert board.turn == "white"


def test_start_position_legal_moves_white_has_20() -> None:
    board = Board.start_position()
    moves = board.generate_legal_moves("white")
    # In a standard chess starting position, White has 20 legal moves
    assert len(moves) == 20


def test_simple_pawn_push() -> None:
    board = Board.start_position()
    # e2e4 should be legal
    from chess_ai.board import Move

    move = Move.from_long_algebraic("e2e4")
    legal_moves = board.generate_legal_moves("white")
    assert any(m.from_sq == move.from_sq and m.to_sq == move.to_sq for m in legal_moves)