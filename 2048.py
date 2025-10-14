#!/usr/bin/env python3
"""
2048 (single-selected-tile movement) - Tkinter

Behavior changes vs classic 2048:
 - User selects exactly one tile (click/tap). Only that tile will move when the user issues
   a direction (arrow keys / WASD / swipe).
 - The selected tile moves along the direction as far as possible into empty cells,
   and will merge with a same-valued tile (single merge per move).
 - Swipe (touch/mouse drag) is supported for mobile-like interaction.
 - Small options UI: change board size, enable/disable swipe, restart.

Run:
    python 2048_single_select.py
"""
import tkinter as tk
from tkinter import messagebox
import random
import copy
import sys

# -------------------------
# Configuration (defaults)
# -------------------------
BOARD_SIZE = 4      # default board size
TARGET = 100      # win target

# -------------------------
# Utility / game logic
# -------------------------
def new_board(n):
    return [[0 for _ in range(n)] for _ in range(n)]

def add_random_tile(board):
    b = board
    empty = [(r, c) for r in range(len(b)) for c in range(len(b)) if b[r][c] == 0]
    if not empty:
        return b
    r, c = random.choice(empty)
    b[r][c] = 4 if random.random() < 0.1 else 2
    return b

def board_equal(a, b):
    return all(a[r][c] == b[r][c] for r in range(len(a)) for c in range(len(a)))

def transpose(board):
    n = len(board)
    return [[board[c][r] for c in range(n)] for r in range(n)]

def reverse_rows(board):
    return [list(reversed(row)) for row in board]

def any_moves_possible(board):
    n = len(board)
    # empty exists
    for r in range(n):
        for c in range(n):
            if board[r][c] == 0:
                return True
    # adjacent equals horizontally or vertically
    for r in range(n):
        for c in range(n):
            if c+1 < n and board[r][c] == board[r][c+1]:
                return True
            if r+1 < n and board[r][c] == board[r+1][c]:
                return True
    return False

def reached_target(board, target=TARGET):
    return any(board[r][c] >= target for r in range(len(board)) for c in range(len(board)))

