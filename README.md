# Vending-Machine-Controller

###Group members
Sidrah Hashmi - 100915053
Xaiver Leung - 101010662

###Selected Option
Option 3 - Vending Machine Controller

###Overview

This project implements a small, finite-state-machie (FSM) based controller for a vending machine. The controller manages item selection, payment collection, insufficient/overpaid payment handling, dispensing, chane return, and simple invalid-input/out-of-stock error handling.

The FSM has 5 states (IDLE, ITEM_SELECTED, DISPENSING, RETURN_CHANGE, ERROR) and is driven by 4 external inputs (select, insert_coin, cancel, acknowledge).

###How it works
