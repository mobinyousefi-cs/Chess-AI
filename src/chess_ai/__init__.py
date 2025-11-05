#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================================================================
Project: Game of Chess AI
File: __init__.py
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi-cs)
Created: 2025-11-05
Updated: 2025-11-05
License: MIT License (see LICENSE file for details)
=

Description:
Package initialization for the Game of Chess AI project. Exposes package-level metadata and a
convenience function for launching the command-line interface.

Usage:
from chess_ai import __version__, run_cli

Notes:
- The CLI entry point is implemented in `chess_ai.main`.
=================================================================================================================
"""

from __future__ import annotations

from .main import run_cli

__all__ = ["__version__", "run_cli"]

__version__ = "0.1.0"