from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    
    config = os.path.join(
    get_package_share_directory('my_robot_bringup'),
    'config',
    'turtle_controller_params.yaml'
    )
    
    turtle_controller_node = Node(
        package='my_py_pkg',
        executable='turtle_controller',
        name='turtle_controller',
        parameters=[config]
    )

    return LaunchDescription([
        turtle_controller_node
    ])