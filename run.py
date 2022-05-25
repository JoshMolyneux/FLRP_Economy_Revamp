"""Automates queries sent to the database to complete the following:
- Refund all inventory items at 60% market value.
- Decrease wallets using a tax bracket system as follows when the player has:
    - Up to $199,999: 0% Decrease
    - Between $200,000 and $499,999: 50% Decrease
    - Between $500,000 and $749,999: 55% Decrease
    - Between $750,000 and $999,999: 60% Decrease
    - Between $1,000,000 and $4,999,999: 65% Decrease
    - $5,000,000 or more: 70% Decrease
- Descale wallets by a fixed number

Usage:
    ./run.py

Author:
    Joshua Molyneux - 05-2022
"""
