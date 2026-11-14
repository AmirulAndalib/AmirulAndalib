"""Noughts and crosses played through GitHub issues.

A visitor opens an issue titled "ttt|move|<cell>" (cell 1-9, left to right, top to
bottom). The workflow calls this script with that title in TTT_TITLE and the issue
author in TTT_PLAYER. The visitor plays X, the profile answers as O, and the board in
README.md between the TTT markers is redrawn. State lives in games/ttt.json.

    python scripts/game/ttt.py            # apply TTT_TITLE and redraw
    python scripts/game/ttt.py --render   # redraw only

The script prints one line for the issue comment and writes nothing outside the repo.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "games" / "ttt.json"
README = ROOT / "README.md"
START, END = "<!-- TTT:START -->", "<!-- TTT:END -->"
REPO = "AmirulAndalib/AmirulAndalib"
LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]
TITLE = re.compile(r"^ttt\|move\|([1-9])$")
LOGIN = re.compile(r"^[A-Za-z0-9-]{1,39}$")


def load() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {
        "board": "." * 9,
        "moves": [],
        "visitors": 0,
        "profile": 0,
        "draws": 0,
        "last": [],
    }


def save(state: dict) -> None:
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")


def winner(board: str) -> str | None:
    for a, b, c in LINES:
        if board[a] != "." and board[a] == board[b] == board[c]:
            return board[a]
    return None


def reply(board: str) -> int:
    """Pick O's move: win, block, centre, a corner, then any side."""
    free = [i for i, cell in enumerate(board) if cell == "."]
    for mark in ("O", "X"):
        for i in free:
            trial = board[:i] + mark + board[i + 1 :]
            if winner(trial) == mark:
                return i
    for i in (4, 0, 2, 6, 8, 1, 3, 5, 7):
        if i in free:
            return i
    raise ValueError("no free cell")


def place(board: str, i: int, mark: str) -> str:
    return board[:i] + mark + board[i + 1 :]


def finish(state: dict, result: str, player: str) -> str:
    key = {"X": "visitors", "O": "profile", "draw": "draws"}[result]
    state[key] += 1
    state["last"] = ([f"{result} vs @{player}"] + state["last"])[:5]
    state["board"] = "." * 9
    state["moves"] = []
    return {
        "X": "You won. New game started.",
        "O": "I won this one. New game started.",
        "draw": "Draw. New game started.",
    }[result]


def play(state: dict, title: str, player: str) -> str:
    match = TITLE.match(title.strip())
    if not match or not LOGIN.match(player):
        return "That move was not understood. Use the links on the profile to play."
    cell = int(match.group(1)) - 1
    board = state["board"]
    if board[cell] != ".":
        return f"Cell {cell + 1} is taken. Pick an empty one."
    board = place(board, cell, "X")
    state["moves"].append(f"@{player} X{cell + 1}")
    if winner(board) == "X":
        return finish(state, "X", player)
    if "." not in board:
        return finish(state, "draw", player)
    answer = reply(board)
    board = place(board, answer, "O")
    state["moves"].append(f"O{answer + 1}")
    state["board"] = board
    if winner(board) == "O":
        return finish(state, "O", player)
    if "." not in board:
        return finish(state, "draw", player)
    return f"You played {cell + 1}, I answered {answer + 1}. Your turn."


def cell_markdown(board: str, i: int) -> str:
    if board[i] == "X":
        return "❌"
    if board[i] == "O":
        return "⭕"
    title = quote(f"ttt|move|{i + 1}")
    body = quote("Just open this issue. A workflow plays the move and closes it.")
    return f"[⬜](https://github.com/{REPO}/issues/new?title={title}&body={body})"


def render(state: dict) -> str:
    b = state["board"]
    rows = [
        "| | | |",
        "|:-:|:-:|:-:|",
        *(
            "| " + " | ".join(cell_markdown(b, r * 3 + c) for c in range(3)) + " |"
            for r in range(3)
        ),
    ]
    recent = ", ".join(state["last"]) if state["last"] else "no finished games yet"
    return "\n".join(
        [
            START,
            "",
            "You are ❌. Click an empty square to open an issue with your move; a workflow plays",
            "⭕ in reply, redraws the board and closes the issue.",
            "",
            *rows,
            "",
            (
                f"Visitors {state['visitors']} · profile {state['profile']}"
                f" · draws {state['draws']} · recent: {recent}"
            ),
            "",
            END,
        ]
    )


def write_readme(state: dict) -> None:
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit("README.md has no TTT markers")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    README.write_text(head + render(state) + tail, encoding="utf-8", newline="\n")


def main() -> None:
    state = load()
    if "--render" not in sys.argv:
        message = play(
            state, os.environ.get("TTT_TITLE", ""), os.environ.get("TTT_PLAYER", "")
        )
        print(message)
    save(state)
    write_readme(state)


if __name__ == "__main__":
    main()
