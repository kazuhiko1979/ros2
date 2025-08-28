#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64

class NumberCounter(Node):
    def __init__(self):
        super().__init__('number_counter')
        self.subscriber = self.create_subscription(Int64, 'number', self.callback, 10)
        self.publisher = self.create_publisher(Int64, 'number_count', 10)
        self.counter = 0
    
    def callback(self, msg):
        self.counter += msg.data
        out_msg = Int64()
        out_msg.data = self.counter
        self.publisher.publish(out_msg)
        self.get_logger().info("Current Count: " + str(self.counter))

def main(args=None):
    rclpy.init(args=args)
    node = NumberCounter()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
        