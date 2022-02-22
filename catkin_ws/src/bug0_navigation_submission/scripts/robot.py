from math import sqrt, radians, degrees, atan2
import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion


x = 0.0
y = 0.0
theta = 0.0
twist = Twist()

def newOdom(msg):
    global x,y,theta

    ort_q = msg.pose.pose.orientation

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    _,_,theta = euler_from_quaternion([ort_q.x, ort_q.y, ort_q.z, ort_q.w])


x_target = 2.0
y_target = 0.0
theta_target = 0.0
around_wall = False
straight_wall = False
following_wall = False
rotating = False
rotate_left = False

"""
scan direction


               0
               |
               |
               |
    90---------| --------- 270
               |
               |
               |
              180
"""


def scan(msg):
    global rotating, following_wall, around_wall, rotate_left, straight_wall
    arr = msg.ranges
    clear = True
    for i in range(0, 360):
        around_wall = True
        if (arr[i] < 0.37):
            if (0<=i<=90 and not rotating):
                #rotate right
                print("right")
                rotate_left = False
                rotating = True
                clear = False
            elif (270<=i<=359 and not rotating):
                #rotate left
                print("left")
                rotate_left = True
                rotating = True
                clear = False

    if (not rotating and around_wall and clear):
        straight_wall = False
        around_wall = False
        rotating = False
        following_wall = False


def go_straight():
    global x,y,theta, x_target, y_target
    theta_target = atan2(y_target-y, x_target-x)
    cmd_vel = Twist()
    cmd_vel.linear.x = 0.15
    cmd_vel.angular.z = 0.5*(theta_target - theta)
    return cmd_vel

def go_straight_wall():
    global straight_wall
    straight_wall = True
    cmd_vel = Twist()
    cmd_vel.linear.x = 0.15
    return cmd_vel

def follow_wall():
    global theta_target, rotating, following_wall
    cmd_vel = Twist()
    if (not following_wall):
        cmd_vel.linear.x = 0.0
        cmd_vel.angular.z = -0.15
        if (rotate_left and theta >= 0) :
            theta_target = radians(90)
            cmd_vel.angular.z *=-1
        elif (not rotate_left):
            theta_target = -radians(90)
        following_wall = True
        rotating = True
        return cmd_vel
    else:
        cmd_vel.linear.x = 0.0
        cmd_vel.angular.z = -0.15
        if (rotate_left) :
            cmd_vel.angular.z *=-1
        if (abs(theta_target - theta) < 0.05):
            rotating = False
            return go_straight_wall()
        return cmd_vel

def velocity():
    global around_wall
    if (not around_wall):
        return go_straight()
    else:
        return follow_wall()

    

if __name__ == "__main__":
    rospy.init_node("robot_node", anonymous=True)
    rospy.Subscriber("/odom", Odometry, newOdom)
    rospy.Subscriber("/scan", LaserScan, scan)
    cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    r = rospy.Rate(50)
    while not rospy.is_shutdown():
        if (abs(x-x_target) < 0.1 and abs(y-y_target) < 0.1):
            print(f"Destination reached at x = {x:.3f} ; y = {y:.3f}")
            cmd_vel_pub.publish(Twist())
            exit()
        else:
            cmd_vel_pub.publish(velocity())
        r.sleep()
