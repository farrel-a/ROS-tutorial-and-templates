#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def talker():
    rospy.init_node('talker', anonymous=True) #(node name, ensure unique)
    pub = rospy.Publisher('chatter', String, queue_size = 10) #(topic name, data type, queue size)
    rate = rospy.Rate(10) #10Hz
    while not rospy.is_shutdown(): 
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str) #std::cout or printf
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: #SIGINT handler
        pass