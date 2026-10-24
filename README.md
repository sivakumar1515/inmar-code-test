# ATM Cash Dispenser

Simulates an ATM that pays a withdrawal using the **minimum number of notes**
from a limited inventory. Python 3, standard library only.

## Files

- `atm.py` – the `ATM` class, the note-selection algorithm and a small command-line demo
- `test_atm.py` – unit tests (`unittest`)

## Usage

```python
from atm import ATM

atm = ATM({500: 8, 200: 10, 100: 20})
atm.dispense(2700)   # -> {500: 5, 200: 1}
atm.inventory        # -> {500: 3, 200: 9, 100: 20}
atm.dispense(50)     # -> None (Cannot dispense requested amount)
```

- `dispense(amount)` returns a dict `{denomination: notes}` on success, or `None`
  if the amount cannot be paid exactly with the notes available.
- Invalid input (zero, negative or non-numeric amount; negative note quantity;
  invalid denomination; empty inventory) raises `ValueError` with a clear message.
- The inventory is only updated after a successful withdrawal. A failed
  withdrawal leaves it unchanged.

## Running the program

```bash
python3 atm.py                 # withdraws 2700 from the sample inventory
python3 atm.py 2700 300 abc 0  # runs several withdrawals one after another
```

## Running the tests

```bash
python3 -m unittest -v
```

## Approach

Always taking the largest note first (greedy) can fail. For example, with
`{4: 1, 3: 2}` and an amount of 6, taking the 4 leaves 2, which cannot be paid.
The correct answer is `{3: 2}`.

So the solution uses **dynamic programming** instead:

1. Start with `best = {0: {}}`, meaning a total of 0 needs no notes.
2. For each denomination, extend every known total by using that note
   0, 1, ... up to the number available, without going over the requested
   amount. For each new total, keep only the combination with the fewest notes.
3. After all denominations are processed, `best[amount]` is the minimum-note
   combination. If the amount was never reached, return `None`.

Because each denomination is limited to its stock, the ATM never dispenses
more notes than it has.

## Complexity

Let `A` = withdrawal amount, `D` = number of denominations, `C` = largest note count.

- **Time:** `O(D × A × C)`. For each denomination, every reachable total
  (at most `A + 1`) is extended up to `C` times.
- **Space:** `O(A × D)`. At most `A + 1` totals are stored, each with a small
  combination of up to `D` entries.
