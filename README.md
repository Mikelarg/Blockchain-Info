BlockChain-Info
-
Get info about balance and transactions of multiple BTC addresses

Arguments
--
- addresses — type addresses here 
- *-b* or *--balance* — get info about balance of addresses
- *-i* or *--incoming* — get info about incoming transactions of addresses
- *-o* or *--outcoming* — get info about outcoming transactions of addresses
- *-f* or *--format* — set format of message about transactions. Parameters: {d} - for transaction date; {a} — for transaction address; {s} — for BTC value. Example "Transaction {s} completed {d} to address {a}"

**Example:**
```
python blockchain_explorer.py 3LPoGRbZzQMFciqoVPyxGRFd2opUZbZVWg 1Af7Fsc34TVe2T3WqnScm3K2d5RiCoLAa8  -i -o -b -f "Transaction {s} completed {d} to address {a}"
```

If no options are filled return 10 random BTC addresses with their balance.


Requirements
--
 **Python 2.7**
 
Installation
--
- ```pip install -r reqs.txt```
-  All Done!

*TODO*
--
Add Threadssssss