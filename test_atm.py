import unittest

from atm import ATM


class DispenseTests(unittest.TestCase):
    def test_example_from_spec(self):
        atm = ATM({500: 8, 200: 10, 100: 20})
        self.assertEqual(atm.dispense(2700), {500: 5, 200: 1})
        self.assertEqual(atm.inventory, {500: 3, 200: 9, 100: 20})

    def test_greedy_trap(self):
        atm = ATM({4: 1, 3: 2})
        self.assertEqual(atm.dispense(6), {3: 2})

    def test_uses_minimum_notes(self):
        atm = ATM({1: 10, 3: 10, 4: 10})
        self.assertEqual(atm.dispense(6), {3: 2})

    def test_respects_limited_stock(self):
        atm = ATM({500: 1, 100: 5})
        self.assertEqual(atm.dispense(1000), {500: 1, 100: 5})

    def test_cannot_dispense_leaves_inventory_unchanged(self):
        atm = ATM({500: 1, 200: 1})
        self.assertIsNone(atm.dispense(300))
        self.assertEqual(atm.inventory, {500: 1, 200: 1})

    def test_not_enough_money(self):
        atm = ATM({100: 2})
        self.assertIsNone(atm.dispense(300))
        self.assertEqual(atm.inventory, {100: 2})

    def test_repeated_withdrawals_drain_inventory(self):
        atm = ATM({100: 2})
        self.assertEqual(atm.dispense(200), {100: 2})
        self.assertIsNone(atm.dispense(100))

    def test_any_denominations_supported(self):
        atm = ATM({2000: 2, 50: 4, 10: 5})
        self.assertEqual(atm.dispense(2230), {2000: 1, 50: 4, 10: 3})


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.atm = ATM({500: 8, 200: 10, 100: 20})

    def test_zero_amount(self):
        with self.assertRaises(ValueError):
            self.atm.dispense(0)

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            self.atm.dispense(-100)

    def test_non_numeric_amount(self):
        for amount in ["abc", "100", None, 100.5, True]:
            with self.assertRaises(ValueError):
                self.atm.dispense(amount)

    def test_negative_note_quantity(self):
        with self.assertRaises(ValueError):
            ATM({500: -1})

    def test_invalid_denominations(self):
        for inventory in [{0: 5}, {-100: 5}, {"500": 5}, {50.5: 5}]:
            with self.assertRaises(ValueError):
                ATM(inventory)

    def test_empty_inventory(self):
        with self.assertRaises(ValueError):
            ATM({})


if __name__ == "__main__":
    unittest.main()
