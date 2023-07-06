import datetime
import json


def split_by_direction(orders):
    buy = [order for order in orders if order["direction"] == "buy"]
    sell = [order for order in orders if order["direction"] == "sell"]
    return buy, sell


def is_the_amounts_ok(orders):
    buy_orders, sell_orders = split_by_direction(orders)
    buy_amount = sum(buy["amount"] for buy in buy_orders)
    sell_amount = sum(sell["amount"] for sell in sell_orders)
    return buy_amount >= 5 and sell_amount >= 5


def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp) / 1000.0)


# TODO: replace the loop with yield statement
def is_delta_ok(timestamp, events):
    last_event = events[0]
    for event in events[1:]:
        if int(event["timestamp"]) > timestamp:
            break
        last_event = event
    print(convert_timestamp(last_event["timestamp"]), "-",
          convert_timestamp(event["timestamp"]),
          "\nTime:", convert_timestamp(timestamp))
    return float(last_event["delta"]) <= 0.7


# TODO: use min() and max()
def is_the_spread_ok(orders):
    buy_orders, sell_orders = split_by_direction(orders)
    max_buy_price, min_sell_price = 0, 0
    if len(buy_orders) > 0:
        max_buy_price = sorted(buy_orders, key=lambda order: order["price"], reverse=True)[0]["price"]
    if len(sell_orders) > 0:
        min_sell_price = sorted(sell_orders, key=lambda order: order["price"])[0]["price"]
    if min_sell_price == 0 and max_buy_price == 0:
        return False
    spread = abs(min_sell_price - max_buy_price)
    return spread <= 0.003

# def is_the_spread_ok(orders):
#     buy_orders, sell_orders = split_by_direction(orders)
#     max_buy_price, min_sell_price = 0, 0
#     if len(buy_orders) > 0:
#         max_buy_price = sorted(buy_orders, key=lambda order: order["price"], reverse=True)[0]["price"]
#     if len(sell_orders) > 0:
#         min_sell_price = sorted(sell_orders, key=lambda order: order["price"])[0]["price"]
#     if min_sell_price == 0 and max_buy_price == 0:
#         return False
#     spread = abs(min_sell_price - max_buy_price)
#     return spread <= 0.003


def get_total_time(orders):
    timestamps = sorted(set(map(lambda order: order["timestamp"], orders)))
    last_timestamp = timestamps[0]
    sum = 0
    for timestamp in timestamps:
        sum += timestamp - last_timestamp
    return sum


def obligations_fulfilled_time(lst):
    last = lst[0]
    sum = 0
    for time in lst[1:]:
        pass
        # check if the timestamp is "OK" or "NOT_OK"
        # calculate time between two "OK" timestamps and between "OK" and "NOT_OK"
        # time between two "NOT_OK" and "NOT_OK" and "OK" is not summed up
    return sum


if __name__ == '__main__':
    with open("order_events.json", "r") as file:
        order_events = json.load(file)
    with open("instrument_events.json", "r") as file:
        instrument_events = json.load(file)

    active = {}
    for order in order_events:
        if order["order_state"] == "open":
            active[order["order_id"]] = order
        else:  # order["order_state"] == "closed"
            active.pop(order["order_id"])
        print("Active:")
        active_orders = [item[1] for item in active.items()]
        for act in active_orders:
            print(act)
        print("Delta: ", is_delta_ok(order["timestamp"], instrument_events))
        print("Spread: ", is_the_spread_ok(active_orders))
        print("Amounts: ", is_the_amounts_ok(active_orders))
        print("\n")

    # by_timestamp = group_by_timestamp(order_events)

    # loop to print values
    # for in_timestamp in by_timestamp:
    #     buy_orders, sell_orders = split_by_direction(in_timestamp)
    #     print(is_the_spread_ok(in_timestamp))
    #     print(is_the_amounts_ok(in_timestamp))
    #     print("Buy")
    #     for order in buy_orders:
    #         print(order)
    #     print("Sell")
    #     for order in sell_orders:
    #         print(order)
    #     print("Next timestamp\n")
    # exit()

    # obligations_fulfilled = []
    # active = []
    # for in_timestamp in by_timestamp:
    #     for order in in_timestamp:
    #         if order["order_state"] == "open":
    #             # order already in active
    #             if order["order_id"] in [order["id"] for order in active]:
    #                 # update the order
    #                 pass
    #             # new order
    #             else:
    #                 active.append(order)
    #                 pass
    #         else:  # closed
    #             if order["order_id"] in [order["id"] for order in active]:
    #                 # remove the order
    #                 pass
    #
    #     # after every timestamp:
    #     timestamp = in_timestamp[0]["timestamp"]
    #     # check if sum of amounts for both sides >= 5
    #     # check if best prices diff <= 0.003
    #     if is_the_amounts_ok(active) and is_the_spread_ok(active) or not is_delta_ok(timestamp, instrument_events):
    #         # when delta > 0.7 then time is counted to fulfilled ???
    #
    #         # if condition above are satisfied then timestamp can be added
    #         # to list of fulfilling obligations timestamps
    #         obligations_fulfilled.append(("OK", timestamp))
    #     else:
    #         obligations_fulfilled.append(("NOT_OK", timestamp))
    #
    #     # from fulfilling obligations timestamps list the total amount
    #     # of time can be calculated
