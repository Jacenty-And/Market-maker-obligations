from json import load
from datetime import datetime
from more_itertools import peekable


def order_events_generator():
    with open("order_events.json", "r") as file:
        events = load(file)
    for event in events:
        yield event


def instrument_events_generator():
    with open("instrument_events.json", "r") as file:
        events = load(file)
    for event in events:
        yield event


def update_active(order, active):
    if order["order_state"] == "open":
        active[order["order_id"]] = order
    else:  # order["order_state"] == "closed"
        active.pop(order["order_id"])


def get_active_list(active):
    return [item[1] for item in active.items()]


def split_by_direction(orders):
    buy = [order for order in orders if order["direction"] == "buy"]
    sell = [order for order in orders if order["direction"] == "sell"]
    return buy, sell


def convert_timestamp(timestamp):
    return datetime.fromtimestamp(int(timestamp) / 1000.0)


def is_spread_ok(orders):
    buy_orders, sell_orders = split_by_direction(orders)
    max_buy_price = max(buy_orders, key=lambda o: o["price"])["price"] if len(buy_orders) else 0
    min_sell_price = min(sell_orders, key=lambda o: o["price"])["price"] if len(sell_orders) else 0
    spread = abs(min_sell_price - max_buy_price)
    return spread <= 0.003


def is_amounts_ok(orders):
    buy_orders, sell_orders = split_by_direction(orders)
    buy_amount = sum(buy["amount"] for buy in buy_orders)
    sell_amount = sum(sell["amount"] for sell in sell_orders)
    return buy_amount >= 5 and sell_amount >= 5


def is_delta_ok(event):
    return float(event["delta"]) <= 0.7


def get_total_time(orders):
    start_time = orders[0]["timestamp"]
    end_time = orders[-1]["timestamp"]
    total_time = end_time - start_time
    return total_time


def calculate_time(timestamps):
    time = start = 0
    for timestamp in timestamps:
        if timestamp[0] is True and start == 0:
            start = timestamp[1]
        if timestamp[0] is False and start > 0:
            time += timestamp[1] - start
            start = 0
    if start > 0:
        time += timestamps[-1][1] - start
    return time


if __name__ == '__main__':
    order_events = order_events_generator()
    instrument_events = peekable(instrument_events_generator())
    event = next_event = next(instrument_events)
    active = {}
    obligations_fulfilled = []

    for order in order_events:
        update_active(order, active)

        print("Active:")
        active_orders = get_active_list(active)
        for act in active_orders:
            print(act)

        # Check instrument_events
        while order["timestamp"] >= int(next_event["timestamp"]):
            try:
                next_event = instrument_events.peek()
            except StopIteration:
                next_event = event
                break
            if int(next_event["timestamp"]) > order["timestamp"]:
                break
            event = next(instrument_events)

        print("Order timestamp: ", convert_timestamp(order["timestamp"]))
        print("Event timestamp: ", convert_timestamp(event["timestamp"]), "Delta: ", event["delta"])
        print("Next event timestamp: ", convert_timestamp(next_event["timestamp"]), "Delta: ", next_event["delta"])
        print("Delta: ", event["delta"])

        print("Spread: ", is_spread_ok(active_orders))
        print("Amounts: ", is_amounts_ok(active_orders))
        print("Delta: ", is_delta_ok(event))
        print("\n")

        if is_spread_ok(active_orders) and is_amounts_ok(active_orders) and is_delta_ok(event):
            obligations_fulfilled.append((True, order["timestamp"]))
        else:
            obligations_fulfilled.append((False, order["timestamp"]))

    time = calculate_time(obligations_fulfilled)
    total_time = get_total_time(list(order_events_generator()))
    percentage = time / total_time
    print("Market maker is fulfilling his obligations {:.2%} of time".format(percentage))
