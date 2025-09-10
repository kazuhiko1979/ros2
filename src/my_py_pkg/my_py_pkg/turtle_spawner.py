import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill
from turtlesim.msg import Pose
from my_robot_interfaces.msg import TurtleArray, Turtle
from my_robot_interfaces.srv import CatchTurtle
import random


class TurtleSpawner(Node):
    def __init__(self):
        super().__init__('turtle_spawner')
        self.turtle_prefix = 'turtle'
        self.turtle_count = 2
        self.alive_turtles = []
        self.publisher = self.create_publisher(TurtleArray, 'alive_turtles', 10)
        self.create_timer(1.0, self.spawn_turtle_timer)
        # kill turtle
        self.create_service(CatchTurtle, 'catch_turtle', self.catch_turtle_callback)
        
    
    def spawn_turtle_timer(self):
        if len(self.alive_turtles) < self.turtle_count:
            name = f'{self.turtle_prefix}_{random.randint(2, 100)}'
            x = random.uniform(1.0, 10.0)
            y = random.uniform(1.0, 10.0)
            self.get_logger().info(f"Trying to spawn {name} at ({x:.2f}, {y:.2f})")
            
            client = self.create_client(Spawn, 'spawn')
            if not client.wait_for_service(timeout_sec=1.0):
                self.get_logger().error('Service spawn not available')
                return
            
            req = Spawn.Request()
            req.x = x
            req.y = y
            req.theta = 0.0
            req.name = name
            future = client.call_async(req)
            future.add_done_callback(lambda f: self.handle_spawn_response(f, name, x, y))

            
    def handle_spawn_response(self, future, name, x, y):    
        if future.result() is not None:
            self.get_logger().info(f"Spawned turtle: {name} at ({x:.2f}, {y:.2f})")
            t = Turtle(name=name, x=x, y=y, theta=0.0)
            self.alive_turtles.append(t)
            # Pose購読を追加（動くごとに位置更新）
            self.create_subscription(Pose, f"{name}/pose", lambda msg, n=name: self.update_pose(n, msg), 10)
            self.publish_alive_turtles()
        else:
            self.get_logger().error("Spawn failed")
            
    def update_pose(self, name, msg):
        for t in self.alive_turtles:
            if t.name == name:
                t.x = msg.x
                t.y = msg.y
                t.theta = msg.theta
                break
        self.publish_alive_turtles()
        
                
    def publish_alive_turtles(self):
        msg = TurtleArray()
        msg.turtles = self.alive_turtles
        self.get_logger().info(f'Published {len(self.alive_turtles)} alive turtles: {[t.name for t in self.alive_turtles]}')
        self.publisher.publish(msg)
    
    
    def catch_turtle_callback(self, request, response):
        name = request.name
        client = self.create_client(Kill, 'kill')
        if not client.wait_for_service(timeout_sec=1.0):
            response.success = False
            return response
        
        req = Kill.Request()
        req.name = name
        future = client.call_async(req)
        future.add_done_callback(lambda f: self.handle_kill_response(f, name))
        
        response.success = True
        return response
    
    
    def handle_kill_response(self, future, name):
        if future.result() is not None:
            self.get_logger().info(f"Killed turtle: {name}")
            self.alive_turtles = [t for t in self.alive_turtles if t.name != name]
            self.publish_alive_turtles()
        else:
            self.get_logger().error(f"Failed to kill turtle: {name}")
    
    
    
def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawner()
    rclpy.spin(node)
    rclpy.shutdown()
    