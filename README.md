# Economic Revamp Script
<p align='center'>
<img src=https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue></img>
<img src=https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white></img>
</p>

### Prerequisites
```sh
pip install -r requirements.txt
```
- mariadb

### NOTES

Edit 'config.py' with the DB information.

Edit 'econ_revamp/items.py' if you wish to add OMMITTED items

When running the script, DO NOT open the log files during execution as data will not save!

### Usage:
```sh
./main.py
```

### PHASE 1

Refund all inventory items (except legacy) at a fixed percentage of market value

### PHASE 2

Decrease wallets using a tax bracket system as follows when the player has:
- Up to $199,999: 0% Decrease
- Between $200,000 and $499,999: 50% Decrease
- Between $500,000 and $749,999: 55% Decrease
- Between $750,000 and $999,999: 60% Decrease
- Between $1,000,000 and $4,999,999: 65% Decrease
- $5,000,000 or more: 70% Decrease

Descale wallets by a fixed number
