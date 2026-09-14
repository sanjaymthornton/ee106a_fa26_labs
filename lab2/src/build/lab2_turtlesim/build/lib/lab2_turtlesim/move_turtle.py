import rclpy
from rclpy.node import Node
import std_msgs
import geometry_msgs
from std_msgs.msg import String
import sys

# We're creating a class called Talker, which is a subclass of Node
class MinimalPublisher(Node):

    # Here, we define the constructor
    def __init__(self, turtle_name):
        # We call the Node class's constructor and call it "minimal_publisher"
        super().__init__('minimal_publisher')
        self.publisher = self.create_publisher(Twist, f'/{turtle_name}/cmd_vel', 10)
         
    def run(self):
        while rclpy.ok():
            user_input = input()
            msg = Twist()

            if user_input == 'w':
                msg.linear.y = 1
            elif user_input == 'a':
                msg.linear.x = -1
            elif user_input == 's':
                msg.linear.y = -1
            elif user_input == 'd':
                msg.linear.x = 1
            elif user_input == 'j':
                msg.angular.z = 0.1
            elif user_input == 'l':
                msg.angular.z = -0.1


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher(turtle_name)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
