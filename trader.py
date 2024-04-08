from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List

class Trader:

    def run(self, state: TradingState):
        to_trade_products = ["AMETHYSTS","STARFRUIT"]
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        
		# Orders to be placed on exchange matching engine
        result = {}
        for product in to_trade_products:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []

            market_trade = state.market_trades[product] if product in state.market_trades else []
            own_trade = state.own_trades[product] if product in state.own_trades else []
            all_trade = market_trade+own_trade
            cur_pos = state.position[product] if product in state.position else 0
            max_pos = 20
            print(f"Position for {product} : {cur_pos}")

            if product == 'AMETHYSTS':
                latest_time_stamp = all_trade[0].timestamp if len(all_trade) > 0 else None
                acceptable_price = 10000 if len(all_trade) == 0 else 0
                for trade in all_trade:
                    acceptable_price = trade.price if trade.timestamp > latest_time_stamp else acceptable_price
                    # acceptable_price += trade.price/len(all_trade)
                    latest_time_stamp = max(latest_time_stamp,trade.timestamp)
            else:
                acceptable_price = 0
                for trade in all_trade:
                    acceptable_price += trade.price/len(all_trade)

            if acceptable_price != None:
                print("Acceptable price : " + str(acceptable_price))
                print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
            
                if len(order_depth.sell_orders) != 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                    if int(best_ask) < acceptable_price and cur_pos < 20:
                        print("BUY", str(best_ask_amount) + "x", best_ask)
                        order_pos = min(-best_ask_amount,max_pos-cur_pos)
                        orders.append(Order(product, best_ask, order_pos))
                        cur_pos += order_pos
        
                if len(order_depth.buy_orders) != 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                    if int(best_bid) > acceptable_price and cur_pos > -20:
                        print("SELL", str(-best_bid_amount) + "x", best_bid)
                        order_pos = min(-best_bid_amount,-max_pos-cur_pos)
                        orders.append(Order(product, best_bid,order_pos))
                        cur_pos += order_pos

            result[product] = orders
    
		# String value holding Trader state data required. 
		# It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
		# Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData