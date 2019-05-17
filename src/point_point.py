#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from tf.transformations import euler_from_quaternion
from tf import transformations
from geometry_msgs.msg import Point, Twist
from math import atan2

x = 0.0
y = 0.0
theta = 0.0
def newOdom(msg):
     global x
     global y
     global theta
     rospy.loginfo("Node was started")
     x = msg.pose.pose.position.x
     y = msg.pose.pose.position.y

     rot_q = msg.pose.pose.orientation
     (roll, pitch, theta) = euler_from_quaternion ([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
#Yaw is the rotation in the Z direction

rospy.init_node ("point_point")

sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size = 1)
#sub = rospy.Subscriber("")
speed = Twist()
r = rospy.Rate(10)
goal = Point()
goal.x = 3.22
goal.y = 8.70

while not rospy.is_shutdown():
    inc_x = goal.x - x
    inc_y = goal.y - y
    angle_to_goal = atan2(inc_y, inc_x)
    if abs(angle_to_goal - theta) > 0.05:
        #print "Found the Goal"
        speed.linear.x = 0.5
        speed.angular.z = 0.3
        #print "value of speed: ", speed
        pub.publish(speed)
    else:
        if goal.x == x and goal.y == y:
           speed.linear.x = 0.0

           #speed.angular.z = 0.0


    pub.publish(speed)
    #rospy.spin()
    r.sleep()

if __name__ == '__main__':
    try:
        main()
    except:
        print("Something wrong!")
