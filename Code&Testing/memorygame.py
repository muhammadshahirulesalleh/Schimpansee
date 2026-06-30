import random
import tkinter as tk

# Colours
BLUE  = "#3b82f6"   # face down
RED   = "#ef4444"
GREEN = "#22c55e"

NUM_CARDS = 4
FLIP_BACK_DELAY = 800   # ms a non-matching pair stays visible before flipping back

# --- Game state ---
card_colours = []        # the hidden colour of each card (fixed for the whole game)
matched = []             # True once a card belongs to a found pair
flipped = []             # indices currently face up and not yet matched
busy = False             # ignore clicks while a non-matching pair flips back
previous_colours = None  # the layout from the previous game (to avoid repeating it)

root = tk.Tk()
root.title("Memory Cards")
root.configure(bg="#f4f4f5")


def on_card_click(i):
    global busy
    # ignore if locked, already matched, or already face up
    if busy or matched[i] or i in flipped:
        return

    cards[i].configure(bg=card_colours[i])   # flip this card face up
    flipped.append(i)

    if len(flipped) == 2:
        a, b = flipped
        if card_colours[a] == card_colours[b]:
            matched[a] = True                # match -> stay up
            matched[b] = True
            flipped.clear()
        else:
            busy = True                      # mismatch -> flip both back shortly
            root.after(FLIP_BACK_DELAY, flip_back)


def flip_back():
    global busy
    for i in flipped:
        cards[i].configure(bg=BLUE)
    flipped.clear()
    busy = False


def new_game():
    """Deal a fresh layout and turn every card face down.

    Only ever runs at start and on retry, so the layout stays fixed during a
    game. The new layout is guaranteed to differ from the previous game's.
    """
    global card_colours, matched, flipped, busy, previous_colours

    new_set = [RED, RED, GREEN, GREEN]
    if previous_colours is None:
        random.shuffle(new_set)
    else:
        # reshuffle until this deal is not identical to the previous one
        while True:
            random.shuffle(new_set)
            if new_set != previous_colours:
                break

    card_colours = new_set
    previous_colours = new_set.copy()   # remember for the next retry

    matched = [False] * NUM_CARDS
    flipped = []
    busy = False
    for card in cards:
        card.configure(bg=BLUE)


# --- Cards ---
board = tk.Frame(root, bg="#f4f4f5")
board.pack(padx=24, pady=(24, 16))

cards = []
for i in range(NUM_CARDS):
    card = tk.Frame(board, width=70, height=95, bg=BLUE, cursor="hand2")
    card.pack_propagate(False)
    card.pack(side="left", padx=8)
    card.bind("<Button-1>", lambda e, idx=i: on_card_click(idx))
    cards.append(card)

# --- Retry button ---
retry_btn = tk.Button(
    root, text="retry", command=new_game,
    font=("Helvetica", 12), relief="flat",
    bg="#e4e4e7", activebackground="#d4d4d8",
    padx=14, pady=4, cursor="hand2",
)
retry_btn.pack(pady=(0, 24))

new_game()       # randomize at start
root.mainloop()