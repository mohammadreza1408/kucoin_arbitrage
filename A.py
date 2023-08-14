import json
import time

import func_arbitrage

#Set Variables  
coin_price_url = 'https://api.kucoin.com'

def step_0():

    # Extract list of coins and prices from Exchange
    coin_json =func_arbitrage.get_coin_tickers('https://api.kucoin.com')

    # Loop through each objects and find the tradeable pairs
    coin_list = func_arbitrage.collect_tradeable(coin_json)

    # Return list of tradeable coins
    return coin_list


def step_1(coin_list):
    
    # Structure the list of tradeable triangular arbitrage pairs
    structured_list = func_arbitrage.structure_triangular_pair(coin_list)

    # Save structure list    
    with open("structured_triangular_pairs.json", "w") as fp:
        json.dump(structured_list, fp)



def step_2():

    # Get Structured Price
    with open("structured_triangular_pairs.json","r") as json_file:
        structured_price = json.load(json_file)


    #Get Latest Surface Price 
    #new_dict = {item['symbol']: item for item in a} 
    prices_json = func_arbitrage.get_coin_tickers(coin_price_url) 
    # print(prices_json)
    #Loop Thtough and Structure Price Information  
    for t_pair in structured_price:
        # print(t_pair)
        prices_dict = func_arbitrage.get_price_for_t_pair(t_pair, prices_json)
        surface_arb = func_arbitrage.calc_triangular_arb_surface_rate(t_pair, prices_dict)
        if len(surface_arb)> 0:
            real_rate_arb = func_arbitrage.get_depth_from_orderbook(surface_arb)
            print(real_rate_arb)
            time.sleep(20)
"""MAIN"""
if __name__ == "__main__":

    step_2()





