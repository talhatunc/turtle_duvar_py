#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class DuvardanKacan(Node):
	def __init__(self):
		super().__init__('duvar_kacan_node')
		self.declare_parameter('hiz', 1.0)
		self.declare_parameter('alt_sinir', 1.0)
		self.declare_parameter('ust_sinir', 10.0)

		self.abone = self.create_subscription(Pose, '/turtle1/pose', self.hareket_et, 10)
		self.yayinci = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

		self.create_timer(1.0, self.konum_yazdir)
		self.x = 0.0
		self.y = 0.0

	def hareket_et(self, msg):
		self.x = msg.x
		self.y = msg.y

		alt = self.get_parameter('alt_sinir').value
		ust = self.get_parameter('ust_sinir').value
		hiz = self.get_parameter('hiz').value

		komut = Twist()
		komut.linear.x = hiz
		if self.x < alt or self.x > ust or self.y < alt or self.y > ust:
			komut.angular.z = 5.0
		else:
			komut.angular.z = 0.0
		
		self.yayinci.publish(komut)

	def konum_yazdir(self):
		self.get_logger().info(f'x: {self.x:.2f}, y: {self.y:.2f}')

def main(args=None):
	rclpy.init(args=args)
	rclpy.spin(DuvardanKacan())
	rclpy.shutdown()

if __name__ == '__main__':
	main()
