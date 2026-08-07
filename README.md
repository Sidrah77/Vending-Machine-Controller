# Vending-Machine-Controller

###Group members (INFR 2810)

Sidrah Hashmi - 100915053
Xaiver Leung - 101010662

###Selected Option

Option 3 - Vending Machine Controller

###Overview

This project implements a small, finite-state-machine (FSM) based controller for a vending machine. The controller manages item selection, payment collection, insufficient/overpaid payment handling, dispensing, change return, and simple invalid-input/out-of-stock error handling.

The FSM has 5 states (IDLE, ITEM_SELECTED, DISPENSING, RETURN_CHANGE, ERROR) and is driven by 4 external inputs (select, insert_coin, cancel, acknowledge).

###How it works

1. The machine starts in IDLE and displays the item menu
2. The customer selects an item with select(code)
- if the code is invalid, the machine enters ERROR
- if the item is out of stock, the machine stays in IDLE and asks for another choice
- otherwise it moves to ITEM_SELECTED and shows the price
3. The customer inserts coins with insert_coin(value). The balance accumulates --> once balance >= price, the machine moves to dispensing
4. DISPENSING releases the item and decrements inventory automatically. 
- if change is owed, the machine moves to RETURN_CHANGE and returns it
- then it returns to IDLE
5. The customer can cancel() at any point during ITEM_SELECTED to get a full refund without dispensing anything
6. ERROR can only be exited with acknowledge()

###How To Run

Requirements - Python 

Interactive demo:
cd src
anaconda3/python.exe vending_machine.py

Then use commands at the prompt:

select A1        # select item with code A1
coin 100         # insert a $1.00 coin (value is in cents)
cancel           # cancel current transaction
ack              # acknowledge/clear an error
status           # show current state
quit             # exit

Run automated tests
anaconda3/python.exe tests/test_vending_machine.py 

This runs 7 test cases (normal purchases + 5 edge cases) and prints PASS/FAIL for each.

###Design notes/simplification

-inventory is fixed at 4 items to keep the project manageable
- Money is tracked in integer cents to avoid floating-point rounding error
- "Dispensing" and "returning change" are modeled as automatic internal transitions rather than separate user-triggered inputs, since a real machine performs these immediately once payment is sufficient
