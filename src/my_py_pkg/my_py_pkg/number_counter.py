#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class NumberCounter(Node):
    def __init__(self):
        super().__init__('number_counter')
        self.subscriber = self.create_subscription(Int64, 'number', self.callback, 10)
        self.publisher = self.create_publisher(Int64, 'number_count', 10)
        
        # Sercive server /reset_counter
        self.reset_counter_service = self.create_service(SetBool, 'reset_counter', self.callback_reset_counter)
        self.counter_ = 0
        
    
    def callback(self, msg):
        self.counter_ += msg.data
        out_msg = Int64()
        out_msg.data = self.counter_
        self.publisher.publish(out_msg)
        self.get_logger().info("Current Count: " + str(self.counter_))
        
    def callback_reset_counter(self, request:SetBool.Request, response:SetBool.Response):
        if request.data:
            self.counter_ = 0
            response.success = True
            response.message = "Counter has been reset."
            self.get_logger().info("Counter has been reset to zero.")
        else:
            response.success = False
            response.message = "Counter has not been reset."
            self.get_logger().info("Counter reset request denied.")
        return response

def main(args=None):
    rclpy.init(args=args)
    node = NumberCounter()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
        