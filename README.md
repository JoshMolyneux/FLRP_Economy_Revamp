# Economic Revamp Script

### Prerequisites
```sh
pip install -r requirements.txt
```
- mariadb

### Usage: 
```sh
./main.py
```

### PHASE 1

Refund all inventory items (except legacy) at 60% market value.

### PHASE 2

Decrease wallets using a tax bracket system as follows when the player has:
- Up to $199,999: 0% Decrease
- Between $200,000 and $499,999: 50% Decrease
- Between $500,000 and $749,999: 55% Decrease
- Between $750,000 and $999,999: 60% Decrease
- Between $1,000,000 and $4,999,999: 65% Decrease
- $5,000,000 or more: 70% Decrease
    
### PHASE 3

Descale wallets by a fixed number.
