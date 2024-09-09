# Mock implementations of trading framework components

class ExecutionClient:
    def execute_order(self, product_id: str, amount: int, order_type: str):
        # This method will be overridden in the mock
        raise NotImplementedError

class PriceTick:
    def __init__(self, product_id: str, price: float):
        self.product_id = product_id
        self.price = price

class LimitOrderAgent:
    def __init__(self, execution_client: ExecutionClient):
        self.execution_client = execution_client
        self.orders = []  # A list to keep track of orders

    def price_tick(self, tick: PriceTick):
        # Handle market data and execute orders if necessary
        for order in self.orders:
            if (order['type'] == 'buy' and tick.price <= order['limit']) or \
               (order['type'] == 'sell' and tick.price >= order['limit']):
                # Execute the order
                self.execution_client.execute_order(
                    product_id=order['product_id'],
                    amount=order['amount'],
                    order_type=order['type']
                )
                # Remove the executed order
                self.orders.remove(order)

    def add_order(self, order_type: str, product_id: str, amount: int, limit: float):
        # Add a new order to the list
        self.orders.append({
            'type': order_type,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        })

    def handle_market_data(self, tick: PriceTick):
        # Example: Buy IBM when price drops below $100
        if tick.product_id == 'IBM' and tick.price < 100:
            self.execution_client.execute_order(
                product_id='IBM',
                amount=1000,
                order_type='buy'
            )

# Mock class for testing ExecutionClient
class MockExecutionClient(ExecutionClient):
    def execute_order(self, product_id: str, amount: int, order_type: str):
        print(f"Executed order: {order_type} {amount} shares of {product_id}")

# Test the implementation
def test_limit_order_agent():
    execution_client = MockExecutionClient()
    agent = LimitOrderAgent(execution_client)

    # Test handle_market_data method
    print("Testing handle_market_data method:")
    agent.handle_market_data(PriceTick('IBM', 95))  # Should execute a buy order for IBM

    # Add a sell order with a limit
    agent.add_order('sell', 'IBM', 500, 105)
    print("Orders before price tick:", agent.orders)
    
    # Test price_tick method
    print("Testing price_tick method:")
    agent.price_tick(PriceTick('IBM', 105))  # Should execute the sell order
    print("Orders after price tick:", agent.orders)

if __name__ == '__main__':
    test_limit_order_agent()
