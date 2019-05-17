#!/usr/bin/env python
#!/usr/bin/env python
from __future__ import print_function
import rospy #importing the ros functions msg.range_max and msg.range_min
            #from geometry_msgs.msg import Twist #for im
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from math import radians

#from math import atan2


#Pre assigning the values for the variables as 0
state = 0
regions = {
    'right':    0,
    'froRight': 0,
    'front':    0,
    'froLeft':  0,
    'left':     0
}

#Pe-defined functions to read the values of messages laser scan and get the min value or closer object from the robot

def laser_read(msg):
    global regions
    regions = {
        'right':    min(msg.ranges[0:71]),
        'froRight': min(msg.ranges[72:143]),
        'front':    min(msg.ranges[144:215]),
        'froLeft':  min(msg.ranges[216:287]),
        'left':     min(msg.ranges[288:359]),
    }
    todo(msg)

#predefined functions for assignning the states for the
def change_state(new_state):
    global state
    if new_state != state:
        state = new_state
#Above sets the state of the robot to new state based upon its operation

#Function to check the laser scan with the Diatance
def todo(msg):
    infy = float('inf')
    global regions
    reg = regions
    d = 1.5
    if reg["front"] > d and reg["froLeft"] > d and reg["froRight"] > d:
        print("case 1 front")
        change_state(0)
    elif reg["front"] < d and reg["froLeft"] > d and reg["froRight"] > d:
        print("case 2 move Left")
        change_state(1)
    elif reg["front"] > d and reg["froLeft"] > d and reg["froRight"] < d:
        print("case 3 move right")
        change_state(1)
    elif reg["front"] > d and reg["froLeft"] < d and reg["froRight"] > d:
        print("case 4 move right")
        change_state(2)
    elif reg["front"] < d and reg["froLeft"] > d and reg["froRight"] < d:
        print("case 5 - move left")
        change_state(1)
    elif reg["front"] < d and reg["froLeft"] < d and reg["froRight"] > d:
        print("case 6 - move right")
        change_state(2)
    elif reg["front"] < d and reg["froLeft"] < d and reg["froRight"] < d:
        print ("case 7 - move left")
        change_state(1)
    elif reg["front"] > d and reg["froLeft"] < d and reg["froRight"] < d:
        print ("case 8 - go front")
        change_state(0)
    else:
        print("No states running")

def go_straight():
    print("Goin' straight!")
    speed = Twist()
    speed.linear.x = 0.3
    speed.angular.z = 0.0
    return speed

def turn_left():
    print("Turning left!")
    speed = Twist()
    speed.linear.x = 0.0
    speed.angular.z = 0.3
    return speed

def turn_right():
    print("Turning right!")
    speed = Twist()
    speed.linear.x = 0.0
    speed.angular.z = -0.6
    return speed

def stop():
    print("stop")
    speed = Twist()
    speed.linear.x = 0.0
    speed.angular.z = radians(1000)
    return speed

def main():
    global pub
    rospy.init_node("mini_project")
    pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size = 10)
    sub = rospy.Subscriber('/laserscan', LaserScan, laser_read)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        speed = Twist()
        if state == 0:
            speed = go_straight()
        elif state == 1:
            speed = turn_left()
        elif state == 2:
            speed = turn_right()
        elif state == 3:
            speed = stop()
        else:
            print("Problem in the robot")
        pub.publish(speed)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except:
        print("Unable to run the Program")
