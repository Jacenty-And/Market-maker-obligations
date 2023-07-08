# Market-maker-obligations
Calculate the percentage of time in which the market maker is fulfilling his obligations.

---

#### Market maker obligations:
- the spread (difference between best buy price and min sell price) should maximally be 0.003
- both bid amount and ask amount should be at least 5
- delta should maximally be 0.7

---

#### Data:
*order_events.json*
```
[
  {
    "timestamp": 1688077800000,
    "order_id": "1",
    "order_state": "open",
    "direction": "buy",
    "price": 0.9995,
    "amount": 4.2
  },
  {
    "timestamp": 1688077800000,
    "order_id": "2",
    "order_state": "open",
    "direction": "sell",
    "price": 1.0015,
    "amount": 4.6
  },
  .
  .
  .
  {
    "timestamp": 1688160600000,
    "order_id": "79",
    "order_state": "open",
    "direction": "sell",
    "price": 1.002,
    "amount": 3.7
  }
]
```  

*instrument_events.json*
```
[
  {
    "timestamp": "1688076000000",
    "delta": "0.4"
  },
  {
    "timestamp": "1688079600000",
    "delta": "0.5"
  },
  .
  .
  .
  {
    "timestamp": "1688155200000",
    "delta": "0.3"
  }
]
```
