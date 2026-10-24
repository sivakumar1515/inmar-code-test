"""ATM cash dispenser that pays an amount using the fewest available notes."""

import sys


class ATM:
    def __init__(self, inventory):
        """inventory: dict of {denomination: number_of_notes}, e.g. {500: 8, 200: 10}."""
        if not isinstance(inventory, dict) or not inventory:
            raise ValueError("ATM inventory must be a non-empty dictionary")
        for note, count in inventory.items():
            if not _is_int(note) or note <= 0:
                raise ValueError(f"Invalid denomination: {note!r}")
            if not _is_int(count) or count < 0:
                raise ValueError(f"Invalid note quantity for {note}: {count!r}")
        self.inventory = dict(inventory)

    def dispense(self, amount):
        """Return {denomination: notes} for the withdrawal, or None if it cannot be paid.

        The inventory is only updated when the withdrawal succeeds.
        """
        if not _is_int(amount):
            raise ValueError("Withdrawal amount must be a whole number")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero")

        result = find_min_notes(amount, self.inventory)
        if result is None:
            return None

        for note, count in result.items():
            self.inventory[note] -= count
        return result


def find_min_notes(amount, inventory):
    """Find the combination with the fewest notes that adds up to amount.

    Dynamic programming: best[total] holds the cheapest known way to make
    `total` using the denominations processed so far. Each denomination is
    tried 0..available times, so limited stock is respected and, unlike a
    greedy approach, every reachable total is considered.
    """
    best = {0: {}}
    for note, available in inventory.items():
        new_best = {}
        for total, notes in best.items():
            for used in range(available + 1):
                new_total = total + note * used
                if new_total > amount:
                    break
                candidate = {**notes, note: used}
                if new_total not in new_best or _count(candidate) < _count(new_best[new_total]):
                    new_best[new_total] = candidate
        best = new_best

    if amount not in best:
        return None
    return {note: used for note, used in best[amount].items() if used > 0}


def _count(notes):
    return sum(notes.values())


def _is_int(value):
    # bool is a subclass of int, but True/False are not valid amounts or notes
    return isinstance(value, int) and not isinstance(value, bool)


def main():
    inventory = {500: 8, 200: 10, 100: 20}
    atm = ATM(inventory)
    print(f"Inventory: {atm.inventory}")

    for arg in sys.argv[1:] or ["2700"]:
        try:
            amount = int(arg) if arg.lstrip("-").isdigit() else arg
            result = atm.dispense(amount)
        except ValueError as error:
            print(f"Withdraw {arg}: Error - {error}")
            continue
        if result is None:
            print(f"Withdraw {arg}: Cannot dispense requested amount")
        else:
            print(f"Withdraw {arg}: {result} (Total notes dispensed: {_count(result)})")
        print(f"Inventory: {atm.inventory}")


if __name__ == "__main__":
    main()
