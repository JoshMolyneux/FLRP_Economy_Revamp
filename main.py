"""Automates queries sent to the database to complete the following:
- PHASE 1 Refund all inventory items (except legacy) at 60% market value.
- PHASE 2 Decrease wallets using a tax bracket system as follows when the player has.
    - Up to $199,999: 0% Decrease
    - Between $200,000 and $499,999: 50% Decrease
    - Between $500,000 and $749,999: 55% Decrease
    - Between $750,000 and $999,999: 60% Decrease
    - Between $1,000,000 and $4,999,999: 65% Decrease
    - $5,000,000 or more: 70% Decrease
- PHASE 3 Descale wallets by a fixed number

Usage:
    ./main.py

Author:
    Joshua Molyneux - 05-2022
    https://fearlessrp.net/member.php?action=profile&uid=17825
    Discord: @Awestruck#3143
"""

from econ_revamp import phase1, phase2, phase3
import config
# import phase2
# import phase3


if __name__ == '__main__':
    # Run our phases
    phase1.main()
    # phase2(connect())
    # phase3(connect(), config.DESCALE_VALUE)

    # Print the total sum of money to the console
    # total = int(econ_revamp.TOTAL_CASH_START[0]) - int(TOTAL_CASH_END[0])
    # print(f"\n\n Total money BEFORE: ${int(TOTAL_CASH_START[0])}")
    # print(f"\n\n Total money AFTER: ${int(TOTAL_CASH_END[0])}")
    # print(f"\n\n Total money removed: ${total}")
    # connect().close()
