"""
Vending Machine Controller
INFR 2810U - Computer Architecture Final Project
"""

from enum import Enum, auto
from dataclasses import dataclass


class State(Enum):
    IDLE = auto()
    ITEM_SELECTED = auto()
    DISPENSING = auto()
    RETURN_CHANGE = auto()
    ERROR = auto()


@dataclass
class Product:
    name: str
    price: int
    qty: int


class VendingMachine:
    def __init__(self):
        self.inventory = {
            "A1": Product("Chips", 150, 3),
            "A2": Product("Chocolate Bar", 175, 2),
            "B1": Product("Soda", 200, 0),
            "B2": Product("Water", 125, 5),
        }
        self.state = State.IDLE
        self.balance = 0
        self.selected_code = None
        self.log = []

    def _emit(self, message):
        self.log.append(message)
        print(message)

    def _reset_transaction(self):
        self.balance = 0
        self.selected_code = None
        self.state = State.IDLE

    def select(self, code):
        if self.state not in (State.IDLE,):
            self._emit(f"[IGNORED] Cannot select '{code}' while in state {self.state.name}.")
            return

        product = self.inventory.get(code)
        if product is None:
            self.state = State.ERROR
            self._emit(f"[ERROR] Invalid selection '{code}'.")
            return

        if product.qty <= 0:
            self._emit(f"[SOLD OUT] '{product.name}' ({code}) is currently out of stock. Please choose another item.")
            return

        self.selected_code = code
        self.state = State.ITEM_SELECTED
        self._emit(f"[SELECTED] {product.name} ({code}) - price ${product.price/100:.2f}. Please insert payment.")

    def insert_coin(self, value):
        if self.state != State.ITEM_SELECTED:
            self._emit(f"[IGNORED] Cannot insert coin in state {self.state.name}. Select an item first.")
            return

        if value <= 0:
            self.state = State.ERROR
            self._emit(f"[ERROR] Invalid coin value: {value}.")
            return

        self.balance += value
        product = self.inventory[self.selected_code]
        self._emit(f"[PAYMENT] Inserted ${value/100:.2f}. Balance: ${self.balance/100:.2f} / ${product.price/100:.2f}")

        if self.balance >= product.price:
            self.state = State.DISPENSING
            self._dispense()

    def cancel(self):
        if self.state in (State.ITEM_SELECTED,):
            refund = self.balance
            self._emit(f"[CANCELLED] Transaction cancelled. Returning ${refund/100:.2f}.")
            self._reset_transaction()
        elif self.state == State.ERROR:
            self._emit("[IGNORED] Use acknowledge() to clear an ERROR state.")
        else:
            self._emit(f"[IGNORED] Nothing to cancel in state {self.state.name}.")

    def acknowledge(self):
        if self.state == State.ERROR:
            self._emit("[RECOVERED] Error cleared. Returning to IDLE.")
            self._reset_transaction()
        else:
            self._emit(f"[IGNORED] acknowledge() only applies in ERROR state (currently {self.state.name}).")

    def _dispense(self):
        product = self.inventory[self.selected_code]
        product.qty -= 1
        self._emit(f"[DISPENSE] Dispensing {product.name}. Remaining stock: {product.qty}.")

        change = self.balance - product.price
        self.balance = 0

        if change > 0:
            self.state = State.RETURN_CHANGE
            self._return_change(change)
        else:
            self._reset_transaction()
            self._emit("[DONE] Thank you for your purchase!")

    def _return_change(self, change):
        self._emit(f"[CHANGE] Returning ${change/100:.2f} in change.")
        self._reset_transaction()
        self._emit("[DONE] Thank you for your purchase!")

    def status(self):
        return {
            "state": self.state.name,
            "balance_cents": self.balance,
            "selected": self.selected_code,
        }


def run_cli():
    vm = VendingMachine()
    print("Vending Machine Controller - type 'help' for commands, 'quit' to exit.")
    print("Available items:")
    for code, p in vm.inventory.items():
        print(f"  {code}: {p.name} - ${p.price/100:.2f} (qty: {p.qty})")

    while True:
        cmd = input("\n> ").strip().split()
        if not cmd:
            continue
        action = cmd[0].lower()

        if action == "quit":
            break
        elif action == "help":
            print("Commands: select <code> | coin <cents> | cancel | ack | status | quit")
        elif action == "select" and len(cmd) == 2:
            vm.select(cmd[1].upper())
        elif action == "coin" and len(cmd) == 2:
            vm.insert_coin(int(cmd[1]))
        elif action == "cancel":
            vm.cancel()
        elif action == "ack":
            vm.acknowledge()
        elif action == "status":
            print(vm.status())
        else:
            print("Unrecognized command. Type 'help'.")


if __name__ == "__main__":
    run_cli()