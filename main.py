"""Automates queries sent to the database to complete the following:
- PHASE 1 Refund all inventory items (except legacy) at FIXED% market value.
- PHASE 2 Decrease wallets using a tax bracket system as follows when the player has.
    - Up to $199,999: 0% Decrease
    - Between $200,000 and $499,999: 50% Decrease
    - Between $500,000 and $749,999: 55% Decrease
    - Between $750,000 and $999,999: 60% Decrease
    - Between $1,000,000 and $4,999,999: 65% Decrease
    - $5,000,000 or more: 70% Decrease
- PHASE 3 Descale wallets by a FIXED number

Usage:
    ./main.py

Author:
    Joshua Molyneux - 05-2022
    https://fearlessrp.net/member.php?action=profile&uid=17825
    Discord: @Awestruck#3143
"""

from econ_revamp import phase1,\
    phase2, set_inv_value_to_zero,\
    create_verification_db_columns


if __name__ == '__main__':
    create_verification_db_columns()
    # Run our phases
    phase1.main()
    phase2.main()
    set_inv_value_to_zero()
    input()
