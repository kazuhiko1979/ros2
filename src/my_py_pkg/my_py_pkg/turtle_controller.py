import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle
import math

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.target = None
        self.pose = None
        self.create_subscription(Pose, 'turtle1/pose', self.pose_callback, 10)
        self.create_subscription(TurtleArray, 'alive_turtles', self.turtles_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.control_loop)
        
    def pose_callback(self, msg):
        self.pose = msg
        
    def turtles_callback(self, msg):
        if msg.turtles:
            self.target = msg.turtles[0]  # target the first turtle in the list
        else:
            self.target = None
            
    def control_loop(self):
        if self.pose is None or self.target is None:
            return
        
        dx = self.target.x - self.pose.x
        dy = self.target.y - self.pose.y
        distance = math.hypot(dx, dy)
        angle_to_target = math.atan2(dy, dx)
        
        # --- 修正ポイント: 角度差を [-pi, pi] に正規化 ---
        angle_diff = angle_to_target - self.pose.theta
        angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))
        
        twist = Twist()
        if distance > 0.5:
            twist.linear.x = 2.0 * distance
            twist.angular.z = 6.0 * angle_diff
        else:
            self.catch_turtle(self.target.name)
        self.cmd_pub.publish(twist)
        
    def catch_turtle(self, name):
        client = self.create_client(CatchTurtle, 'catch_turtle')
        if not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error('Service catch_turtle not available')
            return
        req = CatchTurtle.Request()
        req.name = name
        future = client.call_async(req)
        future.add_done_callback(lambda f: self.handle_catch_response(f, name))
        
    def handle_catch_response(self, future, name):
        if future.result() is not None and future.result().success:
            self.get_logger().info(f'Caught turtle: {name}')
            self.target = None
        else:
            self.get_logger().error(f'Failed to catch turtle: {name}')
        
def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    rclpy.shutdown()