"""
Cookie Clicker Simulator.

Refine and test strategies for the 
pointless but popular online game "Cookie Clicker".

Simulate, plot and compare these strategies across 
your chosen length of time.
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self.__cookies__ = 0.0
        self.__total__ = 0.0
        self.__time__ = 0.0
        self.__cps__ = 1.0
        self.__history__ = [(0.0, None, 0.0, 0.0)]
            
    def __str__(self):
        """
        Return human readable game state.
        """
        return "Time: "+str(self.__time__)+"\nCPS: "+str(self.__cps__)+"\nCookies: "+str(self.__cookies__)+"\nTotal: "+str(self.__total__)
        
    def get_cookies(self):
        """
        Return current number of cookies.
        """
        return self.__cookies__
    
    def get_cps(self):
        """
        Get current CPS.
        """
        return self.__cps__
    
    def get_time(self):
        """
        Get current game time.
        """
        return self.__time__
    
    def get_history(self):
        """
        Returns (copy of) simulation history.
        """
        history_copy = list(self.__history__)
        return history_copy

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies.
        """
        seconds = max(0.0,
                      math.ceil((cookies - self.__cookies__)/self.__cps__))
        return seconds
    
    def wait(self, time):
        """
        Wait for given amount of time and update state.
        """
        if time > 0.0:
            self.__cookies__ += time*self.__cps__
            self.__total__ += time*self.__cps__
            self.__time__ += time
        return
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state.
        """
        if cost <= self.__cookies__:
            self.__cookies__ -= cost
            self.__cps__ += additional_cps
            self.__history__.append((self.__time__,
                                     item_name,
                                     cost,
                                     self.__total__))
        return
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    game = ClickerState()
    copy_info = build_info.clone()
    
    while game.get_time() <= duration:
        time = game.get_time()
        item = strategy(game.get_cookies(),
                        game.get_cps(),
                        game.get_history(),
                        duration-time,
                        copy_info)
        if item == None:
            if duration == time:
                break
            else:
                game.wait(duration-time)

        else:
            cost = copy_info.get_cost(item)
            if game.time_until(cost) > duration-time:
                if duration == time:
                    break
                else:
                    game.wait(duration-time)
                break
            else:
                game.wait(game.time_until(cost))
                game.buy_item(item,cost,copy_info.get_cps(item))
                copy_info.update_item(item)

    
    return game


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Blank strategy: Never builds anything.
	For debugging. Or, implement your own strategy here!
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    funds = cookies + cps*time_left
    costs = [build_info.get_cost(item) for item in build_info.build_items()]
    items = [item for item in build_info.build_items()]
    choice = None
    choice_cost = funds
    for idx in range(len(items)):
        if costs[idx] <= choice_cost:
            choice = items[idx]
            choice_cost = costs[idx]
    return choice

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive affordable item.
    """
    funds = cookies + cps*time_left
    costs = [build_info.get_cost(item) for item in build_info.build_items()]
    items = [item for item in build_info.build_items()]
    choice = None
    choice_cost = 0.0
    for idx in range(len(items)):
        if costs[idx] > choice_cost and costs[idx] <= funds:
            choice = items[idx]
            choice_cost = costs[idx]
    return choice

def strategy_value(cookies, cps, history, time_left, build_info):
    """
    Buy the item with the best cps/cost ratio.
    """
    costs = [build_info.get_cost(item)/build_info.get_cps(item) for item in build_info.build_items()]
    dummy_val, idx = min((val, idx) for (idx, val) in enumerate(costs))
    return build_info.build_items()[idx]
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print "\n", strategy_name, ":\n", state

    # Plot total cookies over time
    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("None", SIM_TIME, strategy_none)
    #run_strategy("Broken Cursor", SIM_TIME, strategy_cursor_broken)
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_value)
    
#run()
    

