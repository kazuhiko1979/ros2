from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    
    config = os.path.join(
        get_package_share_directory('my_robot_bringup'),
        'config',
        'robot_news_params.yaml'
    )
    
    ld = LaunchDescription()
    
    robot_news_station_gliskard = Node(
        package='my_py_pkg', 
        executable='robot_news_station',
        name= "robot_news_station_gliskard",
        # parameters=[{'robot_name': 'glikard'}],
        parameters=[config],  # Alternative way to load from config fil
    )
    
    robot_news_station_bb8 = Node(
        package='my_cpp_pkg', 
        executable='robot_news_station',
        name= "robot_news_station_bb8",
        # parameters=[{'robot_name': 'bb8'}],
        parameters=[config],  # Alternative way to load from config file
    )
    
    robot_news_station_daneel = Node(
        package='my_py_pkg', 
        executable='robot_news_station',
        name= "robot_news_station_daneel",
        # parameters=[{'robot_name': 'daneel'}],
        parameters=[config],  # Alternative way to load from config file
    )
    
    robot_news_station_lander = Node(
        package='my_cpp_pkg', 
        executable='robot_news_station',
        name= "robot_news_station_lander",
        # parameters=[{'robot_name': 'lander'}],
        parameters=[config],  # Alternative way to load from config file
    )
    
    robot_news_station_c3po = Node(
        package='my_py_pkg', 
        executable='robot_news_station',
        name= "robot_news_station_c3po",
        # parameters=[{'robot_name': 'c3po'}],
        parameters=[config],  # Alternative way to load from config file
    )
    
    smartphone = Node(
        package='my_cpp_pkg', 
        executable='smartphone',
        name= "smartphone"
    )
    
    ld.add_action(robot_news_station_gliskard)
    ld.add_action(robot_news_station_bb8)
    ld.add_action(robot_news_station_daneel)
    ld.add_action(robot_news_station_lander)
    ld.add_action(robot_news_station_c3po)
    ld.add_action(smartphone)
    
    return ld
    