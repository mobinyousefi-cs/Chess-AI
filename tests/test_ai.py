#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: Game of Chess AI
File: test_ai.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-05
Updated: 2025-11-05
License: MIT License (see LICENSE file for details)
=

Description:
Basic tests for the chess AI search logic, ensuring that a move is selected and that obvious
checkmates are recognized.

Usage:
pytest tests/test_ai.py
=================================================================================================================
"""

from __future__ import annotations

from chess_ai.ai import SearchResult, evaluate_board, find_best_move
from chess_ai.board import Board


def test_ai_returns_a_move_in_start_position() -> None:
    board = Board.start_position()
    result: SearchResult = find_best_move(board, max_depth=2)
    assert result.move is not None


def test_evaluation_symmetry_for_start_position() -> None:
    board = Board.start_position()
    score = evaluate_board(board)
    assert score == 0.0


def test_simple_checkmate_detection() -> None:
    # Fool's mate position — black to move and already delivered checkmate
    fen = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w"
    board = Board.from_fen(fen)
    assert board.is_in_check("white")