import rospy
from std_msgs.msg import std_msgs
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

x = 5.54
y = 5.54
theta = 0.0

def pose_cb(msg):
    global x,y,theta
    x = msg.x
    y = msg.y
    theta = msg.theta

def move(vel_pub, speed, distance_target):
    #move forward for a certain distance_target
    global x,y
    distance = 0.0
    x0 = x
    y0 = y
    vel_cmd = Twist()
    loop_rate = rospy.Rate(10)
    vel_cmd.linear.x = speed
    while True:
        vel_pub.publish(vel_cmd)
        distance = abs(math.sqrt(((x-x0)**2) + ((y-y0)**2)))
        if (distance > distance_target):
            break
        loop_rate.sleep()
    vel_cmd.linear.x = 0
    vel_pub.publish(vel_cmd)

def rotate(vel_pub, ang_speed_deg, degree, clockwise):
    #rotate in place
    vel_cmd = Twist()
    ang_speed_rad = math.radians(abs(ang_speed_deg))
    if (clockwise):
        ang_speed_rad = -ang_speed_rad
    vel_cmd.angular.z = ang_speed_rad
    t0 = rospy.Time.now().to_sec()
    loop_rate = rospy.Rate(10)
    while True:
        vel_pub.publish(vel_cmd)

        t1 = rospy.Time.now().to_sec()
        deg_travelled = ang_speed_deg * (t1-t0)
        print(deg_travelled)
        loop_rate.sleep()
        if (deg_travelled > degree):
            break
    vel_cmd.angular.z = 0.0
    vel_pub.publish(vel_cmd)

def spiral(vel_pub, lin_speed, ang_speed_deg):
    global x,y
    vel_cmd = Twist()
    vel_cmd.angular.z = math.radians(ang_speed_deg)
    vel_cmd.linear.x = lin_speed
    loop_rate = rospy.Rate(1)
    while(x < 9.5 and y < 9.5):
        vel_pub.publish(vel_cmd)
        vel_cmd.linear.x += 0.5
        vel_cmd.linear.y = 0.0
        vel_cmd.linear.z = 0.0
        vel_cmd.angular.x = 0.0
        vel_cmd.angular.y = 0.0
        vel_cmd.angular.z = math.radians(ang_speed_deg)
        loop_rate.sleep()
    vel_cmd = Twist()
    vel_pub.publish(vel_cmd)

def goto(vel_pub, x_goal, y_goal):
    global x,y,theta
    loop_rate = rospy.Rate(10)
    vel_cmd = Twist()
    while True:
        distance_err = abs(math.sqrt(((x_goal-x)**2) + ((y_goal-y)**2)))
        k_linear = 1.0
        lin_speed = k_linear * distance_err

        k_angular = 4.0
        angle_goal = math.atan2((y_goal-y), (x_goal-x))
        ang_err = angle_goal - theta
        ang_speed = k_angular * ang_err

        vel_cmd.linear.x = lin_speed
        vel_cmd.angular.z = ang_speed

        vel_pub.publish(vel_cmd)
        loop_rate.sleep()
        
        if (distance_err < 0.01):
            break
    vel_cmd = Twist()
    vel_pub.publish(vel_cmd)

def orientation(vel_pub, ang_speed, deg_goal):
    global theta
    theta0 = theta
    loop_rate = rospy.Rate(10)
    rad_goal = math.radians(deg_goal) 
    vel_cmd = Twist()
    while True:   
        err = rad_goal-theta
        if (err>0):
            vel_cmd.angular.z = ang_speed
        else:
            vel_cmd.angular.z = -ang_speed
        vel_pub.publish(vel_cmd)
        loop_rate.sleep()
        if (abs(err) < 0.1):
            break
    vel_cmd = Twist()
    vel_pub.publish(vel_cmd)

def grid(vel_pub, ang_speed, lin_speed):
    goto(vel_pub, 1,1)
    orientation(vel_pub, 1, 0)
    for i in range(5):
        move(vel_pub, lin_speed, 1)
        orientation(vel_pub,1,90)
        move(vel_pub, lin_speed, 9)
        orientation(vel_pub,1, 0)
        move(vel_pub, lin_speed, 1)
        orientation(vel_pub,1, -90)
        move(vel_pub, lin_speed, 9)
        orientation(vel_pub,1, 0)
        

rospy.init_node("clean_node", anonymous=True)
vel_pub = rospy.Publisher("/turtle1/cmd_vel",Twist, queue_size=1000)
pose_sub = rospy.Subscriber("/turtle1/pose", Pose, pose_cb)
print("Welcome to Cleaning Robot Applicatiion")
print("Press 1 for spiral cleaning")
print("Press 2 for grid cleaning")
user = int(input(">>> "))
if (user == 1):
    spiral(vel_pub,0,120)
else :
    grid(vel_pub, 90, 1)
rospy.spin()
    
