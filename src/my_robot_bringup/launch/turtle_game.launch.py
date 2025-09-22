from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    
    config = os.path.join(
    get_package_share_directory('my_robot_bringup'),
    'config',
    'turtles.yaml'
    )
    
    ld = LaunchDescription()
    
    # turtlesim 本体
    turtle_game = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim'
    )
    
    # spawner
    turtle_spawner_node = Node(
        package='my_py_pkg',
        executable='turtle_spawner',
        name='turtle_spawner',
        parameters=[config]
    )
    
    # controller
    turtle_controller_node = Node(
        package='my_py_pkg',
        executable='turtle_controller',
        name='turtle_controller',
        parameters=[config]
    )
    
    ld.add_action(turtle_game)
    ld.add_action(turtle_spawner_node)
    ld.add_action(turtle_controller_node)
    
    return ld