# -------------------------
# GUI + Single-tile move logic
# -------------------------
class Game2048Single:
    TILE_COLORS = {
        0: ("#cdc1b4", "#776e65"),
        2: ("#eee4da", "#776e65"),
        4: ("#ede0c8", "#776e65"),
        8: ("#f2b179", "#f9f6f2"),
        16: ("#f59563", "#f9f6f2"),
        32: ("#f67c5f", "#f9f6f2"),
        64: ("#f65e3b", "#f9f6f2"),
        128: ("#edcf72", "#f9f6f2"),
        256: ("#edcc61", "#f9f6f2"),
        512: ("#edc850", "#f9f6f2"),
        1024:("#edc53f", "#f9f6f2"),
        2048:("#edc22e", "#f9f6f2"),
    }

    def __init__(self, master, size=4):
        self.master = master
        self.size = size
        self.score = 0
        self.best_score = 0
        self.selected = None  # (r,c) or None
        self.swipe_enabled = True
        self._drag_start = None
        self._init_ui()
        self.reset_game()

    def _init_ui(self):
        self.master.title("2048 - Single Selected Tile")
        self.master.resizable(False, False)

        # Top options frame
        top = tk.Frame(self.master)
        top.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew")

        self.score_label = tk.Label(top, text="Score: 0", font=("Helvetica", 14))
        self.score_label.pack(side="left", padx=(0,10))

        self.best_label = tk.Label(top, text="Best: 0", font=("Helvetica", 14))
        self.best_label.pack(side="left", padx=(0,10))

        restart_btn = tk.Button(top, text="Restart", command=self.reset_game)
        restart_btn.pack(side="left", padx=(0,8))

        tk.Label(top, text="Board size:").pack(side="left")
        self.size_var = tk.StringVar(value=str(self.size))
        self.size_entry = tk.Entry(top, width=3, textvariable=self.size_var)
        self.size_entry.pack(side="left", padx=(4,8))

        apply_btn = tk.Button(top, text="Apply", command=self.apply_options)
        apply_btn.pack(side="left", padx=(0,8))

        self.swipe_var = tk.IntVar(value=1)
        swipe_cb = tk.Checkbutton(top, text="Enable Swipe", variable=self.swipe_var, command=self.toggle_swipe)
        swipe_cb.pack(side="left", padx=(0,8))

        # Info label
        info = tk.Label(self.master, text="Click/tap a tile to select it. Use arrow keys / WASD or swipe to move that tile.", font=("Helvetica", 9))
        info.grid(row=2, column=0, padx=10, sticky="w")

        # Board frame
        self.board_frame = tk.Frame(self.master, bg="#bbada0", bd=3)
        self.board_frame.grid(row=1, column=0, padx=10, pady=8)
        self.tiles = [[None]*self.size for _ in range(self.size)]
        self._create_tiles()

        # Bind keys
        self.master.bind("<Left>", lambda e: self.handle_move("Left"))
        self.master.bind("<Right>", lambda e: self.handle_move("Right"))
        self.master.bind("<Up>", lambda e: self.handle_move("Up"))
        self.master.bind("<Down>", lambda e: self.handle_move("Down"))
        # WASD
        self.master.bind("a", lambda e: self.handle_move("Left"))
        self.master.bind("d", lambda e: self.handle_move("Right"))
        self.master.bind("w", lambda e: self.handle_move("Up"))
        self.master.bind("s", lambda e: self.handle_move("Down"))

        # Mouse/touch bindings for swipe detection on the board frame
        self.board_frame.bind("<Button-1>", self._on_press)
        self.board_frame.bind("<B1-Motion>", self._on_drag)
        self.board_frame.bind("<ButtonRelease-1>", self._on_release)

    def _create_tiles(self):
        # destroy existing labels if size changed
        for child in self.board_frame.winfo_children():
            child.destroy()
        self.tiles = [[None]*self.size for _ in range(self.size)]
        for r in range(self.size):
            for c in range(self.size):
                lbl = tk.Label(self.board_frame, text="", width=6, height=3, font=("Helvetica", 24, "bold"),
                               relief="raised", bd=6)
                lbl.grid(row=r, column=c, padx=6, pady=6)
                lbl.bind("<Button-1>", lambda e, rr=r, cc=c: self.select_tile(rr, cc))
                self.tiles[r][c] = lbl

    def apply_options(self):
        # apply board size if valid
        try:
            val = int(self.size_var.get())
            if val >= 2 and val <= 8:
                self.size = val
                self._create_tiles()
                self.reset_game()
            else:
                messagebox.showinfo("Invalid size", "Board size must be between 2 and 8.")
        except Exception:
            messagebox.showinfo("Invalid input", "Please enter a valid number for board size (2-8).")

    def toggle_swipe(self):
        self.swipe_enabled = bool(self.swipe_var.get())

    def reset_game(self):
        self.board = new_board(self.size)
        add_random_tile(self.board)
        add_random_tile(self.board)
        self.score = 0
        self.selected = None
        self.update_gui()

    def update_gui(self):
        for r in range(self.size):
            for c in range(self.size):
                val = self.board[r][c]
                txt = "" if val == 0 else str(val)
                lbl = self.tiles[r][c]
                bg, fg = self.TILE_COLORS.get(val, ("#3c3a32", "#f9f6f2"))
                lbl.config(text=txt, bg=bg, fg=fg)
                # highlight if selected
                if self.selected == (r, c):
                    lbl.config(relief="solid", bd=8, highlightthickness=4)
                else:
                    lbl.config(relief="raised", bd=6, highlightthickness=0)
        self.score_label.config(text=f"Score: {self.score}")
        if self.score > self.best_score:
            self.best_score = self.score
        self.best_label.config(text=f"Best: {self.best_score}")
        self.master.update_idletasks()

    def select_tile(self, r, c):
        if self.board[r][c] == 0:
            # selecting empty tile deselects
            self.selected = None
        else:
            self.selected = (r, c)
        self.update_gui()

    # -------------------------
    # Single tile movement
    # -------------------------
    def handle_move(self, direction):
        if direction not in ("Left", "Right", "Up", "Down"):
            return
        if not self.selected:
            # nothing selected
            return
        moved, gained = self.move_selected(direction)
        if not moved:
            return
        self.score += gained
        add_random_tile(self.board)
        self.update_gui()

        if reached_target(self.board):
            messagebox.showinfo("2048", f"Congratulations! You reached {TARGET}.")
        elif not any_moves_possible(self.board):
            self.update_gui()
            messagebox.showinfo("Game Over", "No more moves available. Game over!")
            if messagebox.askyesno("Restart", "Do you want to restart the game?"):
                self.reset_game()

    def move_selected(self, direction):
        """
        Move ONLY the selected tile in direction until blocked or merge.
        Returns (moved_bool, gained_score)
        """
        if not self.selected:
            return False, 0
        r, c = self.selected
        val = self.board[r][c]
        if val == 0:
            return False, 0

        dr, dc = 0, 0
        if direction == "Left":
            dr, dc = 0, -1
        elif direction == "Right":
            dr, dc = 0, 1
        elif direction == "Up":
            dr, dc = -1, 0
        elif direction == "Down":
            dr, dc = 1, 0

        n = self.size
        cr, cc = r, c
        moved = False
        gained = 0
        merged_this_move = False

        # attempt to slide step by step
        while True:
            nr, nc = cr + dr, cc + dc
            if not (0 <= nr < n and 0 <= nc < n):
                break
            if self.board[nr][nc] == 0:
                # move into empty
                self.board[nr][nc] = self.board[cr][cc]
                self.board[cr][cc] = 0
                cr, cc = nr, nc
                moved = True
                continue
            # occupied
            if self.board[nr][nc] == self.board[cr][cc] and not merged_this_move:
                # merge
                self.board[nr][nc] *= 2
                gained += self.board[nr][nc]
                self.board[cr][cc] = 0
                cr, cc = nr, nc
                moved = True
                merged_this_move = True
            # blocked (either can't merge or already merged)
            break

        # update selected to new position if moved, else keep original but deselect if zero
        if moved:
            # find new position of original tile (it is at cr,cc after moves)
            if self.board[cr][cc] == 0:
                self.selected = None
            else:
                self.selected = (cr, cc)
        else:
            # no movement -> keep selection
            pass

        return moved, gained

    # -------------------------
    # Swipe handling (mouse/touch)
    # -------------------------
    def _on_press(self, event):
        if not self.swipe_enabled:
            return
        # record start coords
        self._drag_start = (event.x_root, event.y_root)

    def _on_drag(self, event):
        # nothing required while dragging
        pass

    def _on_release(self, event):
        if not self.swipe_enabled or not self._drag_start:
            self._drag_start = None
            return
        sx, sy = self._drag_start
        ex, ey = event.x_root, event.y_root
        dx = ex - sx
        dy = ey - sy
        self._drag_start = None
        # threshold
        threshold = 30
        if abs(dx) < threshold and abs(dy) < threshold:
            # treat as tap: select tile under mouse if any
            # convert event coordinates to widget grid cell
            widget = event.widget
            # find which tile label is under pointer by coordinates
            x_local = widget.winfo_pointerx() - widget.winfo_rootx()
            y_local = widget.winfo_pointery() - widget.winfo_rooty()
            # compute approximate column/row by label sizes
            # we iterate tiles and check bbox
            for r in range(self.size):
                for c in range(self.size):
                    lbl = self.tiles[r][c]
                    try:
                        x1 = lbl.winfo_x()
                        y1 = lbl.winfo_y()
                        w = lbl.winfo_width()
                        h = lbl.winfo_height()
                    except Exception:
                        continue
                    if x_local >= x1 and x_local <= x1 + w and y_local >= y1 and y_local <= y1 + h:
                        self.select_tile(r, c)
                        return
            return

        # determine primary direction
        if abs(dx) > abs(dy):
            # horizontal swipe
            if dx > 0:
                self.handle_move("Right")
            else:
                self.handle_move("Left")
        else:
            if dy > 0:
                self.handle_move("Down")
            else:
                self.handle_move("Up")

# -------------------------
# Run
# -------------------------
def main():
    size = BOARD_SIZE
    # Optional: allow passing size via CLI
    if len(sys.argv) > 1:
        try:
            size_arg = int(sys.argv[1])
            if size_arg >= 2:
                size = size_arg
        except Exception:
            pass

    root = tk.Tk()
    game = Game2048Single(root, size=size)
    root.mainloop()

if __name__ == "__main__":
    main()
