import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from turtlesim.srv import TeleportAbsolute
from turtle_patrol_interface.srv import Patrol


class MultiTurtlePatrolServer(Node):
    def __init__(self, turtle_name):
        super().__init__('multi_turtle_patrol_server')

        # Publisher: actually drives turtle1
        self._cmd_pub = self.create_publisher(Twist, f'/{turtle_name}/cmd_vel', 10)
        self._srv = self.create_service(Patrol, f'/{turtle_name}/patrol', self.patrol_callback)

        # Current commanded speeds (what timer publishes)
        self._lin = 0.0
        self._ang = 0.0
        self._posx = 0.0
        self._posy = 0.0
        self._angle = 0.0
        self._name = "turtle1"

        # Timer: publish current speeds at 10 Hz
        self._pub_timer = self.create_timer(0.1, self._publish_current_cmd)

        self.get_logger().info('MultiTurtlePatrolServer ready (continuous publish mode).')

    # -------------------------------------------------------
    # Timer publishes current Twist
    # -------------------------------------------------------
    def _publish_current_cmd(self):
        msg = Twist()
        msg.linear.x = self._lin
        msg.angular.z = self._ang
        self._cmd_pub.publish(msg)

    # -------------------------------------------------------
    # Service callback: update speeds
    # -------------------------------------------------------
    def patrol_callback(self, request: Patrol.Request, response: Patrol.Response):
        self.get_logger().info(
            f"Patrol request: vel={request.vel:.2f}, omega={request.omega:.2f}, posx={request.x:.2f}, posy={request.y:.2f}, theta={request.theta:.2f}, name={request.turtle_name}"
        )

        # Update the speeds that the timer publishes
        self._lin = float(request.vel)
        self._ang = float(request.omega)
        self._posx = float(request.x)
        self._posy = float(request.y)
        self._theta = float(request.theta)
        self._name = float(request.turtle_name)

        # Prepare response Twist reflecting current command
        # Update to display other attributes now too
        cmd = Twist()
        cmd.linear.x = self._lin
        cmd.angular.z = self._ang
        response.cmd = cmd

        self.get_logger().info(
            f"Streaming cmd_vel: lin.x={self._lin:.2f}, ang.z={self._ang:.2f} (10 Hz)"
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = MultiTurtlePatrolServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
