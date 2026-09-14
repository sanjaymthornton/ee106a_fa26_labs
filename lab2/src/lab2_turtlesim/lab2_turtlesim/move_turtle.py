import rclpy
from rclpy.node import Node
import std_msgs
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys

# We're creating a class called Talker, which is a subclass of Node
class MinimalPublisher(Node):

    # Here, we define the constructor
    def __init__(self, turtle_name):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Twist, f'/{turtle_name}/cmd_vel', 10)
         
    def run(self):
        while rclpy.ok():
            user_input = input("Press a letter to move:")
            msg = Twist()

            if user_input == 'w':
                msg.linear.y = 1.0
                msg.linear.x = 0.0
            elif user_input == 'a':
                msg.linear.x = -1.0
                msg.linear.y = 0.0
            elif user_input == 's':
                msg.linear.y = -1.0
                msg.linear.x = 0.0
            elif user_input == 'd':
                msg.linear.x = 1.0
                msg.linear.y = 0.0
            elif user_input == 'j':
                msg.angular.z = 1.0
            elif user_input == 'l':
                msg.angular.z = -1.0

            self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher(sys.argv[-1])
    minimal_publisher.run()
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
