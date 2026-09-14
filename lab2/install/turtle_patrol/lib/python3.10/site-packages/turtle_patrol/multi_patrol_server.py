import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from turtlesim.srv import TeleportAbsolute
from turtle_patrol_interface.srv import Patrol


class MultiTurtlePatrolServer(Node):
    def __init__(self):
        super().__init__('multi_turtle_patrol_server')
        self._turtles = {}
        # Publisher: actually drives turtle1
        self._srv = self.create_service(Patrol, '/turtle_patrol', self.patrol_callback)
        self._pub_timer = self.create_timer(0.1, self._publish_current_cmd)

    def handle_turtles(self, name):
        if name not in self._turtles:
            self._turtles[name] = {
                'pub': self.create_publisher(Twist, f'/{name}/cmd_vel', 10),
                'teleport': self.create_client(TeleportAbsolute, f'/{name}/teleport_absolute'),
                'lin': 0.0,
                'ang': 0.0,
            }
        return self._turtles[name]

    # -------------------------------------------------------
    # Timer publishes current Twist
    # -------------------------------------------------------
    def _publish_current_cmd(self):
        for value in self._turtles.values():
            msg = Twist()
            msg.linear.x = value['lin']
            msg.angular.z = value['ang']
            value['pub'].publish(msg)

    # -------------------------------------------------------
    # Service callback: update speeds
    # -------------------------------------------------------
    def patrol_callback(self, request: Patrol.Request, response: Patrol.Response):
        self.get_logger().info(
            f"Patrol request: vel={request.vel:.2f}, omega={request.omega:.2f}, posx={request.x:.2f}, posy={request.y:.2f}, theta={request.theta:.2f}, name={request.turtle_name}"
        )

        name = str(request.turtle_name)
        turtle_state = self.handle_turtles(name)

        # Update the speeds that the timer publishes
        vel = float(request.vel)
        turtle_state['lin'] = vel
        ang = float(request.omega)
        turtle_state['ang'] = ang

        tele = TeleportAbsolute.Request()
        tele.x = float(request.x)
        tele.y = float(request.y)
        tele.theta = float(request.theta)

        turtle_state['teleport'].call_async(tele)


        # Prepare response Twist reflecting current command
        # Update to display other attributes now too
        cmd = Twist()
        cmd.linear.x = vel
        cmd.angular.z = ang
        response.cmd = cmd

        self.get_logger().info(
            f"Streaming cmd_vel: lin.x={vel:.2f}, ang.z={ang:.2f} (10 Hz)"
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
