#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
      

def main(args=None):
    rclpy.init(args=args)
    node = Node("add_two_ints_client_no_opp")
    
    client = node.create_client(AddTwoInts, 'add_two_ints')
    while not client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('Waiting for Add Two Ints server...')
        
    request = AddTwoInts.Request()
    request.a = 3
    request.b = 8
    future = client.call_async(request)
    rclpy.spin_until_future_complete(node, future)
    if future.result() is not None:
        response = future.result()
        node.get_logger().info(f'Result of add_two_ints: {response.sum}')
    else:
        node.get_logger().error('Service call failed')
    # node.destroy_node()
    
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
        