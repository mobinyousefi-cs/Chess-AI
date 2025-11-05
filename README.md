# Game of Chess AI

A clean, testable Python implementation of a chess engine with a command-line interface and a simple AI opponent based on minimax with alpha–beta pruning.

The goal of this project is to provide:

- A readable and well-structured implementation of chess rules
- A pluggable evaluation function and search algorithm
- A simple CLI so you can play against the engine
- A solid foundation for experimenting with stronger AI ideas (iterative deepening, transposition tables, opening books, etc.)

> **Note**  
> For simplicity, this first version does **not** implement castling or en passant. Promotion, check, checkmate and stalemate are supported.

---

## Project Structure

```text
.
├── LICENSE
├── README.md
├── pyproject.toml
├── .gitignore
├── .editorconfig
├── .github
│   └── workflows
│       └── ci.yml
├── src
│   └── chess_ai
│       ├── __init__.py
│       ├── board.py
│       ├── ai.py
│       ├── game.py
│       └── main.py
└── tests
    ├── test_board.py
    └── test_ai.py
```

---

## Installation

You can install the project in editable/development mode:

```bash
# Clone your repo first, then inside the project root
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -e .[dev]
```

This will install the package along with development dependencies (pytest, black, ruff).

---

## Usage

### Play from the command line

After installation (or from the cloned repo with the virtual environment active):

```bash
python -m chess_ai.main
```

You will see an ASCII board and be prompted for moves. Enter moves in long algebraic format, e.g.:

- `e2e4`
- `g1f3`

The engine will respond with its own move. Type `quit` to exit.

### Change search depth

By default, the engine uses a moderate depth suitable for a laptop. You can change it with the `--depth` flag:

```bash
python -m chess_ai.main --depth 2   # faster, weaker
python -m chess_ai.main --depth 4   # slower, stronger
```

---

## Running Tests

```bash
pytest
```

---

## Extending the Engine

Some ideas for extending this project:

- Add **castling** and **en passant**
- Implement **iterative deepening** with a time budget
- Add **transposition tables** (hash-based caching)
- Implement a simple **opening book**
- Experiment with **different evaluation functions**, e.g. mobility, king safety, pawn structure

This repository is designed so that you can replace or wrap `chess_ai.ai.find_best_move` with alternative algorithms.

---

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.