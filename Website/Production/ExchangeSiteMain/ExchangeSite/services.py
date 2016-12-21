import sys



# This module contains hooks to internal business logic that allows for secure database changes



# Defines project path
sys.path.insert(0, "/home/mal/Programming/ExchangeMechanisms/Development")



def bid_price():
    import ExchangeEngineCollaborative as EEC
    bid_price = EEC.BidPriceChecker()
    return bid_price

def ask_price():
    import ExchangeEngineCollaborative as EEC
    ask_price = EEC.AskPriceChecker()
    return ask_price

def add_user(username, password, email, first_name, last_name):
    import DatabaseScripts.Users.DBAddUser as add_user
    add_user.main(username, password, email, first_name, last_name)

def add_basic_order(username, price, volume, order_type, order_action, trigger_type, trigger_value):
    import DatabaseScripts.BasicOrders.DBAddBasicOrder as add_basic_order
    order_number = add_basic_order.main(username, price, volume, order_type, order_action, trigger_type, trigger_value)
    print "ORDER NUMBER: " + str(order_number)
    return order_number

def get_basic_order_from_book(search_parameter, search_value):
    import DatabaseScripts.BasicOrders.DBSearchBasicOrderBook as get_basic_order_from_book
    # Enter search parameter in all caps with appropriate spacing between words
    print search_parameter
    print search_value
    orders = get_basic_order_from_book.main(search_parameter, search_value)
    return orders

def get_basic_order_from_log(search_parameter, search_value):
    import DatabaseScripts.BasicOrders.DBSearchBasicOrderLog as get_basic_order_from_log
    # Enter search parameter in all caps with appropriate spacing between words
    print search_parameter
    print search_value
    orders = get_basic_order_from_log.main(search_parameter, search_value)
    return orders

def add_instant_order(username, order_action, order_constraint, price, volume):
    import InstantOrderCollaborative as IOC
    order_number = IOC.main(username, order_action, order_constraint, price, volume, "NO")
    print "ORDER NUMBER: " + str(order_number)
    return order_number






