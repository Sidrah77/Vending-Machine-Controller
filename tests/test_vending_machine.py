import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vending_machine import VendingMachine, State


def header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def test_normal_purchase_exact_change():
    header("TEST 1: Normal purchase, exact change")
    vm = VendingMachine()
    vm.select("A2")                 # Chocolate Bar, $1.75
    vm.insert_coin(100)
    vm.insert_coin(75)
    assert vm.state == State.IDLE
    assert vm.inventory["A2"].qty == 1
    print("PASS")


def test_normal_purchase_with_change():
    header("TEST 2: Normal purchase, change returned")
    vm = VendingMachine()
    vm.select("B2")                 # Water, $1.25
    vm.insert_coin(200)
    assert vm.state == State.IDLE
    assert vm.inventory["B2"].qty == 4
    print("PASS")


def test_out_of_stock():
    header("TEST 3 (edge case): Selecting an out-of-stock item")
    vm = VendingMachine()
    vm.select("B1")                 # Soda, qty = 0
    assert vm.state == State.IDLE   # should remain idle, not crash
    print("PASS")


def test_invalid_selection():
    header("TEST 4 (edge case): Invalid item code")
    vm = VendingMachine()
    vm.select("Z9")
    assert vm.state == State.ERROR
    vm.acknowledge()
    assert vm.state == State.IDLE
    print("PASS")


def test_cancel_refunds_balance():
    header("TEST 5 (edge case): Cancel mid-transaction")
    vm = VendingMachine()
    vm.select("A1")
    vm.insert_coin(50)
    vm.cancel()
    assert vm.state == State.IDLE
    assert vm.balance == 0
    assert vm.inventory["A1"].qty == 3  # unchanged, no item dispensed
    print("PASS")


def test_insert_coin_without_selection():
    header("TEST 6 (edge case): Insert coin before selecting an item")
    vm = VendingMachine()
    vm.insert_coin(100)
    assert vm.state == State.IDLE
    assert vm.balance == 0
    print("PASS")


def test_insufficient_then_sufficient_payment():
    header("TEST 7: Insufficient payment, then top-up completes purchase")
    vm = VendingMachine()
    vm.select("A1")                 # Chips, $1.50
    vm.insert_coin(50)
    assert vm.state == State.ITEM_SELECTED  # not enough yet
    vm.insert_coin(100)
    assert vm.state == State.IDLE           # completed
    print("PASS")


if __name__ == "__main__":
    test_normal_purchase_exact_change()
    test_normal_purchase_with_change()
    test_out_of_stock()
    test_invalid_selection()
    test_cancel_refunds_balance()
    test_insert_coin_without_selection()
    test_insufficient_then_sufficient_payment()
    print("\nAll tests passed.")